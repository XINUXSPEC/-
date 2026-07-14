import os
import copy
import threading
import traceback

from requests.exceptions import ChunkedEncodingError

from Work import *

class WorkFlow:
    def __init__(self):
        self.work = Work()

    def resume_download(self,task):
        try:
            if not os.path.exists(task.get_local_url()):
                open(task.get_local_url(), 'w').close()
            task.init_resume_state()
            self.work.continue_download(task)
        except (
                TimeoutError,
                ConnectionError,
                ChunkedEncodingError,
        ) as e:
            self._retransmit(task)
        except FileNotFoundError as e:
            print(e)
            traceback.print_exc()
        except Exception as e:
            print(type(e))
            traceback.print_exc()


    def download(self,task):
        try:
            if not os.path.exists(task.get_local_url()):
                open(task.get_local_url(), 'w').close()
            self.work.download(task)
        except (
                TimeoutError,
                ConnectionError,
                ChunkedEncodingError,
        ) as e:
            self._retransmit(task)
        except FileNotFoundError as e:
            print(e)
            traceback.print_exc()
        except Exception as e:
            print(type(e))
            traceback.print_exc()


    # 重传
    def _retransmit(self,task):
        if task.can_retransmit() is False:
            print("重试失败")
            return
        try:
            if not os.path.exists(task.get_local_url()):
                open(task.get_local_url(), 'w').close()
            task.init_retransmit_state()
            print("连接失败,进行断点重传")

            self.work.continue_download(task)
        except FileNotFoundError as e:
            print(e)
            traceback.print_exc()
        except (
                TimeoutError,
                ConnectionError,
                ChunkedEncodingError,
        ) as e:
            self._retransmit(task)
        except Exception as e:
            print(type(e))
            traceback.print_exc()

    # 指定块进行下载
    def chunk_download(self,task):
        try:
            if not os.path.exists(task.get_local_url()):
                open(task.get_local_url(), 'w').close()
            self.work.chunk_download(task)
        except (
                TimeoutError,
                ConnectionError,
                ChunkedEncodingError,
        ) as e:
            self._retransmit(task)
        except FileNotFoundError as e:
            print(e)
            traceback.print_exc()
        except Exception as e:
            print(type(e))
            traceback.print_exc()


    # 拆分任务与多线程下载
    def multithread_download(self,task):
        if not self._check_chunk(task):
            print("该服务器不支持分块传输")
            self.download(task)
            return
        try:
            all_size = self.work.get_file_size(task)
        except KeyError:
            #TODO
            print("服务器返回数据包响应头没有总长度")
            traceback.print_exc()
            exit(0)
        except TypeError:
            #TODO
            print("类型出错")
            traceback.print_exc()
            exit(0)
        print("文件总大小:"+str(all_size))
        thread_num = 4
        chunk_size = int(all_size / thread_num)
        tasks = []
        print("线程个数"+str(thread_num))
        for i in range(thread_num):
            taski=copy.deepcopy(task)
            if i != thread_num-1:
                taski.init_chunk_state((i*chunk_size,(i+1)*chunk_size))
                taski.set_size(chunk_size)
            else:
                taski.init_last_state(i*chunk_size)
                taski.set_size(all_size - i*chunk_size)
            tasks.append(taski)

        threads = []
        for taski in tasks:
            threads.append(threading.Thread(target=self.chunk_download,args=(taski,)))
            threads[-1].start()

        for t in threads:
            t.join()


    # 测试是否支持分块传输TODO::
    def _check_chunk(self,task):
        return True
