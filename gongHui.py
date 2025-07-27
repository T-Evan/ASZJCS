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

        # 鸡舍打扫
        self.鸡舍打扫()

        # 公会讨伐
        self.公会讨伐()
        #
        # 清理背包
        # self.deleteEquip()

    def 公会挂机奖励(self):
        if 功能开关["公会挂机奖励"] == 0 or 任务记录["公会挂机奖励"] == 1:
            return

        Toast('领取公会挂机奖励')
        isFind = self.进入公会()
        if not isFind:
            return

        任务记录["公会挂机奖励"] = 1
        Toast('领取挂机奖励')
        tapSleep(609, 964)  # 领取挂机奖励
        tapSleep(495, 1226)  # 点击空白

    def 公会讨伐(self):
        if (功能开关["公会讨伐"] == 0 or 任务记录["公会讨伐"] == 1) and (
                功能开关["公会战"] == 0 or 任务记录["公会战"] == 1):
            return

        Toast('公会-远征之门-开始')
        isFind = self.进入公会()
        if not isFind:
            return

        isFind = False
        for k in range(6):
            re = TomatoOcrFindRangeClick(
                keywords=[{'keyword': '远', 'match_mode': 'fuzzy'}, {'keyword': '征', 'match_mode': 'fuzzy'},
                          {'keyword': '之门', 'match_mode': 'fuzzy'}],
                sleep1=2,
                x1=1,
                y1=877, x2=700, y2=962)
            if re:
                Toast('公会-进入远征之门')
                isFind = True
                break
            if not re:
                Toast('寻找远征之门')
                if k < 2:
                    swipe(527, 735, 352, 723)
                    sleep(2)
                else:
                    swipe(352, 723, 527, 735)
                    sleep(2)
        if not isFind:
            Toast('公会-未找到远征入口')
            return

        if 功能开关["公会战"] == 1:
            re = TomatoOcrTap(31, 326, 179, 391, '公会战', match_mode='fuzzy', offsetX=10, offsetY=10, sleep1=1.2)
            if not re:
                Toast('公会战-未找到讨伐入口')
                任务记录["公会战"] = 1
            if re:
                tmp = TomatoOcrTap(329, 971, 391, 1006, '领取')
                任务记录["公会战"] = 1

            # 领取馈赠奖励
            re = CompareColors.compare("684,1191,#E15252|693,1191,#D84747")  # 匹配馈赠红点
            if re:
                Toast('公会讨伐-馈赠领取')
                self.dailyTask.馈赠领取()
            tapSleep(77, 1213, 1.5)  # 返回公会战首页

        if 功能开关["公会讨伐"] == 1:
            re = TomatoOcrTap(31, 607, 223, 670, '讨伐', match_mode='fuzzy')
            if not re:
                Toast('公会讨伐-未找到讨伐入口')
                任务记录["公会讨伐"] = 1

            if re:
                # 领取讨伐奖励
                re = CompareColors.compare("386,702,#E15353|402,699,#E05252")
                if re:
                    Toast('公会讨伐-领取讨伐奖励')
                    tapSleep(351, 738)  # 领取奖励
                    tapSleep(59, 981)  # 点击空白

                # 领取馈赠奖励
                re = CompareColors.compare("684,1191,#E15252|693,1191,#D84747")  # 匹配馈赠红点
                if re:
                    Toast('公会讨伐-馈赠领取')
                    self.dailyTask.馈赠领取()

                # 开始讨伐
                re = TomatoOcrTap(214, 1201, 275, 1235, '讨伐')
                if re:
                    for k in range(2):
                        re = CompareColors.compare(
                            "421,44,#CBCF60|418,49,#CBCF5F|422,58,#CCD060|426,51,#CBD05F|416,45,#212121")
                        if re:
                            Toast('公会讨伐-讨伐次数用尽')
                            break
                        re = TomatoOcrTap(330, 966, 389, 1001, '挑战', sleep1=3)
                        if re:
                            Toast('公会讨伐-开始讨伐')
                            self.dailyTask.战斗检查()

        tapSleep(67, 1215)  # 点击返回
        tapSleep(67, 1215)
        tapSleep(67, 1215)
        任务记录["公会讨伐"] = 1

    def 鸡舍打扫(self):
        if 功能开关["鸡舍打扫"] == 0 or 任务记录["鸡舍打扫"] == 1:
            return

        Toast('公会-鸡舍打扫-开始')
        isFind = self.进入公会()
        if not isFind:
            return

        isFind = False
        for k in range(6):
            re = TomatoOcrFindRangeClick(
                keywords=[{'keyword': '鸡', 'match_mode': 'fuzzy'}, {'keyword': '舍', 'match_mode': 'fuzzy'}], sleep1=2,
                x1=6,
                y1=885, x2=711, y2=930)
            if re:
                Toast('公会-进入鸡舍')
                isFind = True
                break
            if not re:
                Toast('寻找公会鸡舍')
                if k < 2:
                    swipe(527, 735, 352, 723)
                    sleep(2)
                else:
                    swipe(352, 723, 527, 735)
                    sleep(2)

        if not isFind:
            Toast('公会鸡舍-未找到活动入口')
            任务记录["鸡舍打扫"] = 1
            return

        if 功能开关['鸡舍打扫'] == 1:
            for k in range(20):
                re = TomatoOcrTap(302, 1065, 421, 1100, '开始打扫', sleep1=2)
                if re:
                    Toast('公会-开始打扫鸡舍')
                re = FindColors.find("285,204,#EDAB5B|288,206,#F09B43|287,201,#F0A949", rect=[80, 148, 648, 939],
                                     diff=0.9)
                if re:
                    Toast('公会-鸡舍打扫')
                    tapSleep(re.x, re.y, 1.5)
                    tapSleep(365, 1144)  # 点击空白
                    sleep(1)
        任务记录["鸡舍打扫"] = 1
        if 功能开关['饲养鸡仔'] == 1:
            for k in range(5):
                noCt, _ = TomatoOcrText(298, 754, 424, 787, '前往获取')
                if not noCt:
                    TomatoOcrTap(328, 1065, 389, 1098, '饲养')
                re = TomatoOcrTap(302, 1065, 421, 1100, '开始饲养', sleep1=2)
                if re or noCt:
                    Toast('公会-饲养鸡仔')
                    noCt, _ = TomatoOcrText(298, 754, 424, 787, '前往获取')
                    if noCt:
                        if 功能开关['购买鸡仔'] == 0:
                            Toast('无可饲养鸡仔')
                        else:
                            Toast('准备购买鸡仔')
                            re = TomatoOcrTap(298, 754, 424, 787, '前往获取', sleep1=2)  # 进入商店
                            if re:
                                isFind = False
                                for m in range(2):
                                    isFind = FindColors.find(
                                        "129,869,#969298|124,881,#969298|112,897,#928D95|118,883,#E4C094",
                                        rect=[20, 181, 692, 1160], diff=0.95)  # 鸡仔
                                    if isFind and isFind.y + 130 < 1182:
                                        Toast('公会-购买鸡仔')
                                        tapSleep(isFind.x, isFind.y + 130)  # 购买按钮
                                    isFind = FindColors.find(
                                        "126,536,#B95C5C|134,530,#BD5D5D|120,598,#B99B74|129,593,#B89A74", diff=0.94)
                                    if isFind and isFind.y + 150 < 1182:
                                        Toast('公会-购买鸡仔')
                                        tapSleep(isFind.x, isFind.y + 150)  # 购买按钮
                                    swipe(355, 639, 334, 377)
                                    swipe(355, 639, 355, 619)
                                    sleep(2)

                                if not isFind:
                                    Toast('公会-无可购买鸡仔')
                                tapSleep(75, 1215)  # 返回
                    noCt, _ = TomatoOcrText(298, 754, 424, 787, '前往获取')
                    if not noCt:
                        Toast('公会-开始饲养鸡仔')
                        TomatoOcrTap(328, 1065, 389, 1098, '饲养')
                    else:
                        Toast('公会-无可饲养鸡仔')
        tapSleep(75, 1215)  # 返回
        tapSleep(75, 1215)  # 返回

    def 公会捐赠(self):
        if 功能开关["公会捐赠"] == 0 or 任务记录["公会捐赠"] == 1:
            return

        Toast('开始公会捐赠')

        isFind = self.进入公会()
        if not isFind:
            return

        isFind = False
        for k in range(6):
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '大厅', 'match_mode': 'fuzzy'}], sleep1=2, x1=9,
                                         y1=577, x2=711, y2=716)
            if re:
                isFind = True
                TomatoOcrTap(189, 1084, 282, 1114, '公会捐赠', offsetX=20, offsetY=-10, sleep1=1)
                TomatoOcrTap(302, 920, 418, 954, '免费', match_mode='fuzzy')
                任务记录["公会捐赠"] = 1
                break
            if not re:
                Toast('寻找公会大厅')
                if k < 2:
                    swipe(527, 735, 352, 723)
                    sleep(2)
                else:
                    swipe(352, 723, 527, 735)
                    sleep(2)
        if not isFind:
            Toast('公会鸡舍-未找到活动入口')
            任务记录["公会捐赠"] = 1
            return
        tapSleep(75, 1215)  # 返回
        tapSleep(75, 1215)  # 返回

    def 进入公会(self):
        isFind, _ = TomatoOcrText(469, 1249, 529, 1277, '公会')
        if not isFind:
            self.dailyTask.homePage()
            for k in range(3):
                tapSleep(494, 1231, 1.5)
                isFind, _ = TomatoOcrText(469, 1249, 529, 1277, '公会')
                if isFind:
                    break
        if not isFind:
            Toast('未找到公会入口')
        return isFind
