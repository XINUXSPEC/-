import os

from Work import *

class WorkFlow:
    def __init__(self):
        self.work = Work()

    def resume_download(self,task):
        try:
            if os.path.exists(task.get_local_url()) is False:
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


    #重传
    def _retransmit(self,task):
        if os.path.exists(task.get_local_url()) is False:
            open(task.get_local_url(), 'w').close()
        if task.can_retransmit() is False:
            print("重试失败")
            return
        try:
            task.inti_retransmit_state()
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
