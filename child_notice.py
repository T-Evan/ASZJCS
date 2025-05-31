# 导包
import time

from .baseUtils import *
from .res.ui.ui import 功能开关
from ascript.android.screen import FindColors
from ascript.android import screen
from ascript.android import system
from ascript.android.system import ShellListener

checkSkipTime = 0
checkLoginTime = 0


# 实例方法
def main():
    global checkSkipTime
    checkSkipTime = time.time()
    checkLoginTime = time.time()
    while True:
        sleep(4)  # 等待 5 秒
        noticeCancel()


def noticeCancel():
    re = FindColors.find("328,909,#F6F95C|413,910,#F6F95C|303,1000,#FFFF7B|380,999,#FFFF75", diff=0.9)
    if not re:
        re = FindColors.find("298,535,#F2F65A|367,536,#F2F65B|279,842,#F2F65A|356,842,#F2F65A", diff=0.9)
    if not re:
        re = FindColors.find("484,1190,#F1FD2A|484,1210,#F0FC21|585,1190,#F0F559|587,1216,#F0FE23", diff=0.9)
    if re:
        Toast('点击教程')
        print(re.x, re.y)
        tapSleep(re.x + 5, re.y + 5)
    return


class L(ShellListener):
    def commandOutput(self, i: int, s: str):
        print('?', s)

    def commandTerminated(self, i: int, s: str):
        pass

    def commandCompleted(self, i: int, i1: int):
        pass
