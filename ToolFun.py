def getfilename(url):
    index=url.rfind("/")
    index1=url.find("?")
    if index1 ==-1:
        return url[index+1:]
    return url[index+1:index1]

def get_unit(size):
    if size >=1024*1024*1024:
        return str(round(size/1024/1024/1024,1))+" GB"
    elif size >=1024*1024:
        return str(round(size/1024/1024,1))+" MB"
    elif size >=1024:
        return str(round(size/1024,1))+" KB"
    else:
        return str(size)+ "B"


# ===== 前景色 =====
BLACK         = "\033[30m"
RED           = "\033[31m"
GREEN         = "\033[32m"
YELLOW        = "\033[33m"
BLUE          = "\033[34m"
MAGENTA       = "\033[35m"       # 紫色
CYAN          = "\033[36m"
WHITE         = "\033[37m"
GRAY          = "\033[90m"       # 灰色

# ===== 亮色 =====
BRIGHT_BLACK  = "\033[90m"       # 深灰
BRIGHT_RED    = "\033[91m"
BRIGHT_GREEN  = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE   = "\033[94m"
BRIGHT_MAGENTA= "\033[95m"
BRIGHT_CYAN   = "\033[96m"
BRIGHT_WHITE  = "\033[97m"

# ===== 字体效果 =====
BOLD          = "\033[1m"    # 加粗
DIM           = "\033[2m"    # 变暗
ITALIC        = "\033[3m"    # 斜体（部分终端支持）
UNDERLINE     = "\033[4m"    # 下划线
REVERSE       = "\033[7m"    # 前景/背景反色

# ===== 重置 =====
RESET         = "\033[0m"