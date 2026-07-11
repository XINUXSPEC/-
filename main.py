from Task import *
from WorkFlow import *


url = input("下载链接:")
task = Task()
task.init_info(url, getfilename(url))
workflow = WorkFlow()
workflow.resume_download(task)
