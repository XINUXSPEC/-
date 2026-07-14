from Task import *
from WorkFlow import *


url = input("下载链接:")

start=time.time()
task = Task()
task.init_info(url, getfilename(url))
workflow = WorkFlow()
workflow.multithread_download(task)

print("使用时间\n"+str(time.time()-start))
