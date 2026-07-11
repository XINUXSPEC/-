import os
from os import makedirs
from ToolFun import *

class Task:
    max_retransmit_cnt = 5
    def __init__(self):
        self._url = None
        self._file_name = None
        self._root_url = None
        self._ret_cnt = 0
        self._ret_range = None
        self.headers = {
            "User-Agent": "MyDownloader/1.0"
        }

    def init_info(self,url,file_name,root_url="./"):
        self._url = url
        self._ret_cnt = 0
        self._file_name = file_name
        if not os.path.exists(root_url):
            makedirs(root_url)
        self._root_url = root_url

    def inti_retransmit_state(self):
        self._ret_cnt += 1
        self._ret_range = os.path.getsize(self._root_url+self._file_name)
        self.headers["Range"] = f"bytes={self._ret_range}-"

    def init_resume_state(self):
        self._ret_range = os.path.getsize(self._root_url+self._file_name)
        self.headers["Range"] = f"bytes={self._ret_range}-"

    def get_ret_cnt(self):
        return self._ret_cnt

    def can_retransmit(self):
        return self._ret_cnt < self.max_retransmit_cnt

    def get_ret_range(self):
        return self._ret_range

    def get_file_name(self):
        return self._file_name

    def get_url(self):
        return self._url

    def get_root_url(self):
        return self._root_url

    def get_local_url(self):
        return self._root_url+self._file_name

