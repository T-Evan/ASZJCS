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
            tapSleep(52, 1229)
            TomatoOcrTap(457, 721, 525, 754, '确定', sleep1=1.5)
            # tapSleepV2(52, 1229)
            sleep(0.5)

    # 日常任务聚合
    def dailyTask(self):
        if 功能开关["日常总开关"] == 0:
            return

        self.homePage()

        # 日常相关

        # 世界喊话
        self.世界喊话()

        # 小推车领取
        self.小推车领取()

        # 命运之树领取
        self.小木床领取()

        # 小木床领取
        self.命运之树领取()

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

        # 每日特惠
        self.每日特惠()

        # 本周精选
        self.本周精选()

        # 其他签到活动
        self.其他签到活动()

        # 月卡领取
        self.月卡领取()

        # 每日商店
        self.每日商店()

        # 邮件领取
        self.邮件领取()

        # 地图探索
        self.地图探索()

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
            isFind = imageFindClick('家园-每日商店', x1=7, y1=396, x2=699, y2=1043, confidence1=0.6)
            if not isFind:
                re = FindColors.find("377,763,#2E4C31|445,768,#365026|371,857,#574126|411,861,#446E6D|467,860,#7D623A",
                                     rect=[7, 396, 699, 1043], diff=0.95)  # 夜间每日商店
                if not re:
                    re = FindColors.find(
                        "432,821,#4B3F32|468,832,#707085|507,831,#6C6C82|462,858,#43ABDF|455,783,#469572",
                        rect=[3, 476, 705, 1049], diff=0.93, ori=5)  # 白天每日商店
                if not re:
                    re = FindColors.find("498,861,#4E4132|549,864,#5191AD|590,872,#8E735F|544,768,#5C915C",
                                         rect=[4, 498, 702, 1040], diff=0.95, ori=5)  # 凌晨每日商店
                if re:
                    isFind = True
                    tapSleep(re.x, re.y - 40, 1.5)
            if isFind:
                Toast('家园-每日商店')
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
                swipe(197, 759, 487, 729)
                sleep(1.6)
            else:
                Toast('寻找每日商店')
                swipe(487, 729, 197, 759)
                sleep(1.6)

    def 其他签到活动(self):
        if 功能开关["其他签到活动"] == 0:
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
            re = TomatoOcrTap(467, 206, 671, 263, '启程好礼')
            if not re:
                re = TomatoOcrFindRangeClick(keywords=[{'keyword': '启程好礼', 'match_mode': 'fuzzy'}], sleep1=2, x1=7,
                                             y1=107,
                                             x2=699, y2=1144)
            if re:
                tapSleep(72, 284)  # 领取启程福利
                任务记录["启程好礼"] = 1
                tapSleep(71, 1215, 1.5)  # 返回商城页

        if 任务记录["幻想学院"] == 0:
            Toast('商城-幻想学院')
            re = TomatoOcrFindRangeClick(
                keywords=[{'keyword': '幻想', 'match_mode': 'fuzzy'}, {'keyword': '学院', 'match_mode': 'fuzzy'}],
                sleep1=2, x1=7,
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
        re = TomatoOcrTap(394, 1224, 461, 1259, '月卡', sleep1=1.5)
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
        任务记录["月卡领取"] = 1
        tapSleep(64, 1207)  # 空白
        tapSleep(64, 1207)  # 空白

    def 本周精选(self):
        if 功能开关["本周精选"] == 0 or 任务记录["本周精选"] == 1:
            return

        re = TomatoOcrTap(468, 981, 669, 1043, '本周精选', sleep1=1.5)
        if not re:
            self.homePage()
            Toast('日常-本周精选')
            tapSleep(656, 1006, 1.5)
            re = TomatoOcrTap(570, 827, 656, 875, '商城', sleep1=0.8)
            if not re:
                Toast('未找到商城入口')
                return
            swipe(360, 921, 361, 528)  # 下翻寻找本周精选
            sleep(1.5)
            re = TomatoOcrTap(468, 981, 669, 1043, '本周精选', sleep1=1.5)
            if not re:
                re = TomatoOcrFindRangeClick(keywords=[{'keyword': '本周精选', 'match_mode': 'fuzzy'}], sleep1=1.5,
                                             x1=7,
                                             y1=107,
                                             x2=699, y2=1144)
            if not re:
                Toast('未找到本周精选入口')
                任务记录["本周精选"] = 1
                return
        tapSleep(74, 243)  # 领取奖励
        任务记录["本周精选"] = 1
        tapSleep(74, 1202)  # 返回
        tapSleep(74, 1202)

    def 每日特惠(self):
        if 功能开关["每日特惠"] == 0 or 任务记录["每日特惠"] == 1:
            return
        self.homePage()
        Toast('日常-每日特惠')
        tapSleep(656, 1006, 1.5)
        re = TomatoOcrTap(570, 827, 656, 875, '商城', sleep1=0.8)
        if not re:
            Toast('未找到商城入口')
            return
        swipe(360, 921, 361, 528)  # 下翻寻找每日特惠
        sleep(1.5)
        re = TomatoOcrTap(467, 737, 666, 790, '每日特惠', sleep1=1.5)
        if not re:
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '每日特惠', 'match_mode': 'fuzzy'}], sleep1=1.5, x1=7,
                                         y1=107,
                                         x2=699, y2=1144)
        tapSleep(110, 377)  # 领取奖励
        tapSleep(345, 1229)  # 点击空白
        任务记录["每日特惠"] = 1
        tapSleep(74, 1202)  # 返回

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
        re = TomatoOcrTap(467, 942, 666, 1002, '巡礼之证')
        if not re:
            re = TomatoOcrFindRangeClick(keywords=[{'keyword': '巡礼之证', 'match_mode': 'fuzzy'}], sleep1=2, x1=7,
                                         y1=107,
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
        Toast('日常-菜就多躺')
        re = TomatoOcrTap(465, 203, 667, 261, '菜就', match_mode='fuzzy', sleep1=2)
        if not re:
            self.homePage()
            re = TomatoOcrTap(615, 176, 696, 200, '精彩', match_mode='fuzzy')
            if re:
                for k in range(3):
                    re = TomatoOcrTap(465, 203, 667, 261, '菜就', match_mode='fuzzy', sleep1=2)
                    if not re:
                        re = TomatoOcrFindRangeClick(
                            keywords=[{'keyword': '菜就', 'match_mode': 'fuzzy'},
                                      {'keyword': '多躺', 'match_mode': 'fuzzy'}],
                            sleep1=2, x1=15,
                            y1=91, x2=699, y2=1172)
                    if not re:
                        break
        if not re:
            Toast('菜就多躺-入口寻找失败')
            return
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
        Toast('日常-启程签到')
        re = TomatoOcrTap(467, 437, 667, 500, '启程签到', sleep1=2)
        if not re:
            self.homePage()
            re = TomatoOcrTap(615, 176, 696, 200, '精彩', match_mode='fuzzy')
            if re:
                re = TomatoOcrTap(467, 437, 667, 500, '启程签到', sleep1=2)
                if not re:
                    re = TomatoOcrFindRangeClick(keywords=[{'keyword': '启程签到', 'match_mode': 'fuzzy'}], sleep1=2,
                                                 x1=15,
                                                 y1=91, x2=699, y2=1172)
        if not re:
            Toast('启程签到-入口寻找失败')
            return
        任务记录["启程签到"] = 1
        re = FindColors.find("156,336,#DB5050|161,339,#FFFFFF|165,342,#D44444", rect=[7, 181, 701, 1047],
                             diff=0.95)
        if re:
            tapSleep(re.x, re.y, 1.5)
        tapSleep(77, 1212)  # 点击返回

    def 成长试炼(self):
        if 功能开关["成长试炼"] == 0 or 任务记录["成长试炼"] == 1:
            return

        Toast('日常-成长试炼')
        re = TomatoOcrTap(460, 699, 671, 756, '成长试炼', sleep1=2)
        if not re:
            self.homePage()
            re = TomatoOcrTap(615, 176, 696, 200, '精彩', match_mode='fuzzy')
            if re:
                re = TomatoOcrTap(460, 699, 671, 756, '成长试炼', sleep1=2)
                if not re:
                    re = TomatoOcrFindRangeClick(keywords=[{'keyword': '成长试炼', 'match_mode': 'fuzzy'}], sleep1=2,
                                                 x1=15,
                                                 y1=91, x2=699, y2=1172)
        if not re:
            Toast('成长试炼-入口寻找失败')
            return

        for k in range(5):
            Toast('成长试炼-领取')
            re = FindColors.find("122,463,#E35353|135,462,#E25252", rect=[33, 445, 686, 500], diff=0.95)
            if re:
                tapSleep(re.x, re.y)
            re = TomatoOcrTap(568, 610, 631, 644, '领取')
            if not re:
                Toast('日常-成长试炼完成')
                break
            tapSleep(341, 1234)  # 点击空白
        # 领取累积奖励
        re = FindColors.find("160,310,#E96E6E|169,313,#FFFFFF|174,318,#E25252", diff=0.95)
        if re:
            Toast('成长试炼-领取累积奖励')
            tapSleep(re.x - 5, re.y + 5)
            tapSleep(341, 1234)  # 点击空白

        任务记录["成长试炼"] = 1
        tapSleep(77, 1212)  # 点击返回

    def 每日签到(self):
        if 功能开关["每日签到"] == 0 or 任务记录["每日签到"] == 1:
            return
        self.homePage()
        Toast('日常-每日签到')
        re = TomatoOcrTap(615, 176, 696, 200, '精彩', match_mode='fuzzy', sleep1=1.3)
        if re:
            re = TomatoOcrTap(470, 946, 667, 1005, '签到', match_mode='fuzzy')
            if not re:
                re = TomatoOcrFindRangeClick(
                    keywords=[{'keyword': '每日', 'match_mode': 'fuzzy'}, {'keyword': '签到', 'match_mode': 'fuzzy'}],
                    sleep1=2, x1=15,
                    y1=91, x2=699, y2=1172)
            if re:
                re = FindColors.find("613,280,#9FB234|622,280,#FAFBDA|658,282,#A3BD3D", diff=0.95)
                if re:
                    tapSleep(re.x, re.y)
            if re:
                Toast('日常-每日签到完成')
                tapSleep(328, 1229)
            任务记录["每日签到"] = 1
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
            if not re:
                Toast('小木床-已免费加速')

    def 命运之树领取(self):
        if 功能开关["命运之树领取"] == 0:
            return

        if 任务记录["命运之树-倒计时"] > 0:
            diffTime = time.time() - 任务记录["命运之树-倒计时"]
            if diffTime < 20 * 60:
                Toast(f'命运之树-倒计时{round((3 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        re = FindColors.find("408,521,#FEDAE4|413,513,#FED7E1|419,519,#FED3DD|400,519,#FED2DC",
                             rect=[17, 426, 693, 915])
        if re:
            任务记录["命运之树-倒计时"] = time.time()
            Toast('命运之树领取')
            tapSleep(re.x, re.y)

    def 世界喊话(self):
        if 功能开关["世界喊话开关"] == 0:
            return

        need_dur_minute = safe_int(
            功能开关.get("世界喊话间隔", 0).replace("分钟", "").replace("分", "").replace("秒", "").replace("s",
                                                                                                            ""))  # 分钟
        if need_dur_minute == '':
            need_dur_minute = 1  # 默认1分钟
        if 任务记录["世界喊话-倒计时"] > 0:
            diffTime = time.time() - 任务记录["世界喊话-倒计时"]
            if diffTime < need_dur_minute * 60:
                Toast(f'世界喊话-倒计时{round((need_dur_minute * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        任务记录["世界喊话-倒计时"] = time.time()

        self.homePage()
        Toast('日常-世界喊话')
        tapSleep(67, 1089)  # 点击聊天框
        re, _ = TomatoOcrText(23, 789, 74, 820, '位面')
        if not re:
            Toast('世界喊话-未找到喊话入口')
            return
        Toast('世界喊话-已进入喊话入口')

        contentArr = []
        if 功能开关['世界喊话'] != "":
            contentArr.append(功能开关['世界喊话'])
        if 功能开关['世界喊话2'] != "":
            contentArr.append(功能开关['世界喊话2'])
        if 功能开关['世界喊话3'] != "":
            contentArr.append(功能开关['世界喊话3'])
        if 功能开关['世界喊话4'] != "":
            contentArr.append(功能开关['世界喊话4'])

        contents = random.choice(contentArr).split('|')
        print(contents)
        for content in contents:
            # print(content)
            res1 = TomatoOcrTap(99, 1210, 268, 1245, "聊天", 10, 10, match_mode='fuzzy')
            if res1:
                # 延迟 1 秒以便获取焦点，注意某些应用不获取焦点无法输入
                sleep(0.3)
                # 在输入框中输入字符串 "Welcome." 并回车；此函数在某些应用中无效，如支付宝、密码输入框等位置，甚至可能会导致目标应用闪退
                action.input(content)
                action.Key.back()  # 模拟返回键确认输入
                sleep(0.3)
                # 检查是否已输入
                shuru = TomatoOcrTap(99, 1210, 268, 1245, "聊天", 10, 10, match_mode='fuzzy')
                if shuru:
                    Toast('世界喊话-尝试重新输入')
                    action.input(content)
                    action.Key.back()  # 模拟返回键确认输入
                    sleep(0.3)
                isFaSong = False
                for k in range(4):
                    re, shuru = TomatoOcrText(99, 1210, 268, 1245, "聊天", match_mode='fuzzy')
                    if shuru and isFaSong:
                        Toast('世界喊话-已发送')
                        break
                    isFaSong = TomatoOcrTap(610, 1210, 669, 1243, "发", 10, 10, match_mode='fuzzy')
                    sleep(0.3)
                任务记录["世界喊话-倒计时"] = time.time()
            else:
                Toast('世界喊话-尝试清空输入框')
                res = TomatoOcrTap(610, 1210, 669, 1243, "发", 10, 10, match_mode='fuzzy')
                sleep(0.3)
        self.世界聊天检查()

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
        isFind = FindColors.find("43,724,#B27C1E|48,713,#F3D373|54,719,#835520|46,731,#C2A77D|54,727,#FBF490",
                                 rect=[6, 340, 701, 961], diff=0.9)
        if not isFind:
            isFind = FindColors.find("45,699,#FBD06F|47,692,#F4D478|53,697,#D7AD66|40,710,#A3845C|55,708,#F7EF8A",
                                     rect=[4, 399, 702, 823], diff=0.9)
        if not isFind:
            isFind = FindColors.find("47,686,#F2CC59|37,699,#975B43|53,700,#FDF999", rect=[3, 336, 704, 1041],
                                     diff=0.95)
        if isFind:
            Toast('日常-前往小推车')
            tapSleep(isFind.x, isFind.y, 1.5)

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
                # tapSleep(347, 108)  # 点击空白处
                break

        # 检测小推车升级
        if isFind:
            re = FindColors.find("408,840,#4BA5D5|415,840,#FEFEFE|419,841,#4AA5D5", rect=[195, 696, 508, 956],
                                 diff=0.93,
                                 ori=5)
            if re:
                tapSleep(re.x - 10, re.y + 10, 2)
                Toast('日常-小推车升级')
                for k in range(10):
                    re = FindColors.find("408,840,#4BA5D5|415,840,#FEFEFE|419,841,#4AA5D5", rect=[574, 351, 678, 1096],
                                         diff=0.95, ori=5)  # 匹配可升级标记
                    if re:
                        tapSleep(re.x, re.y, 1.5)
                        for m in range(10):
                            re = CompareColors.compare("527,1077,#42A3D3|543,1079,#43A2D4")  # 匹配可升级标记
                            if re:
                                Toast('小推车升级')
                                tapSleep(349, 1096)  # 点击升级
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
                             rect=[11, 831, 317, 1041], diff=0.95, ori=5)  # 匹配红色感叹号
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
                self.主线探索()

    def 主线探索(self):
        re = self.检测探索进入()
        if not re:
            return

        lastPoint = [0, 0]
        lastPointTimes = 0

        failTimes = 0
        for k in range(40):
            self.世界聊天检查()

            re = self.判断是否在探索地图()
            if not re:
                failTimes = failTimes + 1
                Toast(f'未处于探索地图-{failTimes}/5')
            else:
                failTimes = 0
            if failTimes > 3:
                Toast('当前未处于探索地图，中断探索')
                sleep(1)
                break

            re = imageFindClick('探索-定位未开启', x1=25, y1=858, x2=301, y2=1047, rgb=True, confidence1=0.6)
            if re:
                Toast('开启探索定位1')
            re = FindColors.find(
                "295,1006,#343434|289,1008,#4A4A4A|286,1014,#4E4E4E|294,1024,#4B4B4B|303,1014,#4F4F4F|295,1013,#4F4F4F",
                rect=[272, 853, 320, 1049], diff=0.95)
            if re:
                Toast('开启探索定位2')
                tapSleep(re.x, re.y)

            isFind = False
            if not isFind:
                isFind = FindColors.find("431,503,#E35353|436,499,#FEFEFE|438,499,#D27272|434,508,#D96161",
                                         rect=[4, 115, 705, 973], diff=0.93)  # 任务红点
                if not isFind:
                    isFind = FindColors.find("499,389,#E35353|509,389,#E35353|504,392,#FEFBFB",
                                             rect=[4, 115, 705, 973], diff=0.93)
                if isFind:
                    findX = isFind.x
                    findY = isFind.y
                    Toast('寻路主线任务提交')
            if not isFind:
                isFind, findX, findY = imageFind('寻路-战力之门', confidence1=0.7)  # 匹配地图的战力之门标记
                if isFind:
                    Toast('寻路战力之门')
            if not isFind:
                isFind, findX, findY = imageFind('寻路-女神像', confidence1=0.7)
                if isFind:
                    Toast('寻路女神像')
            if not isFind:
                isFind, findX, findY = imageFind('寻路-失落女神像', confidence1=0.7)
                if isFind:
                    Toast('寻路失落女神像')
            if not isFind:
                isFind, findX, findY = imageFind('寻路-远航之碑', confidence1=0.7)
                if isFind:
                    Toast('寻路远航之碑')
            if not isFind:
                isFind, findX, findY = imageFind('寻路-定位', confidence1=0.7, rgb=True)  # 匹配地图的定位标记
            if not isFind:
                lastPointTimes = lastPointTimes + 1

            if isFind:
                if 5 < lastPointTimes < 7:
                    Toast('寻路方案2')
                    swipe(344, 857, 375, 505)
                    sleep(1)
                    tapSleep(findX, findY + 250, 1.5)  # 点击探索标记下方一格寻路
                if 7 <= lastPointTimes <= 9:
                    Toast('寻路方案3')
                    swipe(344, 857, 375, 505)
                    sleep(1)
                    tapSleep(findX, findY + 400, 1.5)  # 点击探索标记下方一格寻路
                if 9 <= lastPointTimes < 10:
                    Toast('自动寻路卡死-尝试手动调整')
                    tapSleep(386, 1246)
                    tapSleep(667, 647, 1)
                    swipe(547, 626, 254, 662)
                    tapSleep(667, 647, 2)
                if lastPointTimes > 12:
                    Toast('自动寻路卡死-返回重试')
                    sleep(1)
                    break

                Toast(f'自动寻路-第{lastPointTimes}/12次')
                if abs(findX - lastPoint[0]) < 5 and abs(findY - lastPoint[1] < 5):
                    lastPointTimes = lastPointTimes + 1
                else:
                    lastPointTimes = 0

                lastPoint = [findX, findY]
                print(lastPoint)
                tapSleep(findX, findY, 0.5)  # 切换探索标记的地图视角
                re = self.判断是否在探索地图()
                if re:
                    self.角色信息检查()
                    # tapSleep(re.x, re.y + 150)  # 点击探索标记下方一格寻路
                    tapSleep(findX, findY + 90, 1.2)  # 点击探索标记下方一格寻路
                    self.对话检查()
                    # tapSleep(re.x, re.y + 50)  # 点击探索标记下方一格寻路
                    # tapSleep(re.x - 150, re.y + 140)  # 点击探索标记下方一格寻路
                    tapSleep(findX + 150, findY + 90, 1.2)  # 点击探索标记下方一格寻路
                else:
                    self.角色信息检查()
                    isFind = False

            self.角色信息检查()
            self.战斗检查()
            self.对话检查()
            self.奖励检查()
            self.其他检查()

            if not isFind:
                re = self.判断是否在探索地图()
                if not re:
                    Toast('返回探索地图')
                    tapSleep(337, 36)
                if re:
                    Toast('移动地图寻路')
                    swipe(511, 551, 531, 819)
                    sleep(2)

        Toast('探索完成-返回家园')
        tapSleep(60, 1216)

    def 检测探索进入(self):
        Toast('等待进入探索地图')
        ifFind = False
        for i in range(10):
            self.对话检查()
            re = self.判断是否在探索地图()
            if re:
                ifFind = True
                Toast('已进入探索地图')
                break
            sleep(0.5)
        if not ifFind:
            Toast('进入探索地图失败-返回')
        return ifFind

    def 地图探索(self):
        if 功能开关["地图探索"] == 0:
            return

        if 任务记录["地图探索-倒计时"] > 0:
            diffTime = time.time() - 任务记录["地图探索-倒计时"]
            if diffTime < 10 * 60:
                Toast(f'地图探索-倒计时{round((10 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        任务记录["地图探索-倒计时"] = time.time()

        self.homePage()
        Toast('日常-地图探索')
        re = self.进入笔记()
        if not re:
            return
        re = CompareColors.compare("285,576,#67C9EA|83,576,#658A69|118,568,#325447|282,620,#5FCBE8")
        if re:
            tapSleep(219, 590, 1.2)
        if not re:
            re = TomatoOcrTap(6, 637, 167, 686, '地图', match_mode='fuzzy')
        if not re:
            Toast('日常-地图探索未开启')
            sleep(0.5)
            return

        Toast('日常-进入地图探索')

        re = CompareColors.compare("129,579,#E45454|135,579,#F1DCDC|140,579,#D84A4A")
        if re:
            Toast('地图探索-领取命运果实')
            tapSleep(90, 595)
            tapSleep(369, 1235)

        re, tili = TomatoOcrText(74, 214, 172, 241, '剩余体力')
        tili = safe_int_v2(tili.replace('/300', ''))
        if tili < 20:
            Toast(f'地图探索-体力不足返回-{tili}/300')
            tapSleep(67, 1212)
            return

        if 功能开关['金币探索'] == 1:
            Toast('日常-金币探索')
            tapSleep(61, 307)
        elif 功能开关['粗炼石探索'] == 1:
            Toast('日常-粗炼石探索')
            tapSleep(131, 314)
        elif 功能开关['时之砂探索'] == 1:
            Toast('日常-时之砂探索')
            tapSleep(214, 315)
        elif 功能开关['历战精华探索'] == 1:
            Toast('日常-历战精华探索')
            tapSleep(284, 309)

        Toast('前往探索地图')
        tapSleep(573, 252, 1.5)
        re = TomatoOcrTap(454, 719, 530, 756, '确定')
        if not re:
            Toast('前往探索地图失败-返回')
            tapSleep(67, 1212)
            return

        re = self.检测探索进入()
        if not re:
            return

        if 功能开关['金币探索'] == 1:
            Toast(f'开始探索金币')
        elif 功能开关['粗炼石探索'] == 1:
            Toast(f'开始探索粗炼石')
        elif 功能开关['时之砂探索'] == 1:
            Toast(f'开始探索时之砂')
        elif 功能开关['历战精华探索'] == 1:
            Toast(f'开始探索历战精华')

        failTimes = 0
        isStart = False
        start_time = int(time.time())
        for k in range(120):
            self.世界聊天检查()

            re = self.判断是否在探索地图()
            if not re:
                failTimes = failTimes + 1
                Toast(f'未处于探索地图{failTimes}/10')
            if failTimes > 10:
                Toast('当前未处于探索地图，中断探索')
                sleep(1)
                break

            if not isStart:
                re = imageFindClick('探索-托管', x1=6, y1=782, x2=326, y2=1055, rgb=True, confidence1=0.7)
                if not re:
                    re = imageFindClick('探索-托管2', x1=6, y1=782, x2=326, y2=1055, rgb=True, confidence1=0.7)
                if re:
                    Toast('探索-配置托管')
                    for i in range(40):
                        re, currCount = TomatoOcrText(308, 855, 409, 894, '探索次数')
                        needCount = safe_int_v2(功能开关['探索次数'])
                        if needCount == 0:
                            needCount = 15  # 默认重复15次，消耗75体力
                        currCount = safe_int_v2(currCount)
                        print(f'探索次数配置{currCount}/{needCount}次')
                        if currCount < needCount:
                            Toast(f'探索次数配置{currCount}/{needCount}次')
                            tapSleep(528, 874, 0.1)
                        else:
                            break
                    re = TomatoOcrTap(301, 937, 415, 975, '开始托管')
                    if not re:
                        Toast('探索托管失败')
                        break
                    isStart = True
                    Toast('探索-开始托管')
                else:
                    Toast(f'探索开始托管失败{failTimes}/10')
                    failTimes = failTimes + 1
                    if failTimes > 10:
                        break
            if isStart:
                current_time = int(time.time())
                elapsed = current_time - start_time
                if elapsed > 8:
                    re = imageFindClick('探索-托管', x1=6, y1=782, x2=326, y2=1055, confidence1=0.7)
                    if not re:
                        re = imageFindClick('探索-托管2', x1=6, y1=782, x2=326, y2=1055, confidence1=0.7)
                    if re:
                        re, _ = TomatoOcrText(301, 937, 415, 975, '开始托管')
                        tapSleep(371, 116)  # 关闭托管页面
                        if re:
                            Toast(f'探索托管完成')
                            break
                    start_time = int(time.time())  # 重置托管检查计时
                Toast(f'探索中{k}/120')
                sleep(1)
            sleep(1)

        Toast('探索完成-返回家园')
        tapSleep(60, 1216)

    def 其他检查(self):
        re, _ = TomatoOcrText(573, 833, 659, 878, '商城')
        if re:
            Toast('关闭商城页')
            tapSleep(331, 74)

        re = FindColors.find("89,468,#E25353|94,470,#FEFEFE|100,472,#E65555", rect=[9, 240, 708, 968], diff=0.95)
        if re:
            Toast('寻路主线任务')
            tapSleep(re.x - 10, re.y + 10, 2)

        re = CompareColors.compare("675,950,#E1E1E1|680,956,#A7A7A7|683,956,#A7A7A7|686,959,#E2E2E2")
        if re:
            Toast('关闭大地图')
            tapSleep(72, 1223)

        re, _ = TomatoOcrText(261, 279, 474, 339, '回路', match_mode='fuzzy')
        if re:
            Toast('能量回路-跳过解密')
            tapSleep(641, 162, 2)  # 点击菲涅克对话
            tapSleep(332, 1224, 1.5)  # 继续对话
            tapSleep(332, 1224, 1.5)  # 继续对话
            TomatoOcrFindRangeClick('帮我', x1=64, y1=714, x2=662, y2=1029, sleep1=2, match_mode='fuzzy')
            TomatoOcrFindRangeClick('提交', x1=64, y1=714, x2=662, y2=1029, sleep1=2, match_mode='fuzzy')
            TomatoOcrFindRangeClick('确定', x1=64, y1=714, x2=662, y2=1029, sleep1=2, match_mode='fuzzy')
            return

        re = TomatoOcrTap(323, 874, 394, 913, '激活')
        if re:
            Toast('激活传送门')
            return

        re = TomatoOcrTap(325, 877, 394, 913, '探索')
        if not re:
            re = TomatoOcrTap(327, 984, 393, 1022, '探索')
        if re:
            Toast('开始探索')
            return

        re = TomatoOcrTap(314, 890, 407, 934, '探索')
        if re:
            Toast('继续探索')
            return

        re = TomatoOcrTap(323, 888, 395, 929, '访问')
        if re:
            Toast('访问雕像')
            return

        re = CompareColors.compare(
            "293,1002,#CCCF68|348,1003,#7B7C41|367,997,#222222|345,1006,#8D8F4A|355,1003,#989B4F|372,1005,#9B9D50|453,1005,#CCCF68")
        if re:
            Toast('开始挑战')
            tapSleep(356, 995)
            return

        re = TomatoOcrTap(330, 931, 390, 969, '开启')
        if re:
            Toast('开启战力之门')
            return

        re = TomatoOcrTap(323, 980, 397, 1018, '解', match_mode='fuzzy')
        if not re:
            re = TomatoOcrTap(325, 1005, 394, 1046, '解', match_mode='fuzzy')
        if re:
            Toast('解锁神像')
            return

        # 领取任务奖励
        re = self.判断是否在探索地图()
        if re:
            re = FindColors.find("322,903,#E45151|333,904,#E35353|328,901,#FFFFFF|328,896,#FFFFFF",
                                 rect=[11, 831, 317, 1041], diff=0.95, ori=5)  # 匹配红色感叹号
            if re:
                Toast('领取主线奖励')
                tapSleep(re.x, re.y)
                return

    def 角色信息检查(self):
        diffTime = time.time() - 任务记录["探索生命补充-倒计时"]
        re = CompareColors.compare("211,58,#38383A|227,59,#39393B|242,58,#39393C")  # 生命值过半
        if re or diffTime > 30:
            re = self.判断是否在探索地图()
            if not re:
                Toast('角色检查-未处于探索地图')
            if re:
                任务记录["探索生命补充-倒计时"] = time.time()
                # 治疗检查
                re1 = CompareColors.compare("211,58,#38383A|227,59,#39393B|242,58,#39393C")  # 生命值过半
                if re1:
                    Toast('剩余生命不足-补充生命')
                    tapSleep(93, 55, 2)
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

        re, _ = TomatoOcrText(323, 880, 396, 916, '替换')
        if not re:
            re, _ = TomatoOcrText(325, 863, 393, 901, '替换')
        if re:
            Toast('玩家信息关闭')
            tapSleep(333, 77)  # 返回
            tapSleep(333, 77)

        re, _ = TomatoOcrText(179, 1041, 244, 1082, '料理')
        if re:
            Toast('玩家信息关闭')
            tapSleep(342, 1240)
            Toast('移开视角')
            tapSleep(476, 516, 2)  # 移开视角

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
        re = CompareColors.compare("120,235,#C9CC67|157,236,#C6C965|535,238,#CCCF68|577,236,#CCCF68")
        if re:
            Toast('战斗奖励确认')
            tapSleep(360, 372)
            return

        re = FindColors.find(
            "23,351,#D6DA72|18,372,#D5D76F|18,388,#DADA71|667,347,#D1D46E|665,361,#D6DA71|657,386,#D6D96F",
            rect=[4, 97, 700, 560], diff=0.95)
        if re:
            Toast('探索奖励确认')
            tapSleep(360, 372)
            return

    def 战斗检查(self):
        re = FindColors.find("414,651,#FEFACA|414,658,#FFF6C7|421,662,#FFF2BD|419,660,#A8803A", diff=0.95)  # 魔物阻挡
        if re:
            Toast('魔物阻挡1')
            tapSleep(re.x, re.y, 2)
        re = FindColors.find("312,530,#FEFAD0|312,536,#FEFBCC|326,557,#FEF3BF|332,557,#FEF3BF", diff=0.95)
        if re:
            Toast('魔物阻挡2')
            tapSleep(re, re.y, 2)

        re = imageFindClick('探索-小怪', x1=14, y1=123, x2=697, y2=1055)  # 魔物阻挡
        if re:
            Toast('清理小怪')

        re = TomatoOcrTap(290, 935, 426, 975, '开始战斗', sleep1=2)
        if not re:
            re = CompareColors.compare("39,920,#DFDEDA|47,918,#DFDEDA|50,935,#222121|58,934,#222121")  # 战斗中队伍图标
        if not re:
            return
        Toast('开始战斗')
        failTimes = 0
        for k in range(90):
            if k < 5:
                re = imageFindClick('幻想阶梯-自动挑战', x1=11, y1=711, x2=183, y2=1046)
                if re:
                    Toast('幻想阶梯-已开启后台挑战')
                    return

            re = CompareColors.compare("39,920,#DFDEDA|47,918,#DFDEDA|50,935,#222121|58,934,#222121")
            if not re:
                Toast(f'战斗状态识别失败{failTimes}/5')
                failTimes = failTimes + 1
            if failTimes > 5:
                Toast('战斗结束')
                tapSleep(337, 1231)
                break

            re = TomatoOcrTap(286, 828, 433, 869, '层', match_mode='fuzzy')
            if re:
                Toast('战斗中-进入下一层')
                failTimes = 0

            re = TomatoOcrTap(320, 976, 396, 1011, '确定')
            if re:
                Toast('战斗中-选择奖励')
                failTimes = 0

            Toast('战斗中')
            sleep(0.5)

    def 对话检查(self):
        re = FindColors.find("354,1241,#202020|366,1241,#202020|360,1252,#222222|352,1251,#DBDBDB|367,1252,#DCDCDC",
                             rect=[320, 1212, 406, 1275])  # 匹配对话箭头
        if re:
            failTimes = 0
            for k in range(30):
                re = FindColors.find(
                    "354,1241,#202020|366,1241,#202020|360,1252,#222222|352,1251,#DBDBDB|367,1252,#DCDCDC",
                    rect=[320, 1212, 406, 1275])  # 匹配对话箭头
                if re:
                    Toast('对话中')
                    tapSleep(re.x, re.y)
                    failTimes = 0
                else:
                    failTimes = failTimes + 1
                if failTimes > 5:
                    Toast('对话结束')
                    break
                sleep(0.5)
            return True

        re = FindColors.find("588,891,#E3E3E3|583,902,#E5E5E5|626,894,#CDD169|643,885,#CCD168|627,910,#E3E3E3",
                             rect=[551, 547, 671, 1186], diff=0.95)  # 匹配对话选择
        if re:
            Toast('选择对话选项')
            tapSleep(re.x, re.y)

        return False

    #  日常任务
    def 日常任务(self):
        if 功能开关["日常任务领取"] == 0:
            return

        if 任务记录["日常任务-倒计时"] > 0:
            diffTime = time.time() - 任务记录["日常任务-倒计时"]
            if diffTime < 3 * 60:
                Toast(f'日常任务-倒计时{round((3 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        任务记录["日常任务-倒计时"] = time.time()

        self.homePage()
        Toast('开始领取每日任务')
        tapSleep(656, 1006, 1.5)
        re = TomatoOcrTap(252, 828, 337, 874, '任务', sleep1=1.5)
        if not re:
            Toast('未找到每日任务入口')
            return
        for i in range(3):
            re = TomatoOcrTap(547, 205, 609, 238, '领取')
            if not re:
                break
            Toast('领取日常任务奖励')
            tapSleep(336, 42)  # 点击空白处
        re = CompareColors.compare("506,1197,#CE4D4D|511,1197,#D64747")  # 匹配周常任务红点
        if re:
            Toast('开始领取周常任务奖励')
            tapSleep(361, 1210, 1.5)
            re = TomatoOcrTap(547, 205, 609, 238, '领取')
            if re:
                Toast('领取日常任务奖励')
                tapSleep(336, 42)  # 点击空白处

        re = CompareColors.compare("685,1194,#DE4E4E|694,1194,#E35353")  # 匹配任务红点
        if re:
            Toast('开始领取主线任务奖励')
            tapSleep(609, 1223, 1.5)
            re = FindColors.find("577,509,#E45454|584,510,#FFFFFF|591,510,#E25252", rect=[471, 220, 685, 1150])
            if re:
                Toast('领取主线任务奖励')
                tapSleep(re.x, re.y)
                tapSleep(336, 42)  # 点击空白处

        re = CompareColors.compare("547,1193,#E45454|558,1193,#E05151")
        if re:
            Toast('开始领取委托任务奖励')
            tapSleep(501, 1220, 1.5)
            for k in range(4):
                # 判断是否可合成
                re1 = FindColors.find("59,337,#9FA42D|56,346,#9FA42E|118,341,#9FA438", rect=[25, 173, 697, 1155],
                                      diff=0.9)
                if re:
                    Toast('开始合成悬赏')
                    tapSleep(re.x, re.y, 1.5)  # 点击待合成物品
                    tapSleep(581, 727, 1.2)  # 点击炼金炉合成
                    re = TomatoOcrTap(334, 1202, 386, 1234, '合成')
                    if not re:
                        Toast('合成失败-未进入合成页面')
                        return
                    re = FindColors.find("352,1003,#F75238|352,1005,#F85338", rect=[58, 880, 674, 1040],
                                         diff=0.95)  # 匹配二级合成入口
                    if re:
                        Toast('开始合成二级材料')
                        tapSleep(re.x, re.y, 1.5)  # 点击二级合成入口
                        tapSleep(581, 727, 1.2)  # 点击炼金炉合成
                    re = TomatoOcrTap(326, 1079, 392, 1117, '合成')
                    if re:
                        Toast('合成成功')
                        tapSleep(351, 45)  # 点击空白处
                        tapSleep(59, 1224)  # 返回
                        tapSleep(365, 45)  # 点击空白处

                re2 = FindColors.find("577,509,#E45454|584,510,#FFFFFF|591,510,#E25252", rect=[25, 160, 695, 953])
                if not re1 and not re2:
                    break
                tapSleep(re.x, re.y)
                Toast('提交委托任务')
                tapSleep(336, 42)  # 点击空白处
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

    def 进入笔记(self):
        isFind = False
        for k in range(3):
            tapSleep(219, 1231)  # 点击笔记
            re, _ = TomatoOcrText(191, 1249, 246, 1276, '笔记')
            if re:
                isFind = True
                break
        if not isFind:
            Toast('未找到笔记入口')
        else:
            Toast('跳转笔记')
        return isFind

    def 馈赠领取(self):
        Toast('检查馈赠领取')
        re = TomatoOcrFindRangeClick(
            keywords=[{'keyword': '馈', 'match_mode': 'fuzzy'}, {'keyword': '赠', 'match_mode': 'fuzzy'}], x1=151,
            y1=1174, x2=695, y2=1251)
        if not re:
            Toast('未找到馈赠入口')
            return

        for k in range(2):
            re = TomatoOcrTap(562, 205, 614, 233, '领取', sleep1=1.5)
            if re:
                Toast('领取馈赠')
                tapSleep(620, 1130)  # 点击空白
            re = CompareColors.compare("473,1100,#E35353|480,1100,#FFFFFF|486,1100,#E25252")  # 匹配全服馈赠
            if re:
                Toast('幻想阶梯-领取全服馈赠')
                tapSleep(443, 1119)  # 点击全服馈赠

    def 判断是否在探索地图(self):
        re, name = TomatoOcrText(493, 262, 710, 290, '地图名称')
        if '(' not in name and ')' not in name:
            return False
        return True
