import requests

from pgbar import *

class Work:
    def __init__(self):
        pass

    # 下载工作
    # 参数: task 任务所需参数
    def download(self,task):
        bar = pgbar()
        url = task.get_url()
        filename = task.get_file_name()
        local_url = task.get_root_url()+filename

        with requests.get(url, stream=True, timeout=(5, 10)) as response:
            if response.headers.get("Content-Length"):
                filesize = int(response.headers["Content-Length"])
            else:
                filesize = None
                print("文件大小未知")
            bar.init_info(filesize, filename)

            with open(local_url, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 48):
                    f.write(chunk)
                    bar.update(len(chunk))
            bar.finish()



    # 断点重传
    def continue_download(self,task):
        bar = pgbar()
        url = task.get_url()
        filename = task.get_file_name()
        local_url = task.get_root_url() + filename
        task_range = task.get_ret_range()
        with requests.get(url, stream=True, timeout=(5, 10),headers=task.headers) as response:
            if response.headers.get("Content-Length"):
                filesize = int(response.headers["Content-Length"])+task_range
            else:
                filesize = None
                print("文件大小未知")
            bar.init_info(filesize, filename,task_range)
            with open(local_url, "a+b") as f:
                for chunk in response.iter_content(chunk_size=1024 * 48):
                    f.write(chunk)
                    bar.update(len(chunk))
            bar.finish()

    # 指定Range偏移进行下载
    def chunk_download(self,task):
        url = task.get_url()
        local_url = task.get_local_url()
        if not task.is_last_state:
            start,end = task.get_range()
        else :
            start = task.get_last_range()
        with requests.get(url, stream=True, timeout=(5, 10),headers=task.headers) as response:
            with open(local_url, "r+b") as f:
                f.seek(start)
                for chunk in response.iter_content(chunk_size=1024 * 48):
                    f.write(chunk)
        print("下载完成,大小为"+str(task.get_size()),"开始位置",start)


    # 获取文件的大小
    def get_file_size(self,task):
        url = task.get_url()
        response = requests.get(url, stream=True, timeout=(5, 10))
        return  int(response.headers.get("Content-Length"))