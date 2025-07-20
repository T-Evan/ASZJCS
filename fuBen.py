# 导包
import time

from .特征库 import *
from .res.ui.ui import 功能开关
from .startUp import StartUp
from .res.ui.ui import 任务记录
from .baseUtils import *
from .daily import DailyTask
from ascript.android.screen import FindColors


class FuBenTask:
    def __init__(self):
        self.startupTask = StartUp(f"{功能开关['游戏包名']}")
        self.dailyTask = DailyTask()

    # 副本任务聚合
    def fuBenTask(self):
        if 功能开关["副本总开关"] == 0 or 功能开关["副本自动接收邀请"] == 1:
            return

        self.dailyTask.homePage()

        # 幻想阶梯
        self.幻想阶梯()

        # 圣兽试炼
        self.圣兽试炼()

        # 混沌侵袭
        self.混沌侵袭()

        # 素材秘境
        self.素材秘境()

        # 地图探索
        self.dailyTask.地图探索()

        # 魔物讨伐
        self.魔物讨伐()

        # 每日副本
        self.每日副本()

    def 魔物讨伐(self):
        if 功能开关["魔物讨伐"] == 0:
            return
        Toast('副本-魔物讨伐')
        isFind = False
        nowCheck = ''
        for k in range(2):
            self.dailyTask.homePage()
            Toast('魔物讨伐-寻找聊天入口')
            tapSleep(650, 1090, 0.4)  # 点击聊天框
            tapSleep(670, 1090, 0.4)  # 点击聊天框
            isFind, _ = TomatoOcrText(609, 1208, 672, 1245, '发送', match_mode='fuzzy')
            if isFind:
                break
        if not isFind:
            Toast('魔物讨伐-寻找聊天入口失败')
            sleep(0.5)
            return
        Toast('魔物讨伐-已进入界域聊天')

        start_time = int(time.time())
        change_time = int(time.time())  # 切换频道检查
        功能开关["寻找讨伐等待时长"] = safe_int_v2(功能开关["寻找讨伐等待时长"])
        if 功能开关["寻找讨伐等待时长"] == 0:
            功能开关["寻找讨伐等待时长"] = 5  # 默认5分钟
        totalWait = 功能开关["寻找讨伐等待时长"] * 60
        lastFind = []
        while 1:
            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed > totalWait:
                Toast('魔物讨伐-等待队伍超时')
                break

            if current_time - change_time > 5:
                change_time = int(time.time())  # 切换频道检查
                lastFind = []
                if 功能开关['魔物讨伐切换频道'] == 1:
                    Toast('魔物讨伐-切换频道')
                    if nowCheck == '位面':
                        isFind = TomatoOcrFindRangeClick(
                            keywords=[{'keyword': '界', 'match_mode': 'fuzzy'},
                                      {'keyword': '域', 'match_mode': 'fuzzy'}],
                            x1=14,
                            y1=511, x2=85, y2=1161, sleep1=0.5)
                        nowCheck = '界域'

                    else:
                        TomatoOcrFindRangeClick(
                            keywords=[{'keyword': '位', 'match_mode': 'fuzzy'},
                                      {'keyword': '面', 'match_mode': 'fuzzy'}],
                            x1=14,
                            y1=511, x2=85, y2=1161, sleep1=0.5)
                        nowCheck = '位面'

            isFind, _ = TomatoOcrText(609, 1208, 672, 1245, '发送', match_mode='fuzzy')
            if not isFind:
                Toast('魔物讨伐-已退出聊天频道')
                break

            Toast(f'魔物讨伐-等待讨伐队伍{elapsed}/{totalWait}')
            all_points = []
            isFind1, tmpPoints = imageFindAll('危险的魔物', x1=126, y1=94, x2=666, y2=1145, confidence1=0.8)
            all_points.extend(tmpPoints)
            isFind2, tmpPoints = imageFindAll('强大的魔王', x1=126, y1=94, x2=666, y2=1145, confidence1=0.8)
            all_points.extend(tmpPoints)
            all_points = sorted(all_points, key=lambda x: x["center_y"], reverse=True)
            for p in all_points:
                if p['center_y'] in lastFind:
                    continue
                tapSleep(p['center_x'], p['center_y'], 0.1)
                tapSleep(p['center_x'], p['center_y'], 0.1)
                Toast('魔物讨伐-加入讨伐队伍')
                lastFind.append(p['center_y'])
                isClick = False
                for k in range(5):
                    isClick, _ = TomatoOcrText(457, 719, 526, 754, '确定')
                    if isClick:
                        break
                    re = CompareColors.compare(
                        "307,329,#FFFFFF|337,334,#FFFFFF|364,331,#FFFFFF|394,329,#FFFFFF|418,329,#FFFFFF|440,336,#FFFFFF",
                        diff=0.86)
                    if re:
                        Toast('魔物讨伐-已被讨伐')
                        break
                    sleep(0.1)
                if isClick:
                    break

            if isFind1 or isFind2:
                # 点击加入讨伐
                waitFight = False
                waitConfirm = False
                fightDone = False
                for k in range(20):
                    if not waitConfirm:
                        re = TomatoOcrTap(457, 719, 526, 754, '确定', sleep1=2)
                        if re:
                            waitConfirm = True
                        if k > 4 and not re:
                            Toast('加入失败-魔王已被讨伐')
                            break
                    waitFight = CompareColors.compare(
                        "40,164,#CED168|52,159,#242424|62,142,#CED168|65,175,#CCCF68|68,167,#929463")  # 是否进入探索地图
                    if waitFight:
                        break
                    sleep(0.3)
                if waitFight or waitConfirm:
                    lastFind = []
                    Toast('前往讨伐地图')
                    failFindTimes = 0
                    for k in range(20):
                        re = TomatoOcrTap(474, 964, 542, 1005, '讨伐', 2)
                        re = TomatoOcrTap(293, 934, 424, 978, '战斗', match_mode='fuzzy')
                        if re:
                            Toast('开始讨伐')
                            failTimes = 0
                            fightDone = True
                            start_time = int(time.time())
                            for m in range(400):
                                re = CompareColors.compare(
                                    "39,920,#DFDEDA|47,918,#DFDEDA|50,935,#222121|58,934,#222121")
                                if not re:
                                    Toast(f'战斗状态识别失败{failTimes}/5')
                                    failTimes = failTimes + 1
                                    re = TomatoOcrTap(300, 273, 423, 315, '战斗结束', match_mode='fuzzy')
                                    if re:
                                        Toast('讨伐战斗结束')
                                        tapSleep(337, 1231)
                                        break
                                if failTimes > 7:
                                    Toast('战斗结束')
                                    tapSleep(337, 1231)
                                    break

                                re = TomatoOcrTap(320, 976, 396, 1011, '确定')
                                if re:
                                    Toast('战斗中-选择奖励')
                                    failTimes = 0
                                # self.战斗喊话()

                                Toast('战斗中')
                                sleep(0.5)
                        if fightDone:
                            break

                        # 二次检测是否已进入战斗
                        re1, _ = TomatoOcrText(474, 964, 542, 1005, '讨伐')
                        re2, _ = TomatoOcrText(293, 934, 424, 978, '战斗', match_mode='fuzzy')
                        if re1 or re2:
                            continue

                        waitPoint = False
                        # if not waitPoint:
                        #     waitPoint = FindColors.find(
                        #         "280,880,#E25353|419,880,#2B2A29|425,880,#2C2A28|436,882,#2E2D2B",
                        #         rect=[0, 6, 701, 1272], diff=0.96)  # 魔王底部血条
                        #     if waitPoint:
                        #         print(waitPoint.x, waitPoint.y)
                        #         Toast('点击魔王4')
                        #         tapSleep(waitPoint.x + 50, waitPoint.y - 80, 2.5)
                        waitPoint = FindColors.find("325,909,#E35353|342,909,#E15252|344,905,#E35353|372,907,#E25252",
                                                    diff=0.94)  # 魔王底部血条
                        if waitPoint:
                            if 12 < waitPoint.x < 281 and 970 < waitPoint.y < 1030:
                                print(waitPoint.x, waitPoint.y)
                            else:
                                print(waitPoint.x, waitPoint.y)
                                Toast('点击魔王1')
                                tapSleep(waitPoint.x + 50, waitPoint.y - 80, 1.2)

                        if not waitPoint:
                            waitPoint = FindColors.find(
                                "454,905,#303C2A|467,907,#36432C|481,904,#3D4C31|498,907,#3D4F32",
                                diff=0.98)  # 魔王底部血条
                            if waitPoint:
                                if 12 < waitPoint.x < 281 and 970 < waitPoint.y < 1030:
                                    print(waitPoint.x, waitPoint.y)
                                else:
                                    print(waitPoint.x, waitPoint.y)
                                    Toast('点击魔王2')
                                    tapSleep(waitPoint.x - 40, waitPoint.y - 80, 1.2)

                        # 二次检测是否已进入战斗
                        re1, _ = TomatoOcrText(474, 964, 542, 1005, '讨伐')
                        re2, _ = TomatoOcrText(293, 934, 424, 978, '战斗', match_mode='fuzzy')
                        if re1 or re2:
                            continue

                        # 未找到可点击魔王，点击头像寻路
                        if not waitPoint:
                            waitFind = FindColors.find(
                                "328,1204,#FBFBF3|357,1223,#FFFFEE|345,1248,#222222|307,1242,#FEFEF1|309,1229,#222222",
                                rect=[0, 6, 701, 1272], diff=0.9)  # 魔物图标
                            if waitFind:
                                if waitFind.x < 130 and waitFind.y < 138:
                                    Toast('移动视角讨伐区域-1')
                                    swipe(244, 456, 495, 784)
                                else:
                                    Toast('前往讨伐区域-1')
                                    tapSleep(waitFind.x, waitFind.y + 4)
                            if not waitFind:
                                waitFind = FindColors.find(
                                    "357,1218,#FBFBF4|378,1205,#FAFAF1|405,1224,#FDFFEE|406,1238,#BABD6E",
                                    rect=[7, 9, 703, 1278], diff=0.9)
                                if waitFind:
                                    if waitFind.x < 130 and waitFind.y < 138:
                                        Toast('移动视角讨伐区域-2')
                                        swipe(244, 456, 495, 784)
                                    else:
                                        Toast('前往讨伐区域-2')
                                        tapSleep(waitFind.x + 3, waitFind.y + 3, 1)
                            if not waitFind:
                                waitFind = FindColors.find(
                                    "691,752,#3F3F3E|690,746,#F8F8F0|655,746,#696969|652,757,#E2E2E2|671,785,#414140|690,776,#E9E9E3",
                                    diff=0.95)
                                if waitFind:
                                    if waitFind.x < 130 and waitFind.y < 138:
                                        Toast('移动视角讨伐区域-3')
                                        swipe(244, 456, 495, 784)
                                    else:
                                        Toast('前往讨伐区域-3')
                                        tapSleep(waitFind.x + 3, waitFind.y + 3, 1)

                        if not waitPoint:
                            waitPoint = FindColors.find(
                                "421,912,#E35353|429,912,#E35353|437,912,#E35353|446,912,#E35353", diff=0.95)  # 魔王底部血条
                            if waitPoint:
                                if 12 < waitPoint.x < 281 and 970 < waitPoint.y < 1030:
                                    print(waitPoint.x, waitPoint.y)
                                else:
                                    print(waitPoint.x, waitPoint.y)
                                    Toast('点击魔王6')
                                    tapSleep(waitPoint.x + 50, waitPoint.y - 80, 2.5)
                        if not waitPoint:
                            failFindTimes = failFindTimes + 1
                            Toast(f'寻找魔王位置失败{failFindTimes}/8')
                        if failFindTimes > 8:
                            break

                        if failFindTimes > 2:
                            self.dailyTask.角色信息检查()
                            self.dailyTask.世界聊天检查()

        sleep(0.2)

    def 圣兽试炼(self):
        if 功能开关["圣兽试炼"] == 0 or 任务记录["圣兽试炼"] == 1:
            return

        re = self.进入笔记()
        if not re:
            return

        Toast('日常-圣兽试炼挑战')

        re = CompareColors.compare("479,598,#F3C3FB|528,647,#C39D8C|512,689,#F5E1B2|581,571,#E5D1C1|633,617,#9A94A1")
        if re:
            tapSleep(567, 629, 1.2)
        if not re:
            re = TomatoOcrTap(433, 741, 577, 784, '每日活动', match_mode='fuzzy', sleep1=1.3)
        if not re:
            Toast('日常-每日活动未开启')
            sleep(0.5)
            return

        Toast('日常-进入每日活动')
        re = TomatoOcrTap(14, 329, 205, 381, '圣兽试炼', sleep1=1.3)
        if re:
            Toast('进入圣兽试炼')
        if not re:
            Toast('圣兽试炼未开启')
            return

        # 领取每日奖励
        re = FindColors.find("282,899,#E45454|293,901,#DF5151|290,898,#FFFFFF", rect=[25, 858, 697, 992], diff=0.95)
        if re:
            Toast('圣兽试炼-领取每日奖励')
            tapSleep(re.x - 5, re.y + 5)
            tapSleep(355, 1144)  # 点击空白
            任务记录["圣兽试炼"] = 1

        # 领取击破记录奖励
        re = CompareColors.compare("503,1197,#E15353|509,1196,#FEFDFD|512,1196,#DD4D4D")
        if re:
            tapSleep(422, 1213)  # 点击排行榜
        re = CompareColors.compare("681,44,#DD5555|687,42,#F9F0F0|690,42,#E14F4F", diff=0.95)
        if re:
            Toast('圣兽试炼-领取击破奖励')
            tapSleep(656, 67)
            re = FindColors.find("339,721,#DF5454|347,721,#D14545|351,721,#E55353", diff=0.95)
            if re:
                tapSleep(re.x - 30, re.y + 40)
                TomatoOcrTap(293, 978, 422, 1018, '通关', match_mode='fuzzy')
            for k in range(5):
                re = TomatoOcrTap(212, 1201, 279, 1235, '试炼')
                if re:
                    break
                tapSleep(67, 1213)  # 返回

        # 识别是否完成匹配
        # re = CompareColors.compare("571,929,#CCD168|582,928,#CFD268|586,926,#D0D168") # 识别金币宝箱
        # if re:
        #     Toast('圣兽试炼-已完成每日奖励-返回')
        #     tapSleep(73, 1208)
        #     return

        self.副本匹配()

    def 幻想阶梯(self):
        if 功能开关["幻想阶梯"] == 0:
            return

        if 任务记录["幻想阶梯-倒计时"] > 0:
            diffTime = time.time() - 任务记录["幻想阶梯-倒计时"]
            if diffTime < 3 * 60:
                Toast(f'幻想阶梯-倒计时{round((3 * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        任务记录["幻想阶梯-倒计时"] = time.time()

        self.dailyTask.homePage()
        Toast('日常-幻想阶梯挑战')

        re = TomatoOcrFindRangeClick(
            keywords=[{'keyword': '层', 'match_mode': 'fuzzy'}, {'keyword': '完成', 'match_mode': 'fuzzy'}], x1=18,
            y1=770, x2=267, y2=1030)
        if re:
            Toast('日常-幻想阶梯-挑战完成领取')
            tapSleep(356, 1207)  # 点击返回
            tapSleep(356, 1207)

        re = self.进入笔记()
        if not re:
            return

        re = CompareColors.compare("611,254,#BCF3F5|601,284,#BBEEF4|541,290,#1E2826|536,307,#1A2329|609,336,#6EB9BE")
        if re:
            tapSleep(585, 273, 1.2)
        if not re:
            re = TomatoOcrTap(432, 124, 596, 173, '幻想阶梯', match_mode='fuzzy')
        if not re:
            Toast('日常-幻想阶梯未开启')
            sleep(0.5)
            return

        # re = TomatoOcrTap(271, 160, 449, 211, '月影之森')
        # if re:
        #     Toast('幻想阶梯-进入月影之森')
        # if not re:
        #     Toast('幻想阶梯-未找到关卡入口')
        #     return

        tapSleep(343, 280)  # 进入默认关卡

        re = CompareColors.compare("685,1199,#E15151|690,1196,#F5E7E7|694,1196,#E35454")  # 匹配馈赠红点
        if re:
            Toast('幻想阶梯-馈赠领取')
            self.dailyTask.馈赠领取()
        tapSleep(246, 1221)  # 点击阶梯

        re = FindColors.find("561,176,#D44545|564,176,#FFFFFF|567,176,#CA4949", rect=[6, 113, 704, 1150],
                             diff=0.95)
        if not re:
            Toast('幻想阶梯-未达到推荐战力-尝试挑战')
            re = FindColors.find("569,442,#CDD067|579,447,#D0D368|665,435,#D2D569|666,459,#D2D568",
                                 rect=[520, 142, 692, 1144], diff=0.93)
            if re:
                tapSleep(re.x, re.y, 3)
        else:
            Toast('日常-幻想阶梯-开始挑战')
            tapSleep(re.x, re.y, 3)
        if not re:
            Toast('幻想阶梯-无法挑战')
            return

        self.战斗检查()
        tapSleep(77, 1212)
        tapSleep(77, 1212)
        tapSleep(77, 1212)

    def 混沌侵袭(self):
        if 功能开关["混沌侵袭"] == 0 or 任务记录["混沌侵袭"] == 1:
            return

        Toast('混沌侵袭-任务开始')
        self.dailyTask.homePage()
        re = TomatoOcrFindRangeClick(
            keywords=[{'keyword': '混沌', 'match_mode': 'fuzzy'}, {'keyword': '侵袭', 'match_mode': 'fuzzy'}], x1=603,
            y1=108, x2=705, y2=434, sleep1=3, offsetX=10, offsetY=-10)
        if not re:
            Toast('混沌侵袭-未找到活动入口')
            return

        Toast('混沌侵袭-开始')
        re = FindColors.find("657,776,#E15252|665,776,#D24747", rect=[24, 743, 698, 875], diff=0.9)
        if re:
            Toast('混沌侵袭-领取活动奖励')
            tapSleep(re.x - 5, re.y + 5, 1.5)
            tapSleep(368, 1265)  # 点击空白处
        任务记录["混沌侵袭"] = 1

    def 素材秘境(self):
        if 功能开关["素材秘境"] == 0 or 任务记录["素材秘境"] == 1:
            return

        Toast('素材秘境-任务开始')
        re = self.进入笔记()
        if not re:
            return
        re = CompareColors.compare("157,991,#EEE6BA|172,1021,#F0ECDD|252,989,#836651|240,1046,#B68A5D|208,1076,#A4A195")
        if not re:
            Toast('日常-素材秘境未开启')
            sleep(0.5)
            return

        Toast('日常-进入素材秘境')
        tapSleep(189, 1008, 1.5)
        for k in range(10):
            re = FindColors.find("337,195,#58B4E1|335,173,#41A4D5", rect=[37, 116, 713, 720], diff=0.9)
            if not re:
                re = FindColors.find("328,176,#E35353|329,186,#DF5454|336,183,#FFFFFF", rect=[14, 112, 700, 1114],
                                     diff=0.9)

            if re:
                Toast('素材秘境-开始采集')
                tapSleep(re.x - 30, re.y + 50)
                re = CompareColors.compare("685,1194,#DC5151|689,1196,#FFFFFF|693,1194,#DC4C4C")
                if re:
                    Toast('素材秘境-馈赠领取')
                    self.dailyTask.馈赠领取()
                tapSleep(244, 1212)
                failTimes = 0
                for m in range(30):
                    re, count = TomatoOcrText(381, 959, 416, 983, '剩余次数')
                    count = safe_int_v2(count)
                    if count == 0:
                        failTimes = failTimes + 1
                    if failTimes > 6:
                        Toast(f'素材秘境-采集完成')
                        break
                    Toast(f'素材秘境-采集中-剩余{count}次')
                    tapSleep(359, 928, 0.2)
                tapSleep(80, 1207)  # 返回
            任务记录["素材秘境"] = 1

    def 每日副本(self):
        if 功能开关["日常副本"] == 0:
            return

        re = self.进入日常副本()
        if not re:
            return

        re = CompareColors.compare("682,1191,#E65555|695,1193,#E25252")
        if re:
            Toast('日常副本-馈赠领取')
            self.dailyTask.馈赠领取()
            TomatoOcrTap(263, 1201, 320, 1235, '副本')

        needFightCt = safe_int_v2(功能开关['日常副本重复挑战次数'])
        if needFightCt == 0:
            needFightCt = 2
        for k in range(needFightCt):
            if 功能开关['副本地图'] == "世界之树":
                Toast(f'日常副本-世界之树')
                re = TomatoOcrTap(472, 243, 516, 291, '树', sleep1=2, match_mode='fuzzy')
                if not re:
                    re = TomatoOcrFindRangeClick('树', sleep1=2, match_mode='fuzzy', x1=91, y1=216, x2=596, y2=1071)
                if not re:
                    swipe(342, 265, 343, 1023, dur=600)
                    sleep(1.5)
                    re = TomatoOcrTap(472, 243, 516, 291, '树', sleep1=2, match_mode='fuzzy')
            elif 功能开关['副本地图'] == "机神山":
                Toast(f'日常副本-机神山')
                re = TomatoOcrTap(221, 551, 486, 617, '机', sleep1=2, match_mode='fuzzy')
                if not re:
                    re = TomatoOcrFindRangeClick('机', sleep1=2, match_mode='fuzzy', x1=91, y1=216, x2=596, y2=1071)
                if not re:
                    swipe(342, 265, 343, 1023, dur=600)
                    sleep(1.5)
                    re = TomatoOcrTap(221, 551, 486, 617, '机', sleep1=2, match_mode='fuzzy')
            elif 功能开关['副本地图'] == "海之宫遗迹":
                Toast(f'日常副本-海之宫遗迹')
                re = TomatoOcrTap(146, 203, 570, 265, '海', sleep1=2, match_mode='fuzzy')
                if not re:
                    re = TomatoOcrTap(144, 195, 215, 268, '海', sleep1=2, match_mode='fuzzy')
                if not re:
                    re = TomatoOcrFindRangeClick('海', sleep1=2, match_mode='fuzzy', x1=91, y1=216, x2=596, y2=1071)
            elif 功能开关['副本地图'] == "源水大社":
                Toast(f'日常副本-源水大社')
                re = TomatoOcrTap(285, 558, 343, 618, '水', sleep1=2, match_mode='fuzzy')
                if not re:
                    swipe(343, 923, 342, 365, dur=300)
                    sleep(0.6)
                    re = TomatoOcrTap(288, 563, 342, 615, '水', sleep1=2, match_mode='fuzzy')
                if not re:
                    re = TomatoOcrFindRangeClick('水', sleep1=2, match_mode='fuzzy', x1=91, y1=216, x2=596, y2=1071)
            elif 功能开关['副本地图'] == "黄泉阁":
                Toast(f'日常副本-黄泉阁')
                re = TomatoOcrTap(332, 915, 384, 964, '泉', sleep1=2, match_mode='fuzzy')
                if not re:
                    swipe(343, 923, 342, 365, dur=300)
                    sleep(0.6)
                    re = TomatoOcrTap(332, 915, 384, 964, '泉', sleep1=2, match_mode='fuzzy')
                if not re:
                    re = TomatoOcrFindRangeClick('泉', sleep1=2, match_mode='fuzzy', x1=91, y1=216, x2=596, y2=1071)
            elif 功能开关['副本地图'] == "封魔峡":
                Toast(f'日常副本-封魔峡')
                re = TomatoOcrTap(332, 915, 384, 964, '魔', sleep1=2, match_mode='fuzzy')
                if not re:
                    swipe(343, 923, 342, 365, dur=300)
                    sleep(0.6)
                    re = TomatoOcrTap(332, 915, 384, 964, '魔', sleep1=2, match_mode='fuzzy')
                if not re:
                    re = TomatoOcrFindRangeClick('峡', sleep1=2, match_mode='fuzzy', x1=91, y1=216, x2=596, y2=1071)
            elif 功能开关['副本地图'] == "默认副本":
                Toast(f'日常副本-默认副本')
                re = FindColors.find("640,501,#A2B776|639,509,#A2B776|672,504,#A1B978|670,510,#A2B778|658,483,#323232",
                                     ori=6)
                if re:
                    tapSleep(re.x, re.y, 2)
                    re = True
            if not re:
                re = self.进入日常副本()
                if not re:
                    return
            if re:
                if 功能开关['副本难度'] == "默认难度":
                    Toast(f'日常副本-默认难度')
                elif 功能开关['副本难度'] == "困难":
                    Toast(f'日常副本-困难难度')
                    re = TomatoOcrTap(528, 1199, 592, 1238, '困难')
                    if not re:
                        re = TomatoOcrTap(394, 1199, 458, 1235, '困难')
                    if not re:
                        re = TomatoOcrTap(331, 1202, 386, 1237, '困难')
                    if not re:
                        re = TomatoOcrFindRangeClick('困难', sleep1=2, match_mode='fuzzy', x1=159, y1=1177, x2=682,
                                                     y2=1250)
                elif 功能开关['副本难度'] == "普通":
                    Toast(f'日常副本-普通难度')
                    re = TomatoOcrTap(261, 1196, 323, 1237, '普通')
                    if not re:
                        re = TomatoOcrTap(211, 1197, 282, 1237, '普通')
                    if not re:
                        re = TomatoOcrTap(188, 1196, 257, 1237, '普通')
                    if not re:
                        re = TomatoOcrFindRangeClick('普通', sleep1=2, match_mode='fuzzy', x1=159, y1=1177, x2=682,
                                                     y2=1250)
                elif 功能开关['副本难度'] == "噩梦":
                    Toast(f'日常副本-噩梦难度')
                    re = TomatoOcrTap(581, 1201, 637, 1235, '噩梦')
                    if not re:
                        re = TomatoOcrTap(461, 1201, 527, 1237, '噩梦')
                    if not re:
                        re = TomatoOcrFindRangeClick('噩梦', sleep1=2, match_mode='fuzzy', x1=159, y1=1177, x2=682,
                                                     y2=1250)
                elif 功能开关['副本难度'] == "炼狱":
                    Toast(f'日常副本-炼狱难度')
                    re = TomatoOcrTap(600, 1199, 664, 1240, '炼狱')
                    if not re:
                        re = TomatoOcrFindRangeClick('炼狱', sleep1=2, match_mode='fuzzy', x1=159, y1=1177, x2=682,
                                                     y2=1250)

                Toast(f'第{k + 1}/{needFightCt}次挑战')
                self.副本匹配()

    def 进入日常副本(self):
        Toast('每日副本-开始')

        re = self.进入笔记()
        if not re:
            return False

        # 检测剩余次数
        re, count = TomatoOcrText(125, 173, 173, 198, '剩余次数')
        count = safe_int(count.replace('/2', ''))
        if count == 0 and 功能开关["无次数继续"] == 0:
            Toast('每日副本次数已用完')
            return False

        re = CompareColors.compare("153,244,#324C6C|198,236,#2C4540|225,344,#FEFFFF|216,358,#83B2D1|235,353,#EBF6FB")
        if re:
            tapSleep(192, 274, 1.5)  # 点击日常副本
        if not re:
            re = TomatoOcrTap(14, 124, 159, 170, '日常', match_mode='fuzzy')
        if not re:
            Toast('日常副本未开启')
            return False

        Toast('日常-进入日常副本')
        return True

    def 副本匹配(self):
        re = TomatoOcrTap(502, 1077, 572, 1114, '匹配')
        if not re:
            re = TomatoOcrTap(500, 1077, 574, 1114, '匹配')
            if not re:
                Toast('当前状态不可匹配')
                return

        Toast('开始匹配')
        failTimes = 0
        totalWait = 200  # 30000 毫秒 = 30 秒
        start_time = int(time.time())
        while True:
            re, _ = TomatoOcrText(477, 1074, 600, 1114, '取消匹配')
            if not re:
                failTimes = failTimes + 1
                Toast(f'匹配失败{failTimes}/10')
            if failTimes > 10:
                Toast('匹配失败，返回')
                break

            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed > totalWait:
                re = TomatoOcrTap(477, 1074, 600, 1114, '取消', match_mode='fuzzy')
                Toast('匹配超时，取消匹配')
                break

            Toast(f'匹配中{elapsed}/200s')
            re = TomatoOcrTap(486, 1083, 554, 1121, '接受')
            if re:
                self.副本战斗()
                break
            sleep(0.5)

    def 副本战斗(self):
        startFight = False
        waitFightCt = 0
        while True:
            re = TomatoOcrTap(486, 1083, 554, 1121, '接受')
            startFight = TomatoOcrTap(322, 934, 394, 975, '准备', sleep1=2)
            Toast('准备战斗')
            if startFight:
                break
            re, waitNum = TomatoOcrText(280, 992, 438, 1035, '剩余', match_mode='fuzzy')
            if not re:
                Toast(f'进入匹配失败{waitFightCt}/8')
                waitFightCt = waitFightCt + 1
            else:
                Toast(f'匹配成功,等待进入挑战-{waitNum}')
                waitFightCt = 0
            if waitFightCt > 8:
                Toast(f'进入匹配失败{waitFightCt}/5-返回')
                re = TomatoOcrTap(477, 1074, 600, 1114, '取消匹配')
                break
            sleep(1)
        if not startFight:
            Toast('开始战斗失败-返回')
            return startFight

        for l in range(30):
            startFight, _ = TomatoOcrText(277, 932, 446, 980, '取消准备')
            Toast(f'等待队友准备{l}/30')
            if not startFight:
                break
            sleep(1)

        Toast('开始战斗')
        failTimes = 0
        start_time = int(time.time())
        while True:
            self.战斗喊话()
            re = CompareColors.compare("39,926,#DFDEDA|39,915,#DFDEDA|52,915,#DFDEDA|60,920,#E0DFDB")
            if not re:
                re = CompareColors.compare("39,920,#B7B7B7|47,920,#B7B7B7|47,924,#B7B7B7|60,923,#B7B7B7")
            if not re:
                re, _ = TomatoOcrText(263, 296, 456, 342, '房间', match_mode='fuzzy')  # 副本房间地图-等待页
                if re:
                    Toast('等待选择房间')
                    re = FindColors.find("496,654,#CCCF68|496,661,#CCCF68|495,672,#CCCF68", rect=[131, 252, 633, 1052],
                                         diff=0.9)
                    if re:
                        Toast('自动选择房间')
                        tapSleep(re.x + 5, re.y + 5)
                if not re:
                    Toast(f'战斗状态识别失败{failTimes}/10')
                    sleep(1)
                    failTimes = failTimes + 1
            else:
                failTimes = 0

            if failTimes > 10:
                Toast('战斗结束')
                tapSleep(337, 1231)
                break

            # 世界树战斗结束
            re1, _ = TomatoOcrText(494, 1196, 611, 1232, '领取', match_mode='fuzzy')
            re2 = False
            if not re1:
                re2, _ = TomatoOcrText(22, 801, 146, 842, '掉落', match_mode='fuzzy')
            if re1 or re2:
                if 功能开关['不开宝箱'] == 0:
                    re, tili = TomatoOcrText(587, 1142, 634, 1169, '领奖次数')
                    if tili == "0/2":
                        # 判断是否可购买体力
                        needCt = safe_int_v2(功能开关["日常副本补充次数"])
                        if re1 and needCt > 0:
                            re = TomatoOcrTap(494, 1196, 611, 1232, '领取', match_mode='fuzzy', sleep1=1.5)
                            if re:
                                re, buyCt = TomatoOcrText(524, 683, 565, 708, '限购次数')
                                buyCt = safe_int_v2(buyCt.replace('/2', ''))
                                if buyCt >= needCt:
                                    Toast(f'已购买{buyCt}/needCt次-跳过购买')
                                    Toast('战斗结束-购买次数用尽-返回房间')
                                    tapSleep(235, 1204, 1.2)  # 返回
                                    tapSleep(64, 1220, 1.2)  # 返回
                                    TomatoOcrTap(457, 721, 525, 754, '确定', sleep1=1.5)
                                    break
                                else:
                                    Toast(f'购买次数-{buyCt}/{needCt}次')
                                    TomatoOcrTap(461, 724, 522, 763, '购买', sleep1=1.5)
                        else:
                            Toast('战斗结束-奖励次数用尽-返回房间')
                            tapSleep(64, 1220, 1.2)  # 返回
                            TomatoOcrTap(457, 721, 525, 754, '确定', sleep1=1.5)
                            break
                    re = CompareColors.compare(
                        "398,232,#CED168|387,205,#222222|364,187,#222222|337,214,#222222|387,277,#222222|359,312,#222222|320,280,#222222")  # S宝箱
                    if 功能开关["仅S评开启"] == 1 and not re:
                        Toast('非S评宝箱-跳过开启')
                    else:
                        re = TomatoOcrTap(494, 1196, 611, 1232, '领取', match_mode='fuzzy', sleep1=1.5)
                        Toast('战斗结束-开启宝箱')
                        TomatoOcrTap(457, 721, 525, 754, '确定', sleep1=1.5)
                else:
                    Toast('战斗结束-不开宝箱')
                tapSleep(64, 1220)  # 返回
                TomatoOcrTap(457, 721, 525, 754, '确定', sleep1=1.5)
                break

            # 圣兽战斗结束
            re3 = TomatoOcrTap(299, 274, 421, 312, '结束', match_mode='fuzzy')
            if re3:
                Toast('圣兽试炼-战斗结束')
                tapSleep(354, 1226, 1.5)  # 返回房间
                # 领取每日奖励
                re = FindColors.find("282,899,#E45454|293,901,#DF5151|290,898,#FFFFFF", rect=[25, 858, 697, 992],
                                     diff=0.95)
                if re:
                    Toast('圣兽试炼-领取每日奖励')
                    tapSleep(re.x - 5, re.y + 5)
                    tapSleep(355, 1144)  # 点击空白
                break

            re = TomatoOcrTap(325, 935, 385, 972, '准备')
            if re:
                Toast('战斗中-准备')
                failTimes = 0

            current_time = int(time.time())
            elapsed = current_time - start_time
            if elapsed > 650:
                Toast('战斗超时-退出')
                break
            sleep(0.5)
            Toast(f'战斗中{elapsed}/650s')
        return startFight

    def 进入笔记(self):
        self.dailyTask.homePage()
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

    def 战斗检查(self):
        re = FindColors.find("292,568,#FEF9C9|303,568,#FCF6C9|303,578,#FEF6C5")  # 魔物阻挡
        if re:
            Toast('魔物阻挡')
            tapSleep(re.x - 30, re.y + 30, 2)

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

    def 战斗喊话(self):
        if 功能开关['队伍喊话'] == "":
            return

        need_dur_minute = safe_int_v2(
            功能开关.get("队伍喊话间隔", 0).replace("分钟", "").replace("分", "").replace("秒", "").replace("s",
                                                                                                            ""))  # 分钟
        if need_dur_minute == 0:
            need_dur_minute = 1  # 默认1分钟
        if 任务记录["队伍喊话-倒计时"] > 0:
            diffTime = time.time() - 任务记录["队伍喊话-倒计时"]
            if diffTime < need_dur_minute * 60:
                Toast(f'队伍喊话-倒计时{round((need_dur_minute * 60 - diffTime) / 60, 2)}min')
                sleep(1.5)
                return

        tapSleep(58, 1112)  # 点击左下角喊话
        if 功能开关["副本自动接收邀请"]:
            re = TomatoOcrFindRangeClick('队伍', x1=14, y1=511, x2=85, y2=1161, sleep1=1.3)
        else:
            re = TomatoOcrTap(22, 793, 74, 817, '战场', sleep1=1.3)
            if not re:
                re = TomatoOcrTap(22, 686, 77, 711, '战场', sleep1=1.3)
            if not re:
                re = TomatoOcrTap(20, 684, 75, 714, '战场', sleep1=1.3)
            if not re:
                re = TomatoOcrFindRangeClick('战场', x1=14, y1=511, x2=85, y2=1161, sleep1=1.3)
        if not re:
            Toast("未识别到战场喊话入口")
            任务记录["队伍喊话-倒计时"] = time.time()
            self.dailyTask.世界聊天检查()
            return
        Toast("开始队伍喊话")
        任务记录["队伍喊话-倒计时"] = time.time()
        contentArr = []
        if 功能开关['队伍喊话'] != "":
            contentArr.append(功能开关['队伍喊话'])
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
                    Toast('队伍喊话-尝试重新输入')
                    action.input(content)
                    action.Key.back()  # 模拟返回键确认输入
                    sleep(0.3)
                isFaSong = False
                for k in range(4):
                    re, shuru = TomatoOcrText(99, 1210, 268, 1245, "聊天", match_mode='fuzzy')
                    if shuru and isFaSong:
                        Toast('队伍喊话-已发送')
                        break
                    isFaSong = TomatoOcrTap(610, 1210, 669, 1243, "发", 10, 10, match_mode='fuzzy')
                    sleep(0.3)
                任务记录["队伍喊话-倒计时"] = time.time()
            else:
                Toast('队伍喊话-尝试清空输入框')
                res = TomatoOcrTap(610, 1210, 669, 1243, "发", 10, 10, match_mode='fuzzy')
                sleep(0.3)
        self.dailyTask.世界聊天检查()

        if 功能开关['发送随机表情'] == 1:
            # 发送表情
            tapSleep(673, 1010)  # 点击表情
            tapSleep(264, 883)  # 嗨
