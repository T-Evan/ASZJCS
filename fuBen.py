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
        if 功能开关["副本总开关"] == 0:
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

        # 每日副本
        self.每日副本()

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
            re = TomatoOcrTap(433, 741, 577, 784, '每日活动', match_mode='fuzzy')
        if not re:
            Toast('日常-每日活动未开启')
            sleep(0.5)
            return

        Toast('日常-进入每日活动')
        re = TomatoOcrTap(14, 329, 205, 381, '圣兽试炼')
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

        re = TomatoOcrTap(271, 160, 449, 211, '月影之森')
        if re:
            Toast('幻想阶梯-进入月影之森')
        if not re:
            Toast('幻想阶梯-未找到关卡入口')
            return

        re = CompareColors.compare("685,1199,#E15151|690,1196,#F5E7E7|694,1196,#E35454")  # 匹配馈赠红点
        if re:
            Toast('幻想阶梯-馈赠领取')
            self.dailyTask.馈赠领取()
        tapSleep(246, 1221)  # 点击阶梯

        re = FindColors.find("561,176,#D44545|564,176,#FFFFFF|567,176,#CA4949", rect=[6, 113, 704, 1150],
                             diff=0.95)
        if not re:
            Toast('幻想阶梯-未达到推荐战力-尝试挑战')
            re = TomatoOcrTap(582, 896, 652, 931, '挑战', sleep1=3)
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
            if re:
                Toast('素材秘境-开始采集')
                tapSleep(re.x, re.y)
                for m in range(30):
                    re, count = TomatoOcrText(381, 959, 416, 983, '剩余次数')
                    count = safe_int_v2(count)
                    if count == 0:
                        Toast(f'素材秘境-采集完成')
                        tapSleep(74, 1212, 1)  # 返回
                        break
                    Toast(f'素材秘境-采集中-剩余{count}次')
                    tapSleep(359, 928, 0.2)
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
            Toast(f'日常副本-选择副本')
            if 功能开关['副本地图'] == "世界之树":
                re = TomatoOcrTap(472, 243, 516, 291, '树', sleep1=2)
            elif 功能开关['副本地图'] == "机神山":
                re = TomatoOcrTap(221, 551, 486, 617, '机', sleep1=2, match_mode='fuzzy')
            elif 功能开关['副本地图'] == "海之宫遗迹":
                re = TomatoOcrTap(152, 914, 212, 968, '海', sleep1=2)
            elif 功能开关['副本地图'] == "默认副本":
                Toast(f'日常副本-选择默认副本')
                re = FindColors.find("640,501,#A2B776|639,509,#A2B776|672,504,#A1B978|670,510,#A2B778|658,483,#323232",
                                     ori=6)
                if re:
                    tapSleep(re.x, re.y, 2)
            if not re:
                re = self.进入日常副本()
                if not re:
                    return
            if re:
                if 功能开关['副本难度'] == "默认难度":
                    Toast(f'日常副本-选择默认难度')
                elif 功能开关['副本难度'] == "困难":
                    Toast(f'日常副本-困难难度')
                    re = TomatoOcrTap(528, 1199, 592, 1238, '困难')
                elif 功能开关['副本难度'] == "普通":
                    Toast(f'日常副本-普通难度')
                    re = TomatoOcrTap(261, 1196, 323, 1237, '普通')

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
                Toast(f'进入匹配失败{waitFightCt}/5')
                waitFightCt = waitFightCt + 1
            else:
                Toast(f'匹配成功,等待进入挑战-{waitNum}')
                waitFightCt = 0
            if waitFightCt > 5:
                Toast(f'进入匹配失败{waitFightCt}/5-返回')
                re = TomatoOcrTap(477, 1074, 600, 1114, '取消匹配')
                break
            sleep(1)
        if not startFight:
            Toast('开始战斗失败-返回')
            return

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
            if elapsed > 450:
                Toast('战斗超时-退出')
                break
            sleep(0.5)
            Toast(f'战斗中{elapsed}/450s')
        return

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
