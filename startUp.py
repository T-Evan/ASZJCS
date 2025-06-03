# 导包
from ascript.android import system
from six import print_
from ascript.android.system import ShellListener

from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .res.ui.ui import switch_lock
from .baseUtils import *
import shutil
import os
import sys
from ascript.android import system
from ascript.android.screen import FindColors
import sys
import traceback
from ascript.android.system import Device


class StartUp:
    # 构造器
    def __init__(self, app_name):
        self.app_name = app_name

    # 实例方法
    def start_app(self):
        global 功能开关
        # r = system.shell(f"start -n com.xd.cfbmf")
        tryTimes = 0

        max_attempt = 35

        display = Device.display()
        # 屏幕宽度
        if display.widthPixels != 720 or display.heightPixels != 1280:
            Toast(f'分辨率为 {display.widthPixels} * {display.heightPixels}，请检查分辨率是否正确')
            Dialog.confirm("屏幕分辨率不为 720 * 1280，请重新设置", "分辨率错误")
            r = system.shell(f"wm size 720x1280", L())
            r = system.shell(f"wm density 320", L())
            display = Device.display()
            if display.widthPixels != 720 or display.heightPixels != 1280:
                Dialog.confirm("屏幕分辨率已设置为 720 * 1280", "分辨率已调整")

        for attempt in range(max_attempt):
            tryTimes = tryTimes + 1

            system.open(self.app_name)

            # 判断是否已在首页
            shou_ye1 = self.返回首页()
            if shou_ye1:
                return True

            # 识别是否进入登录页
            login1, _ = TomatoOcrText(618, 77, 693, 108, "服务器")  # 首页服务器选择
            if login1:
                Toast('准备进入游戏')
                self.login()
            else:
                re, _ = TomatoOcrText(317, 72, 401, 118, '公告')
                if re:
                    Toast('关闭公告页')
                    tapSleep(334, 1237)  # 点击空白处，关闭登录页公告
                    tapSleep(334, 1237)  # 点击空白处

            # 判断是否已在首页
            shou_ye1 = self.返回首页()
            if not shou_ye1:
                # 不在首页，尝试开始返回首页
                # 开始异步处理返回首页
                功能开关["needHome"] = 1
                功能开关["fighting"] = 0
                Toast('正在返回首页')
                tapSleep(52, 1229)
                TomatoOcrTap(457, 721, 525, 754, '确定', sleep1=1.5)
                # tapSleepV2(52, 1229)
            Toast(f'启动游戏，等待加载中，{attempt}/{max_attempt}')

            sleep(1)  # 等待游戏启动
        print('启动游戏失败，尝试重启游戏')
        # 结束应用
        r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
        # 重启游戏
        return self.start_app()

    def 返回首页(self):
        # 判断是否已在首页
        shou_ye1 = CompareColors.compare(
            "320,1221,#DADE71|369,1218,#746661|356,1169,#FEDCE3|403,1223,#CDD068")  # 判断底部家园图标（已点亮）
        if not shou_ye1:
            re = CompareColors.compare("353,1186,#FFD1DA|361,1204,#AC8B7B|358,1251,#756361")  # 匹配底部家园图标(未点亮)
            if re:
                Toast('返回首页')
                tapSleep(358, 1223, 1)
                shou_ye1 = CompareColors.compare(
                    "320,1221,#DADE71|369,1218,#746661|356,1169,#FEDCE3|403,1223,#CDD068")  # 判断底部家园图标（已点亮）
        if shou_ye1:
            Toast('已进入游戏')
            功能开关["needHome"] = 0
            return True
        return False

    def login(self):
        sleep(0.5)
        login1 = False
        login1, _ = TomatoOcrText(618, 77, 693, 108, "服务器")  # 首页服务器选择

        if not login1:
            return self.start_app()

        for i in range(2):
            login1, _ = TomatoOcrText(618, 77, 693, 108, "服务器")  # 首页服务器选择
            if login1:
                Toast(f'等待进入游戏')
                tapSleep(345, 1052, 2)

        shou_ye = False
        for loopCount in range(4):
            shou_ye1, _ = TomatoOcrText(333, 1249, 386, 1276, '家园')
            if shou_ye1:
                Toast('已进入游戏')
                shou_ye = True
                sleep(0.5)  # 等待 3 秒
            tapSleep(682, 17)  # 点击空白处

        # if not shou_ye:
        #     return self.start_app()

        return shou_ye


class L(ShellListener):
    def commandOutput(self, i: int, s: str):
        print('?', s)

    def commandTerminated(self, i: int, s: str):
        pass

    def commandCompleted(self, i: int, i1: int):
        pass
