# 导包
import time

from .baseUtils import *
from .res.ui.ui import 功能开关
from ascript.android.screen import FindColors
from ascript.android import screen
from ascript.android import system
from ascript.android.system import ShellListener
from .daily import DailyTask
from .startUp import StartUp

checkSkipTime = 0  # 检查游戏操作卡死，退回首页再返回游戏
checkLoginTime = 0

dailyTask = DailyTask()
startupTask = StartUp(f"{功能开关['游戏包名']}")


# 实例方法
def main():
    global checkSkipTime
    checkSkipTime = time.time()
    checkOpenTime = time.time()  # 检测悬浮窗打开
    while True:
        sleep(4)  # 等待 5 秒
        # noticeCancel()
        if 功能开关["顶号等待"] != "" and 功能开关["顶号等待"] != "0":
            anotherLogin()

        # 检查辅助点开，游戏操作卡死
        if time.time() - checkOpenTime > 10:
            checkOpenTime = time.time()
            re = FindColors.find("236,222,#EA2D5E|233,236,#ECEFF1|217,233,#EA2D5E|255,236,#EA2D5E|238,258,#EA2D5E",
                                 rect=[1, 110, 88, 348], diff=0.95)
            if re:
                tapSleep(12, 56)

        if time.time() - checkSkipTime > 900:
            checkSkipTime = time.time()
            action.Key.home()
            sleep(2)
            system.open(startupTask.app_name)


def anotherLogin():
    res1, _ = TomatoOcrText(313, 70, 403, 122, "公告")
    if res1:
        tapSleep(314, 1230)  # 关闭首页公告

    res1, _ = TomatoOcrText(231, 562, 485, 609, "登录", match_mode='fuzzy')
    if res1:
        print("顶号等待，检查被顶号")
        start_time = int(time.time())
        need_another_minute = safe_int(功能开关.get("顶号等待", 0))  # 分钟
        if need_another_minute == '':
            need_another_minute = 0
        total_another_minute = need_another_minute * 60
        while True:
            功能开关["needHome"] = 0
            功能开关["fighting"] = 1
            current_time = int(time.time())
            if total_another_minute != 0 and current_time - start_time >= total_another_minute:
                Toast("顶号等待，开始重新登录")
                for i in range(3):
                    res1 = TomatoOcrTap(231, 562, 485, 609, "登录", match_mode='fuzzy')
                    startupTask.login()
                    sleep(4)
                    功能开关["fighting"] = 0
                    sleep(5)
                break
            tmpMinute = (current_time - start_time)
            tmpDiffMinute = (total_another_minute - (current_time - start_time))
            Toast(f"顶号等待，已等待{tmpMinute}s/剩余等待{tmpDiffMinute}s")
            sleep(2)  # 等待
    else:
        # login()
        print("顶号等待，检查状态正常")

    return


def noticeCancel():
    # print('教程检查')
    re = FindColors.find("328,909,#F6F95C|413,910,#F6F95C|303,1000,#FFFF7B|380,999,#FFFF75", diff=0.9)
    if re:
        Toast('点击教程1')
    if not re:
        re = FindColors.find("298,535,#F2F65A|367,536,#F2F65B|279,842,#F2F65A|356,842,#F2F65A", diff=0.9)
        if re:
            Toast('点击教程2')
    if not re:
        re = FindColors.find("484,1190,#F1FD2A|484,1210,#F0FC21|585,1190,#F0F559|587,1216,#F0FE23", diff=0.9)
        if re:
            Toast('点击教程3')
    if not re:
        re = FindColors.find("324,912,#E7EB58|324,923,#E5EA57|326,847,#EAF075|326,868,#EEF47B|326,792,#EBF17B",
                             diff=0.95)
        if re:
            Toast('点击教程4')
    if not re:
        re = FindColors.find("523,197,#F9FC52|534,198,#FBFD52|561,198,#F9FB50|586,198,#FBFD4E", diff=0.9)
        if re:
            Toast('点击教程5')
    if re:
        print(re.x, re.y)
        tapSleep(re.x + 5, re.y + 5)

    # dailyTask.对话检查()
    return


class L(ShellListener):
    def commandOutput(self, i: int, s: str):
        print('?', s)

    def commandTerminated(self, i: int, s: str):
        pass

    def commandCompleted(self, i: int, i1: int):
        pass
