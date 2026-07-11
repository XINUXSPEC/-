from ToolFun import *
import time

class pgbar:
    width = 100
    def __init__(self,):
        self.total_byte = 0                          #总大小
        self.total_text = None                       #总大小文本(单位)
        self.file_name = None                        #下载文件
        self.desc = None                             #状态描述
        self.download_size = 0                       #已下载大小
        self.speed = 0                               #速度
        self.cycle_size = 0                          #用来记录下载的量
        self.cycle_time = 0                          #用来记录周期开始的时间
        self.first = False
        self.start_time = None


    def init_info(self,total_byte,filename,download_size=0):
        self.total_byte = total_byte
        if total_byte:
            self.total_text = get_unit(total_byte)
        self.file_name = filename
        self.download_size = download_size
        self.speed = 0
        self.cycle_size = 0
        self.cycle_time = time.time()
        self.start_time = self.cycle_time
        self.first = False

    def render(self):

        if self.first:
            if self.total_text:
                print("\033[3F", end="")  # 上移三行
                print("\033[J", end="")  # 清除旧内容
            else:
                print("\033[2F", end="")  # 上移两行
                print("\033[J", end="")  # 清除旧内容
        self.first = True
        # 第一行：文件名
        print(BOLD+f"{WHITE}📄  {self.file_name}{RESET}")

        # 第二行和第三行
        if self.total_byte:
            self._render_know()
        else:
            self._render_unknow()
    def _render_know(self):
        if self.download_size < self.total_byte:
            self.speed = round(self.cycle_size / (time.time() - self.cycle_time), 1)
            self.desc = get_unit(self.speed) + '/s'
        else:
            self.desc = "完成"
        # 第二行：下载信息
        percent = self.download_size / self.total_byte * 100
        print(
            f"{CYAN}{self.desc}{RESET}   "
            f"{YELLOW}{get_unit(self.download_size)}{RESET} / "
            f"{YELLOW}{get_unit(self.total_byte)}{RESET}   "
            f"{GREEN}({percent:.1f}%){RESET}"
        )

        # 第三行：进度条
        ratio = self.download_size / self.total_byte
        filled = int(self.width * ratio)
        second = (self.total_byte - self.download_size) / self.speed

        bar = (
                BRIGHT_GREEN +
                ("✔ " if self.download_size >= self.total_byte else "⬇ ") +
                GREEN +
                "━" * filled +
                GRAY +
                "─" * (self.width - filled) +
                RED +
                "  ETA " + f'{format(int(second / 60), "02d")}:{format(int(second % 60), "02d")}' +
                RESET
        )
        print(bar)

    def _render_unknow(self):
        self.speed = round(self.cycle_size / (time.time() - self.cycle_time), 1)
        self.desc = get_unit(self.speed) + '/s'
        print(
            f"{CYAN}速度：{self.desc}{RESET}   ",
            f"{YELLOW}已下载：{get_unit(self.download_size)}{RESET}"
        )


    def update(self,sz):
        self.cycle_size +=sz
        self.download_size += sz
        if time.time() - self.cycle_time >= 0.5:
            self.render()
            self.cycle_size = 0
            self.cycle_time = time.time()

    def finish(self):
        self.render()
        tm = time.time() - self.start_time
        print("\n")
        print(
            f"{CYAN}📦 总大小:{RESET} "
            f"{BRIGHT_YELLOW}{get_unit(self.download_size)}{RESET}"
        )

        print(
            f"{CYAN}⏱ 耗时:{RESET} "
            f"{BRIGHT_WHITE}{tm:.1f}{RESET}"
            f"{GRAY}s{RESET}"
        )

        print(
            f"{CYAN}⚡ 平均速度:{RESET} "
            f"{BRIGHT_GREEN}{get_unit(self.download_size / tm)}{RESET}"
            f"{GRAY}/s{RESET}"
        )



