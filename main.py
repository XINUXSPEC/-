import time
import requests
from ToolFun import *
from pgbar import *




# https://proof.ovh.net/files/1Mb.dat?ss=1
def download():
    url = input("下载链接:")
    bar = pgbar()

    response = requests.get(url,stream=True)

    filename = getfilename(response.url)
    if response.headers["Content-Length"]:
        filesize = int(response.headers.get("Content-Length"))
    else:
        filesize = 0
        print("文件大小为0")
        exit(0)

    bar.file_name = filename
    bar.size = filesize
    bar.init_info(filesize,filename)

    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024*48):
            f.write(chunk)
            bar.update(len(chunk))
    bar.finish()

download()
