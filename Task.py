import os
from os import makedirs
from ToolFun import *

class Task:
    max_retransmit_cnt = 5
    def __init__(self):
        self.last_range = None
        self._range = None
        self._url = None
        self._file_name = None
        self._root_url = None
        self._ret_cnt = 0
        self._start_range = None
        self.headers = {
            "User-Agent": "MyDownloader/1.0"
        }
        self._size = None
        self.is_last_state = False

    def init_info(self,url,file_name,root_url="./"):
        self._url = url
        self._ret_cnt = 0
        self._file_name = file_name
        if not os.path.exists(root_url):
            makedirs(root_url)
        self._root_url = root_url

    def init_retransmit_state(self):
        self._ret_cnt += 1
        self._start_range = os.path.getsize(self._root_url + self._file_name)
        self.headers["Range"] = f"bytes={self._start_range}-"

    def init_resume_state(self):
        self._start_range = os.path.getsize(self._root_url + self._file_name)
        self.headers["Range"] = f"bytes={self._start_range}-"

    def init_chunk_state(self,new_range):
        start,end = self._range = new_range
        self._start_range =start
        self.headers["Range"] = f"bytes={start}-{end}"

    def init_last_state(self,last_range):
        self.headers["Range"] = f"bytes={last_range}-"
        self.is_last_state = True
        self.last_range=last_range

    def get_ret_cnt(self):
        return self._ret_cnt

    def can_retransmit(self):
        return self._ret_cnt < self.max_retransmit_cnt

    def get_start_range(self):
        return self._start_range

    def get_file_name(self):
        return self._file_name

    def get_url(self):
        return self._url

    def get_root_url(self):
        return self._root_url

    def get_local_url(self):
        return self._root_url+self._file_name

    def get_size(self):
        return self._size

    def set_file_name(self,file_name):
        self._file_name = file_name

    def set_size(self,size):
        self._size = size

    def get_range(self):
        return self._range

    def get_last_range(self):
        return self.last_range