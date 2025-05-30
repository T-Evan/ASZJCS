# 导包
import time

from .特征库 import *
from .res.ui.ui import 功能开关
from .startUp import StartUp
from .res.ui.ui import 任务记录
from .baseUtils import *
from .daily import DailyTask
from ascript.android.screen import FindColors


class GongHuiTask:
    def __init__(self):
        self.startupTask = StartUp(f"{功能开关['游戏包名']}")
        self.dailyTask = DailyTask()

    # 角色任务聚合
    def gongHuiTask(self):
        if 功能开关["公会总开关"] == 0:
            return

        self.dailyTask.homePage()

        # 公会挂机奖励
        self.公会挂机奖励()

        # 公会捐赠
        self.公会捐赠()
        #
        # 清理背包
        # self.deleteEquip()

    def 公会挂机奖励(self):
        if 功能开关["公会挂机奖励"] == 0 or 任务记录["公会挂机奖励"] == 1:
            return

        Toast('领取公会挂机奖励')
        self.dailyTask.homePage()
        isFind = False
        for k in range(3):
            tapSleep(494, 1231, 1.5)
            isFind, _ = TomatoOcrText(469, 1249, 529, 1277, '公会')
            if isFind:
                break
        if not isFind:
            Toast('未找到公会入口')
            return

        任务记录["公会挂机奖励"] = 1
        Toast('领取挂机奖励')
        tapSleep(609, 964)  # 领取挂机奖励
        tapSleep(495, 1226)  # 点击空白

    def 公会捐赠(self):
        if 功能开关["公会捐赠"] == 0 or 任务记录["公会捐赠"] == 1:
            return

        Toast('开始公会捐赠')
        self.dailyTask.homePage()

        isFind = False
        for k in range(3):
            tapSleep(494, 1231, 1.5)
            isFind, _ = TomatoOcrText(469, 1249, 529, 1277, '公会')
            if isFind:
                break
        if not isFind:
            Toast('未找到公会入口')
            return

        for k in range(6):
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '大厅', 'match_mode': 'fuzzy'}], sleep1=2, x1=9,
                                         y1=577, x2=711, y2=716)
            if re:
                TomatoOcrTap(189, 1084, 282, 1114, '公会捐赠', offsetX=20, offsetY=-10, sleep1=1)
                TomatoOcrTap(302, 920, 418, 954, '免费', match_mode='fuzzy')
                任务记录["公会捐赠"] = 1
                break
            if not re:
                Toast('寻找公会大厅')
                if k < 2:
                    swipe(527, 735, 352, 723)
                else:
                    swipe(352, 723, 527, 735)
        tapSleep(75, 1215)  # 返回
