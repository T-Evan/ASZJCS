# 导包
import time

from PIL.ImageChops import offset
from ascript.android.system import ShellListener

from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .startUp import StartUp
from .res.ui.ui import 任务记录
from .baseUtils import *
from ascript.android import action
from .res.ui.ui import switch_lock
import re as rePattern
from ascript.android.screen import FindColors
from ascript.android.action import Path
from ascript.android import system
import sys
import traceback


class DailyTask:
    def __init__(self):
        self.startupTask = StartUp(f"{功能开关['游戏包名']}")

    def homePage(self, needQuitTeam=False):
        tryTimes = 0
        while True:
            tryTimes = tryTimes + 1

            if tryTimes > 5:
                self.对话检查()
                system.open(f"{功能开关['游戏包名']}")

            if tryTimes > 10:
                login1, _ = TomatoOcrText(618, 77, 693, 108, "服务器")  # 首页服务器选择
                if login1:
                    return self.startupTask.start_app()

            if tryTimes > 18:
                Toast(f'尝试返回游戏,{tryTimes}/20')
                system.open(f"{功能开关['游戏包名']}")

            if tryTimes > 23:
                return

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
                功能开关["needHome"] = 0
                Toast('日常 - 已返回首页')
                return True

            功能开关["needHome"] = 1
            Toast('正在返回首页')
            tapSleepV2(52, 1229)
            # tapSleepV2(52, 1229)
            sleep(0.5)

    # 日常任务聚合
    def dailyTask(self):
        if 功能开关["日常总开关"] == 0:
            return

        self.homePage()

        # 日常相关

        # 小推车领取
        self.小推车领取()

        # 小木床领取
        self.小木床领取()

        # 每日签到
        self.每日签到()

        # 成长试炼
        self.成长试炼()

        # 启程签到
        self.启程签到()

        # 菜就多躺
        self.菜就多躺()

        # 巡礼之证
        self.巡礼之证()

        # 其他签到活动
        self.其他签到活动()

        # 月卡领取
        self.月卡领取()

        # 每日商店
        self.每日商店()

        # 邮件领取
        self.邮件领取()

        # 幻想阶梯
        self.幻想阶梯()

        # 自动主线
        self.自动主线()

        # 领取每日奖励
        self.日常任务()

        # 开启装备宝箱
        # self.openTreasure()

        # 更换装备
        # self.updateEquip()
        #
        # 清理背包
        # self.deleteEquip()

    def 幻想阶梯(self):
        if 功能开关["幻想阶梯"] == 0:
            return
        self.homePage()
        Toast('日常-幻想阶梯挑战')

        re = TomatoOcrFindRangeClick(
            keywords=[{'keyword': '层', 'match_mode': 'fuzzy'}, {'keyword': '完成', 'match_mode': 'fuzzy'}], x1=18,
            y1=770, x2=267, y2=1030)
        if re:
            Toast('日常-幻想阶梯-挑战完成领取')
            tapSleep(356, 1207)  # 点击返回
            tapSleep(356, 1207)

        tapSleep(219, 1231)  # 点击笔记
        re, _ = TomatoOcrText(191, 1249, 246, 1276, '笔记')
        if not re:
            Toast('日常-未找到笔记入口')
            return
        re = TomatoOcrTap(427, 123, 595, 176, '幻想阶梯')
        if re:
            Toast('日常-进入幻想阶梯')
            re = FindColors.find("561,176,#D44545|564,176,#FFFFFF|567,176,#CA4949", diff=0.95)
            if re:
                tapSleep(re.x, re.y, 1.5)
                re = FindColors.find("561,176,#D44545|564,176,#FFFFFF|567,176,#CA4949", rect=[6, 113, 704, 1150],
                                     diff=0.95)
                if re:
                    Toast('日常-幻想阶梯-开始挑战')
                    tapSleep(re.x, re.y, 2.5)
                    self.战斗检查()
                else:
                    Toast('日常-幻想阶梯-未达到推荐战力')
            tapSleep(77, 1212)
            tapSleep(77, 1212)

    def 邮件领取(self):
        if 功能开关["邮件领取"] == 0 or 任务记录["邮件领取"] == 1:
            return
        self.homePage()
        Toast('日常-检查邮件领取')
        for k in range(8):
            re = FindColors.find("430,609,#896751|407,609,#8D6C52|449,607,#B18154|427,472,#80534B",
                                 rect=[14, 435, 696, 697], diff=0.95)
            if not re:
                re = FindColors.find("303,606,#3E2C20|281,607,#392A1D|326,609,#443022|309,465,#6E3535|377,606,#294730",
                                     rect=[4, 399, 702, 823], diff=0.93)
            if re:
                Toast('日常-领取邮件')
                print(re.x, re.y)
                tapSleep(re.x, re.y - 40, 1.5)
                re = TomatoOcrTap(438, 1014, 562, 1054, '全部领取')
                任务记录["邮件领取"] = 1
                tapSleep(348, 1224)  # 返回首页
                tapSleep(348, 1224)
                break
            if k < 4:
                swipe(487, 729, 197, 759)
                sleep(2)
            else:
                swipe(197, 759, 487, 729)
                sleep(2)

    def 每日商店(self):
        if 功能开关["每日商店"] == 0 or 任务记录["每日商店"] == 1:
            return
        self.homePage()
        Toast('日常-检查每日商店')
        for k in range(8):
            re = FindColors.find("377,763,#2E4C31|445,768,#365026|371,857,#574126|411,861,#446E6D|467,860,#7D623A",
                                 rect=[7, 396, 699, 1043], diff=0.95)  # 夜间每日商店
            if not re:
                re = FindColors.find("432,821,#4B3F32|468,832,#707085|507,831,#6C6C82|462,858,#43ABDF|455,783,#469572",
                                     rect=[3, 476, 705, 1049], diff=0.93, ori=5)  # 白天每日商店
            if not re:
                re = FindColors.find("498,861,#4E4132|549,864,#5191AD|590,872,#8E735F|544,768,#5C915C",
                                     rect=[4, 498, 702, 1040], diff=0.95, ori=5)  # 凌晨每日商店
            if re:
                Toast('家园-每日商店')
                tapSleep(re.x, re.y - 40, 1.5)
                for j in range(5):
                    re = FindColors.find("40,185,#F9C562|40,224,#FCDE7D|45,214,#FBDA78", rect=[11, 164, 691, 735],
                                         diff=0.95)  # 折扣标识(仅前两排，不考虑九折)
                    if re:
                        Toast('每日商店-折扣商品购买')
                        tapSleep(re.x + 100, re.y + 220, 1)  # 购买按钮

                re = CompareColors.compare("503,1193,#E35353|514,1193,#E25252")  # 宝库红点
                if re:
                    Toast('每日商店-宝库')
                    tapSleep(427, 1221, 1)
                    TomatoOcrTap(98, 392, 162, 425, '免费')

                任务记录["每日商店"] = 1
                tapSleep(348, 1224)  # 返回首页
                break
            if k < 4:
                Toast('寻找每日商店')
                swipe(487, 729, 197, 759)
                sleep(1.6)
            else:
                Toast('寻找每日商店')
                swipe(197, 759, 487, 729)
                sleep(1.6)

    def 其他签到活动(self):
        if 功能开关["其他签到活动"] == 0 or 任务记录["其他签到活动"] == 1:
            return
        self.homePage()

        Toast('日常-其他签到活动')
        tapSleep(656, 1006, 1.5)
        re = TomatoOcrTap(570, 827, 656, 875, '商城', sleep1=0.8)
        if not re:
            Toast('未找到商城入口')
            return
        if 任务记录["启程好礼"] == 0:
            Toast('商城-启程好礼')
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '启程好礼', 'match_mode': 'fuzzy'}], sleep1=2, x1=7,
                                         y1=107,
                                         x2=699, y2=1144)
            if re:
                tapSleep(72, 284)  # 领取启程福利
                任务记录["启程好礼"] = 1
                tapSleep(71, 1215)  # 返回商城页

        if 任务记录["幻想学院"] == 0:
            Toast('商城-幻想学院')
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '幻想学院', 'match_mode': 'fuzzy'}], sleep1=2, x1=7,
                                         y1=107,
                                         x2=699, y2=1144)
            if re:
                tapSleep(80, 738)  # 领取启程福利
                任务记录["幻想学院"] = 1
                tapSleep(71, 1215)  # 返回商城页

        if 任务记录["魔法文具"] == 0:
            Toast('商城-魔法文具')
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '魔法文具', 'match_mode': 'fuzzy'}], sleep1=2, x1=7,
                                         y1=107,
                                         x2=699, y2=1144)
            if re:
                tapSleep(80, 738)  # 领取启程福利
                任务记录["魔法文具"] = 1
                tapSleep(71, 1215)  # 返回商城页

    def 月卡领取(self):
        if 功能开关["月卡领取"] == 0 or 任务记录["月卡领取"] == 1:
            return
        self.homePage()
        Toast('日常-月卡领取')
        tapSleep(656, 1006, 1.5)
        re = TomatoOcrTap(570, 827, 656, 875, '商城', sleep1=0.8)
        if not re:
            Toast('未找到商城入口')
            return
        re = TomatoOcrTap(394, 1224, 461, 1259, '月卡')
        if not re:
            Toast('未找到月卡入口')
            return
        re, _ = TomatoOcrText(514, 516, 582, 550, '元', match_mode='fuzzy')
        if not re:
            tapSleep(538, 527)  # 领取
            tapSleep(421, 1237)  # 空白

        re, _ = TomatoOcrText(513, 1004, 579, 1036, '元', match_mode='fuzzy')
        if not re:
            tapSleep(536, 1018)  # 领取
            tapSleep(421, 1237)  # 空白
        tapSleep(64, 1207)  # 空白
        tapSleep(64, 1207)  # 空白

    def 巡礼之证(self):
        if 功能开关["巡礼之证"] == 0 or 任务记录["巡礼之证"] == 1:
            return
        self.homePage()
        Toast('日常-巡礼之证')
        tapSleep(656, 1006, 1.5)
        re = TomatoOcrTap(570, 827, 656, 875, '商城', sleep1=0.8)
        if not re:
            Toast('未找到商城入口')
            return
        re = TomatoOcrFindRangeClick(keywords=[{'keyword': '巡礼之证', 'match_mode': 'fuzzy'}], sleep1=2, x1=7, y1=107,
                                     x2=699, y2=1144)
        if re:
            re = CompareColors.compare("685,1194,#DE4E4E|694,1193,#E35353")
            if re:
                Toast('巡礼之证-检查巡礼目标')
                tapSleep(558, 1216, 1)  # 点击任务
                for k in range(4):
                    re = FindColors.find("200,1091,#E45454|213,1092,#E25252", rect=[42, 1079, 682, 1145], diff=0.95)
                    if re:
                        Toast('巡礼之证-领取巡礼目标')
                        tapSleep(re.x, re.y, 0.8)
                        TomatoOcrTap(546, 415, 609, 449, '领取')
            re = TomatoOcrTap(238, 1199, 345, 1236, '巡礼之证')  # 点击巡礼之证
            if re:
                Toast('巡礼之证-检查指引赐福')
                re = FindColors.find("200,1091,#E45454|213,1092,#E25252", rect=[34, 350, 688, 1043], diff=0.97)
                if re:
                    Toast('巡礼之证-领取指引赐福')
                    tapSleep(re.x, re.y)

            任务记录["巡礼之证"] = 1
        tapSleep(74, 1204)  # 返回
        tapSleep(74, 1204)

    def 菜就多躺(self):
        if 功能开关["菜就多躺"] == 0 or 任务记录["菜就多躺"] == 1:
            return
        self.homePage()
        Toast('日常-菜就多躺')
        re = TomatoOcrTap(615, 176, 696, 200, '精彩活动')
        if re:
            re = TomatoOcrFindRangeClick(
                keywords=[{'keyword': '菜就', 'match_mode': 'fuzzy'}, {'keyword': '多躺', 'match_mode': 'fuzzy'}],
                sleep1=2, x1=15,
                y1=91, x2=699, y2=1172)
            re = TomatoOcrTap(530, 1014, 671, 1047, '白菜狗商店')
            if re:
                Toast('白菜狗商店-领取免费狗币')
                for k in range(5):
                    re = TomatoOcrTap(100, 558, 165, 590, '免费')
                    re = CompareColors.compare("224,358,#D84949|232,356,#E04E4E")  # 免费红点
                    if not re:
                        break
                    tapSleep(290, 1213)  # 点击空白
                    tapSleep(290, 1213)  # 点击空白

                re = CompareColors.compare("688,1194,#E15151|699,1197,#E65555|697,1196,#E35353")
                if re:
                    Toast('白菜狗商店-领取每日委托')
                    tapSleep(571, 1212)
                    for k in range(5):
                        re = TomatoOcrTap(566, 392, 626, 426, '领取')
                        if not re:
                            break
                        tapSleep(582, 1224)  # 点击空白
                        tapSleep(582, 1224)  # 点击空白

                任务记录["菜就多躺"] = 1

            tapSleep(77, 1212)  # 点击返回
            tapSleep(77, 1212)

    def 启程签到(self):
        if 功能开关["启程签到"] == 0 or 任务记录["启程签到"] == 1:
            return
        self.homePage()
        Toast('日常-启程签到')
        re = TomatoOcrTap(615, 176, 696, 200, '精彩活动')
        if re:
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '启程签到', 'match_mode': 'fuzzy'}], sleep1=2, x1=15,
                                         y1=91, x2=699, y2=1172)
            re = FindColors.find("156,336,#DB5050|161,339,#FFFFFF|165,342,#D44444", rect=[7, 181, 701, 1047], diff=0.95)
            if re:
                tapSleep(re.x, re.y, 1.5)
            任务记录["启程签到"] = 1
            tapSleep(77, 1212)  # 点击返回
            tapSleep(77, 1212)

    def 成长试炼(self):
        if 功能开关["成长试炼"] == 0 or 任务记录["成长试炼"] == 1:
            return
        self.homePage()
        Toast('日常-成长试炼')
        re = TomatoOcrTap(615, 176, 696, 200, '精彩活动')
        if re:
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '成长试炼', 'match_mode': 'fuzzy'}], sleep1=2, x1=15,
                                         y1=91, x2=699, y2=1172)
            for k in range(5):
                re = FindColors.find("122,463,#E35353|135,462,#E25252", rect=[33, 445, 686, 500], diff=0.95)
                if re:
                    tapSleep(re.x, re.y)
                re = TomatoOcrTap(568, 610, 631, 644, '领取')
                if not re:
                    Toast('日常-成长试炼完成')
                    break
                tapSleep(341, 1234)  # 点击空白
            任务记录["成长试炼"] = 1
            tapSleep(77, 1212)  # 点击返回
            tapSleep(77, 1212)

    def 每日签到(self):
        if 功能开关["每日签到"] == 0 or 任务记录["每日签到"] == 1:
            return
        self.homePage()
        Toast('日常-每日签到')
        re = TomatoOcrTap(615, 176, 696, 200, '精彩活动')
        if re:
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '每日签到', 'match_mode': 'fuzzy'}], sleep1=2, x1=15,
                                         y1=91, x2=699, y2=1172)
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '领取', 'match_mode': 'fuzzy'}], sleep1=2, x1=15,
                                         y1=91, x2=699, y2=1172)
            if re:
                Toast('日常-每日签到完成')
                tapSleep(328, 1229)
            任务记录["每日签到"] = 1
            tapSleep(77, 1212)
            tapSleep(77, 1212)

    def 小木床领取(self):
        if 功能开关["小木床领取"] == 0:
            return

        if 任务记录["小木床-倒计时"] > 0:
            diffTime = time.time() - 任务记录["小木床-倒计时"]
            if diffTime < 3 * 60:
                Toast(f'小木床-倒计时{round((3 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        任务记录["小木床-倒计时"] = time.time()

        self.homePage()
        Toast('日常-检查小木床领取')
        re = FindColors.find("664,612,#3C7CCB|678,612,#619AC9|663,623,#2772A9|677,625,#9CCDE0",
                             rect=[4, 399, 702, 823], diff=0.9)
        if not re:
            re = FindColors.find("663,618,#4485D1|669,619,#699EDD|675,618,#518AC4|661,630,#1F629D|673,632,#4CA5C3",
                                 rect=[20, 345, 699, 877], diff=0.95)
        if re:
            Toast('日常-前往小木床')
            tapSleep(re.x, re.y, 1.5)
            re = FindColors.find("664,612,#3C7CCB|678,612,#619AC9|663,623,#2772A9|677,625,#9CCDE0",
                                 rect=[4, 399, 702, 823], diff=0.9)
            if re:
                Toast('日常-领取小木床')
                tapSleep(re.x, re.y, 1.5)

            tapSleep(440, 615, 2)  # 点击小木床
            re = TomatoOcrTap(274, 943, 447, 980, '免费', match_mode='fuzzy', sleep1=3)
            if re:
                Toast('小木床-今日免费加速')
                tapSleep(355, 1210)
                tapSleep(355, 1210)

    def 小推车领取(self):
        if 功能开关["小推车领取"] == 0:
            return

        if 任务记录["小推车-倒计时"] > 0:
            diffTime = time.time() - 任务记录["小推车-倒计时"]
            if diffTime < 3 * 60:
                Toast(f'小推车-倒计时{round((3 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        任务记录["小推车-倒计时"] = time.time()

        self.homePage()
        Toast('日常-检查小推车领取')
        re = FindColors.find("43,724,#B27C1E|48,713,#F3D373|54,719,#835520|46,731,#C2A77D|54,727,#FBF490",
                             rect=[6, 340, 701, 961], diff=0.9)
        if not re:
            re = FindColors.find("45,699,#FBD06F|47,692,#F4D478|53,697,#D7AD66|40,710,#A3845C|55,708,#F7EF8A",
                                 rect=[4, 399, 702, 823], diff=0.9)
        if not re:
            FindColors.find("47,686,#F2CC59|37,699,#975B43|53,700,#FDF999", rect=[3, 336, 704, 1041], diff=0.95)
        if re:
            Toast('日常-前往小推车')
            tapSleep(re.x, re.y, 1.5)

        for k in range(4):
            re = FindColors.find("45,699,#FBD06F|47,692,#F4D478|53,697,#D7AD66|40,710,#A3845C|55,708,#F7EF8A",
                                 rect=[4, 399, 702, 823], diff=0.9)
            if not re:
                re = FindColors.find("180,763,#FBCB77|175,778,#DFBB6F|162,781,#C4A47F|187,776,#FBE58B",
                                     rect=[4, 399, 702, 823], diff=0.9)
            if not re:
                re = FindColors.find("336,767,#D4D272|348,767,#B28157|347,778,#6D463F|364,779,#FBE68B",
                                     rect=[11, 484, 697, 958], diff=0.9)  # 夜间推车

            if re:
                Toast('日常-领取小推车')
                tapSleep(re.x, re.y, 2)
                tapSleep(347, 108)  # 点击空白处
                break

        # 检测小推车升级
        re = FindColors.find("408,840,#4BA5D5|415,840,#FEFEFE|419,841,#4AA5D5", rect=[195, 696, 508, 956], diff=0.95,
                             ori=5)
        if re:
            tapSleep(re.x, re.y, 2)
            Toast('日常-小推车升级')
            for k in range(10):
                re = FindColors.find("408,840,#4BA5D5|415,840,#FEFEFE|419,841,#4AA5D5", rect=[574, 351, 678, 1096],
                                     diff=0.95, ori=5)  # 匹配可升级标记
                if re:
                    tapSleep(re.x, re.y, 1.5)
                    for m in range(10):
                        re = CompareColors.compare("527,1077,#42A3D3|543,1079,#43A2D4")  # 匹配可升级标记
                        if re:
                            tapSleep(re.x, re.y)
                        sleep(0.1)
                    tapSleep(60, 1212)  # 点击返回
            tapSleep(356, 1220)  # 返回家园

    def 自动主线(self):
        if 功能开关["自动主线"] == 0:
            return

        Toast('检查主线任务')
        self.homePage()
        # 领取任务奖励
        re = FindColors.find("322,903,#E45151|333,904,#E35353|328,901,#FFFFFF|328,896,#FFFFFF",
                             rect=[20, 703, 347, 1038], diff=0.95, ori=5)  # 匹配红色感叹号
        if re:
            Toast('领取主线任务奖励')
            tapSleep(re.x - 30, re.y + 50)  # 点击奖励图标

        # 主线探索
        re = FindColors.find(
            "271,993,#B2B655|277,998,#B2B655|272,1007,#B1B655|268,1001,#222322|286,1002,#222322|278,1013,#222322|269,1017,#222322",
            rect=[6, 726, 311, 1041], diff=0.9, ori=5)
        if re:
            _, taskName = TomatoOcrText(20, 997, 241, 1030, '任务名称')
            Toast(f'主线任务开始-{taskName}')
            tapSleep(re.x - 10, re.y + 30)  # 点击前往探索
            re = TomatoOcrTap(459, 718, 525, 756, '确定')
            if re:
                self.地图探索()

    def 地图探索(self):
        Toast('等待进入探索地图')
        for i in range(3):
            self.对话检查()
            re = CompareColors.compare("63,140,#CCCF68|56,149,#212121|60,167,#D3D387|41,162,#CCCF68")  # 匹配探索地图左上队伍图标
            if re:
                break
            sleep(0.5)

        Toast('已进入探索地图')

        lastPoint = [0, 0]
        lastPointTimes = 0
        for k in range(30):
            self.世界聊天检查()

            re = CompareColors.compare(
                "257,1011,#222323|252,1016,#4F4F4F|252,1027,#232323|257,1029,#232323|253,1038,#222222", diff=0.8)
            if re:
                Toast('开启探索定位')
                tapSleep(252, 1008)

            re = FindColors.find(
                "396,889,#EDEDE5|398,914,#CBCF60|384,905,#222222|413,906,#222222|409,929,#222222|380,929,#212121|396,926,#CACE60",
                rect=[3, 197, 705, 1275], diff=0.93)  # 匹配地图的定位标记
            if not re:
                re = FindColors.find("48,1136,#8EA5D3|44,1147,#81A4D8|52,1145,#65C7D5|66,1149,#BBBDCD",
                                     rect=[8, 115, 692, 1271], diff=0.95)
                if re:
                    Toast('寻路关卡')
            if not re:
                re = FindColors.find("40,777,#E2E2E2|47,783,#9BECF8|55,796,#CECECE|61,793,#7F6E44|64,783,#E2E2E2",
                                     rect=[3, 176, 701, 1259], diff=0.9)  # 女神像
                if re:
                    Toast('寻路神像')
            if not re:
                re = FindColors.find("50,522,#9BA18F|52,531,#9AA4A0|39,544,#818C83|53,544,#ACB5AC",
                                     rect=[6, 116, 716, 1255], diff=0.96)  # 女神像
                if re:
                    Toast('寻路神像')
            if not re:
                re = FindColors.find("431,503,#E35353|436,499,#FEFEFE|438,499,#D27272|434,508,#D96161",
                                     rect=[4, 115, 705, 973], diff=0.93)  # 任务红点
                if re:
                    Toast('寻路任务提交')

            if not re:
                lastPointTimes = lastPointTimes + 1
            if lastPointTimes > 4:
                Toast('自动寻路卡死-尝试调整')
                tapSleep(386, 1246)
            if lastPointTimes > 10:
                Toast('自动寻路卡死-返回')
                sleep(1)
                break

            if re:
                Toast('开始自动寻路')
                lastPoint = [re.x, re.y]
                if abs(re.x - lastPoint[0]) < 5 and abs(re.y - lastPoint[1] < 5):
                    lastPointTimes = lastPointTimes + 1
                else:
                    lastPointTimes = 0

                print(re.x, re.y)
                tapSleep(re.x, re.y)  # 切换探索标记的地图视角
                self.角色信息检查()
                # tapSleep(re.x, re.y + 150)  # 点击探索标记下方一格寻路
                tapSleep(re.x, re.y + 90)  # 点击探索标记下方一格寻路
                self.对话检查()
                # tapSleep(re.x, re.y + 50)  # 点击探索标记下方一格寻路
                # tapSleep(re.x - 150, re.y + 140)  # 点击探索标记下方一格寻路
                tapSleep(re.x + 150, re.y + 90)  # 点击探索标记下方一格寻路

            self.战斗检查()
            self.对话检查()
            self.奖励检查()
            self.其他检查()

            if not re:
                Toast('移动地图寻路')
                swipe(511, 551, 531, 819)
                sleep(2)

        Toast('探索完成-返回家园')
        tapSleep(60, 1216)

    def 其他检查(self):
        re = CompareColors.compare("301,899,#CCCF68|318,898,#CCCF68|356,896,#222222|375,894,#878947|437,898,#CCCF68",
                                   diff=0.95)
        if re:
            Toast('激活传送门')
            tapSleep(372, 896)
            return

        re = CompareColors.compare(
            "311,1001,#CCCF68|348,1003,#222222|371,1003,#8B8D49|372,1000,#222222|445,996,#CCCF68", diff=0.93)
        if re:
            Toast('开始探索')
            tapSleep(408, 1017)
            return

        re = CompareColors.compare(
            "293,1002,#CCCF68|348,1003,#7B7C41|367,997,#222222|345,1006,#8D8F4A|355,1003,#989B4F|372,1005,#9B9D50|453,1005,#CCCF68")
        if re:
            Toast('开始挑战')
            tapSleep(356, 995)
            return

        # re = FindColors.find(
        #     "293,1023,#CCCF68|322,1024,#CCCF68|340,1027,#222222|368,1026,#222222|447,1019,#CCCF68|352,1037,#222222",
        #     rect=[11, 110, 697, 1156], diff=0.98)
        # if re:
        #     Toast('解锁神像')
        #     tapSleep(re.x, re.y, 2)
        #     return

        re = CompareColors.compare("286,914,#E45454|294,914,#FFFFFF|300,914,#E25252")
        if re:
            Toast('领取主线奖励')
            tapSleep(274, 969)
            return

        re = FindColors.find("89,468,#E25353|94,470,#FEFEFE|100,472,#E65555", rect=[9, 240, 708, 968], diff=0.95)
        if re:
            Toast('寻路主线任务')
            tapSleep(re.x, re.y, 3)
            return

    def 角色信息检查(self):
        if 任务记录["探索生命补充-倒计时"] > 0:
            diffTime = time.time() - 任务记录["探索生命补充-倒计时"]
            if diffTime > 30:
                任务记录["探索生命补充-倒计时"] = time.time()
                # 治疗检查
                re = CompareColors.compare("56,151,#222222|60,156,#222222|63,145,#CCCF68|60,172,#CED171")  # 队伍图标
                if re:
                    re1 = CompareColors.compare("222,58,#CBCF60|231,58,#CBCF60|240,56,#CBCF60", diff=0.8)  # 绿色生命值
                    if not re1:
                        Toast('剩余生命不足-补充生命')
                        tapSleep(55, 66, 2)
                        re, 剩余生命 = TomatoOcrText(175, 954, 255, 989, '剩余生命')
                        Toast(f'剩余生命{剩余生命}')
                        剩余生命 = safe_float_v2(剩余生命.replace('%', ''))
                        if 剩余生命 < 70:
                            re = FindColors.find("584,1061,#DA514F|586,1062,#DA514F", rect=[415, 1046, 607, 1085],
                                                 diff=0.95)  # 料理不足红色数字
                            if re:
                                Toast('剩余料理不足-购买料理')
                                re = TomatoOcrTap(181, 1046, 244, 1077, '料理')
                                if re:
                                    TomatoOcrTap(156, 1019, 273, 1057, '自动选择')
                                    TomatoOcrTap(402, 774, 463, 808, '购买')
                            else:
                                Toast('一键治疗')
                                tapSleep(481, 1065)
                        tapSleep(333, 1216)  # 返回

        # re = CompareColors.compare("306,876,#CCCF68|342,877,#797B41|372,882,#5C5D34|414,884,#CCCF68")
        # if re:
        #     Toast('玩家信息关闭')
        #     tapSleep(353, 1212)

        re = CompareColors.compare(
            "443,377,#E7E9EE|473,377,#ECECEF|503,377,#E7E9EC|536,377,#E7E8EC|418,333,#707070|461,331,#707070")
        if re:
            Toast('玩家信息关闭')
            tapSleep(366, 1096)
            Toast('移开视角')
            tapSleep(158, 401, 2)  # 移开视角

        # re = CompareColors.compare("306,876,#CCCF68|342,877,#797B41|372,882,#5C5D34|414,884,#CCCF68")
        # if re:
        #     Toast('角色信息关闭')
        #     tapSleep(353, 1212)
        #
        #     Toast('角色信息关闭')
        #     tapSleep(353, 1212)
        #     tapSleep(158, 401, 2)  # 移开视角

    def 世界聊天检查(self):
        re = CompareColors.compare("36,1223,#060606|41,1234,#050505|52,1224,#0A0A0A|25,1248,#E2E2E2|52,1248,#E2E2E2")
        if re:
            Toast('世界聊天关闭')
            tapSleep(37, 1210)

    def 小游戏检查(self):
        re, _ = TomatoOcrText(265, 284, 435, 334, '能量回路')
        if re:
            Toast('开始能量回路')

    def 奖励检查(self):
        re = CompareColors.compare("202,369,#D3D770|214,369,#D6DA72|508,369,#D3D770|598,366,#D6DA71")
        if re:
            Toast('探索奖励确认')
            tapSleep(360, 372)

        re = CompareColors.compare("120,235,#C9CC67|157,236,#C6C965|535,238,#CCCF68|577,236,#CCCF68")
        if re:
            Toast('战斗奖励确认')
            tapSleep(360, 372)

    def 战斗检查(self):
        re = FindColors.find("292,568,#FEF9C9|303,568,#FCF6C9|303,578,#FEF6C5")  # 魔物阻挡
        if re:
            Toast('魔物阻挡')
            tapSleep(re.x - 30, re.y + 30, 2)

        re = imageFindClick('探索-小怪', x1=14, y1=123, x2=697, y2=1055)  # 魔物阻挡
        if re:
            Toast('清理小怪')
            # tapSleep(re.x + 10, re.y + 70, 2)

        re = TomatoOcrTap(290, 935, 426, 975, '开始战斗', sleep1=2)
        if not re:
            re = CompareColors.compare("39,920,#DFDEDA|47,918,#DFDEDA|50,935,#222121|58,934,#222121")
            if not re:
                return
        Toast('开始战斗')
        for k in range(90):
            re = CompareColors.compare("39,920,#DFDEDA|47,918,#DFDEDA|50,935,#222121|58,934,#222121")
            if not re:
                Toast('战斗结束')
                tapSleep(337, 1231)
                break
            Toast('战斗中')
            sleep(0.5)

    def 对话检查(self):
        re = FindColors.find(
            "360,1250,#222222|350,1251,#E2E2E2|366,1251,#DDDDDD|360,1256,#222222|314,1238,#DDDDDD|446,1245,#E2E2E2",
            rect=[170, 1046, 568, 1272], diff=0.96)  # 匹配对话箭头
        if re:
            for k in range(10):
                re = FindColors.find(
                    "360,1250,#222222|350,1251,#E2E2E2|366,1251,#DDDDDD|360,1256,#222222|314,1238,#DDDDDD|446,1245,#E2E2E2",
                    rect=[170, 1046, 568, 1272], diff=0.95)  # 匹配对话箭头
                if re:
                    Toast('对话中')
                    tapSleep(re.x, re.y)
            return True

        re = FindColors.find("89,986,#221F00|96,986,#221F00|108,985,#221F00|121,982,#E8E8E8|74,983,#EDEDED",
                             rect=[41, 754, 666, 1215])  # 匹配对话选择
        if re:
            Toast('选择对话选项')
            tapSleep(re.x, re.y)

        return False

    #  日常任务
    def 日常任务(self):
        if 功能开关["日常任务领取"] == 0:
            return
        self.homePage()
        Toast('开始领取每日任务')
        tapSleep(656, 1006, 1.5)
        re = TomatoOcrTap(252, 828, 337, 874, '任务')
        if not re:
            Toast('未找到每日任务入口')
            return
        for i in range(3):
            re = TomatoOcrTap(547, 205, 609, 238, '领取')
            if re:
                Toast('领取日常任务奖励')
                tapSleep(336, 42)  # 点击空白处
        re = CompareColors.compare("423,1196,#E45454|415,1194,#CA3C3C")  # 匹配周常任务红点
        if re:
            Toast('开始领取周常任务奖励')
            tapSleep(361, 1210)
            re = TomatoOcrTap(547, 205, 609, 238, '领取')
            if re:
                Toast('领取日常任务奖励')
                tapSleep(336, 42)  # 点击空白处

        re = CompareColors.compare("685,1194,#DE4E4E|694,1194,#E35353")  # 匹配任务红点
        if re:
            Toast('开始领取主线任务奖励')
            tapSleep(609, 1223)
            re = TomatoOcrTap(547, 205, 609, 238, '领取')
            if re:
                Toast('领取主线任务奖励')
                tapSleep(336, 42)  # 点击空白处
        tapSleep(72, 1216)  # 返回首页
        tapSleep(72, 1216)

    # 主线推图
    def newMap(self):
        if 功能开关["自动挑战首领"] == 1:
            self.homePage()
            for k in range(13):
                done, _ = TomatoOcrText(641, 872, 679, 890, '10', match_mode='fuzzy')  # X10 完成
                if done:
                    Toast('等待连续战斗完成')
                    break

                re = TomatoOcrTap(619, 850, 702, 875, '战', match_mode='fuzzy', offsetX=10, offsetY=-10)  # 主线挑战、连续战斗
                if re:
                    Toast('开始连续战斗')
                if not re:
                    tapSleep(682, 17)  # 点击空白处
