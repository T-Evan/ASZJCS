# 导包
import time

from .特征库 import *
from .res.ui.ui import 功能开关
from .startUp import StartUp
from .res.ui.ui import 任务记录
from .baseUtils import *
from .daily import DailyTask
from ascript.android.screen import FindColors


class JueSeTask:
    def __init__(self):
        self.startupTask = StartUp(f"{功能开关['游戏包名']}")
        self.dailyTask = DailyTask()

    # 角色任务聚合
    def jueSeTask(self):
        if 功能开关["日常总开关"] == 0:
            return

        self.dailyTask.homePage()

        # 更换装备
        self.更换装备()
        #
        # 清理背包
        # self.deleteEquip()

    def 更换装备(self):
        if 功能开关["自动更换装备"] == 0 and 功能开关["自动强化装备"] == 0:
            return

        if 任务记录["强化装备-倒计时"] > 0:
            diffTime = time.time() - 任务记录["强化装备-倒计时"]
            if diffTime < 3 * 60:
                Toast(f'强化装备-倒计时{round((3 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        任务记录["强化装备-倒计时"] = time.time()
        Toast('开始检测装备')
        self.dailyTask.homePage()

        isFind = False
        for k in range(3):
            tapSleep(74, 1238, 1.5)
            isFind, _ = TomatoOcrText(44, 1250, 112, 1276, '角色')
            if isFind:
                break
        if not isFind:
            Toast('未找到角色入口')
            return

        if 功能开关["自动更换装备"] == 1:
            waitAll = FindColors.find_all("129,375,#E15151|134,372,#FFFFFF|139,373,#E25252",
                                          rect=[14, 279, 715, 715])  # 红色感叹号（替换）
            if waitAll:
                for wait in waitAll:
                    Toast('开始替换装备')
                    tapSleep(wait.x, wait.y)
                    re = CompareColors.compare("347,861,#E25252|336,860,#E35353")  # 替换 红点
                    if re:
                        TomatoOcrTap(191, 861, 268, 901, '替换')
                        re = FindColors.find("197,303,#F2FF79|197,311,#EEFF77", diff=0.95)
                        if re:
                            Toast('更换装备成功')
                            tapSleep(re.x, re.y, 1.5)
                            TomatoOcrFindRangeClick('更换', x1=14, y1=340, x2=702, y2=943)
                    else:
                        re = CompareColors.compare("595,860,#E35353|607,861,#E25252")
                        if re:
                            Toast('领取馈赠')
                            TomatoOcrTap(456, 863, 525, 902, '培养')
                            if re:
                                TomatoOcrTap(579, 1204, 641, 1235, '馈赠')
                                TomatoOcrTap(562, 206, 612, 233, '领取', sleep1=2)
                                Toast('返回角色页继续')
                                tapSleep(606, 1221)
                                tapSleep(72, 1226)
                                tapSleep(72, 1226)
                        else:
                            Toast('无可替换装备')
                            tapSleep(367, 99)  # 点击空白

        if 功能开关["自动强化装备"] == 1:
            waitAll = FindColors.find_all("127,375,#40A3D4|132,371,#FFFFFF|138,370,#D9E8F4", rect=[12, 271, 705, 707],
                                          diff=0.95)  # 蓝色感叹号（强化）
            if waitAll:
                for wait in waitAll:
                    Toast('开始强化装备')
                    tapSleep(wait.x, wait.y)
                    re = CompareColors.compare("593,858,#43A1D7|606,860,#4DA6D6")  # 培养 蓝点
                    if re:
                        TomatoOcrTap(456, 863, 525, 902, '培养')
                        for k in range(5):
                            Toast('强化装备成功')
                            TomatoOcrTap(324, 1065, 393, 1103, '强化')
                            re = CompareColors.compare("492,1063,#42A2D6|508,1063,#66BFEB")
                            if not re:
                                Toast('强化装备完成')
                                tapSleep(72, 1226)
                                tapSleep(72, 1226)
                                break
