# 导包
import time

from ascript.android import system

from .特征库 import *
from ascript.android.ui import Dialog
from .baseUtils import *
from .res.ui.ui import 功能开关, 任务记录
from .fuBen import FuBenTask
from .daily import DailyTask
from ascript.android.screen import FindColors
import pymysql
import threading

fuBenTask = FuBenTask()
dailyTask = DailyTask()


# 实例方法
def main():
    global checkZBTime
    global checkQuitTeamTime
    checkZBTime = time.time()  # 兜底接收准备页面
    checkQuitTeamTime = time.time()  # 退队检查倒计时
    while True:
        if 功能开关["副本自动接收邀请"] == 1:
            if 功能开关["fighting"] == 0:
                Toast('等待组队邀请')
                waitInvite()
        sleep(1)  # 等待 5 秒


def waitInvite():
    tmpBx = 功能开关["不开宝箱"]
    功能开关["不开宝箱"] = 1

    global checkZBTime
    global checkQuitTeamTime
    res1, _, _ = TomatoOcrFindRange(
        keywords=[{'keyword': '同', 'match_mode': 'fuzzy'}, {'keyword': '意', 'match_mode': 'fuzzy'}], x1=217,
        y1=883, x2=402, y2=954)
    res2 = False
    res3 = False
    if time.time() - checkZBTime > 5:
        res2, _ = TomatoOcrText(491, 1086, 551, 1120, "接受")  # 接受准备
        checkZBTime = time.time()

    fight_type = ''
    if not res1 and not res2 and not res3:
        checkQuitTeamTime = time.time()
        return

    if res1:
        功能开关["fighting"] = 1
        功能开关["needHome"] = 0
        resFightName, 任务记录["战斗-关卡名称"] = TomatoOcrText(85, 923, 258, 950, "关卡名称")  # 关卡名称
        resTeamName, 任务记录["战斗-房主名称"] = TomatoOcrText(80, 856, 144, 885, "房主名称")  # 房主名称
        Toast(f'{任务记录["战斗-关卡名称"]}-{任务记录["战斗-房主名称"]}')
        # 黑名单判断
        blackList = 功能开关['副本带队黑名单']
        blackList = blackList.split('|')
        for black in blackList:
            if black == '':
                continue
            if black in 任务记录["战斗-关卡名称"] or black in 任务记录["战斗-房主名称"]:
                Toast('命中黑名单，拒绝组队邀请')
                res1 = TomatoOcrTap(242, 910, 296, 940, "拒绝", offsetX=3, offsetY=3)
                功能开关["fighting"] = 0
                return

        res1 = TomatoOcrFindRangeClick(
            keywords=[{'keyword': '同', 'match_mode': 'fuzzy'}, {'keyword': '意', 'match_mode': 'fuzzy'}], x1=217,
            y1=883, x2=402, y2=954, offsetX=3, offsetY=3)

    waitFight = False
    findDoneStatus = False
    teamShout = False
    totalWait = 50
    checkYaoQingTime = time.time()  # 兜底检查邀请玩家页面
    if 功能开关["自动离房等待时间"] != "":
        totalWait = safe_int_v2(功能开关["自动离房等待时间"])
    start_time = int(time.time())
    for i in range(200):
        current_time = int(time.time())
        elapsed = current_time - start_time
        if elapsed >= totalWait:
            Toast(f'等待进入战斗超时，退出组队')
            break

        # 兜底，已在队伍中时，停止返回操作
        功能开关["fighting"] = 1
        功能开关["needHome"] = 0

        # 行李页，返回首页
        Toast(f'{fight_type}-等待队长开始{elapsed}/{totalWait}s')

        # 兜底，已在队伍中时，停止返回操作
        功能开关["fighting"] = 1
        功能开关["needHome"] = 0

        # 返回房间
        failTeam = 0
        for j in range(18):
            # 战斗结束治疗
            re = TomatoOcrTap(400, 800, 511, 832, '治疗', match_mode='fuzzy')
            if re:
                Toast("战斗结束 - 一键治疗")

            res1 = FindColors.find("56,277,#CDD068|63,278,#CCD068|50,284,#CED167|52,293,#B5B562",
                                   rect=[11, 116, 110, 726], diff=0.9)
            if not res1:
                res1 = FindColors.find("52,340,#CED16A|50,346,#D0D06B|52,357,#CDCF6A|63,347,#CED168|69,354,#CDD068",
                                       rect=[15, 110, 102, 503], diff=0.93)
            if not res1:
                re1, _ = TomatoOcrText(486, 1083, 554, 1121, '接受')
                if not re1:
                    re1, _ = TomatoOcrText(322, 934, 394, 975, '准备')
                if re1:
                    break
                if not re1:
                    Toast(f'未进入房间{j}/ 15')
                    failTeam = failTeam + 1
            if res1:
                break
            sleep(1)
        if failTeam >= 15:
            re, _ = TomatoOcrText(322, 934, 394, 975, '准备')
            if not re:
                re, _ = TomatoOcrText(486, 1083, 554, 1121, '接受')
                if not re:
                    break

        re1, _ = TomatoOcrText(486, 1083, 554, 1121, '接受')
        re2, _ = TomatoOcrText(322, 934, 394, 975, '准备')
        if re1 or re2:
            waitFight = fuBenTask.副本战斗()
            if waitFight:
                Toast('战斗结束 - 等待下次带队')
                # 战斗结束后不立即返回，先处理队伍中的逻辑
                功能开关["fighting"] = 1
                功能开关["needHome"] = 0
                start_time = int(time.time())

        # 判断队伍已解散
        re = CompareColors.compare(
            "42,156,#CCCF6E|55,157,#222222|58,145,#D3D585|78,157,#C9CE67|55,181,#303842|58,168,#CED072")
        if re:
            Toast("战斗结束 - 队伍已解散")
            break
        sleep(0.5)

    for p in range(2):
        quitTeamRe = dailyTask.homePage(needQuitTeam=True)
        功能开关["fighting"] = 0
    功能开关["不开宝箱"] = tmpBx

    return


def checkFightType():
    fight_type = ''
    res, fightName = TomatoOcrText(377, 582, 592, 615, "关卡类型")
    if fight_type == '' and has_common_chars("恶龙大通缉", fightName, 2):
        fight_type = "恶龙带队"
    if fight_type == '' and has_common_chars("秘境之间", fightName, 2):
        fight_type = "秘境带队"
    if fight_type == '' and has_common_chars("梦魇狂潮", fightName, 2):
        fight_type = "梦魇带队"
    if fight_type == '' and has_common_chars("绝境挑战", fightName, 2):
        fight_type = "绝境带队"
    if fight_type == '' and has_common_chars("终末战", fightName, 2):
        fight_type = "终末战带队"
    if fight_type == '' and has_common_chars("忆战回环", fightName, 2):
        fight_type = "忆战回环带队"
    if fight_type == '' and has_common_chars("大暴走", fightName, 2):
        fight_type = "暴走带队"
    if fight_type == '' and has_common_chars("斗歌会", fightName, 2):
        fight_type = "斗歌会带队"
    if fight_type == '' and has_common_chars("使徒来袭", fightName, 2):
        fight_type = "使徒来袭带队"
    if fight_type == '' and has_common_chars("莱茵幻境", fightName, 2):
        fight_type = "斗歌会带队"
    if fight_type == '' and has_common_chars("桎梏之形", fightName, 2):
        fight_type = "桎梏之形带队"
    if fight_type == '' and has_common_chars("三打三守三魔头", fightName, 2):
        fight_type = "三魔头带队"
    if fight_type == '' and has_common_chars("调查队", fightName, 2):
        fight_type = "调查队带队"

    if fight_type == '':
        for k in range(2):
            if fight_type != '':
                break
            if fight_type == '':
                resELong1, _ = TomatoOcrText(405, 588, 498, 615, "恶龙大通缉")  # 恶龙邀请
                if resELong1:
                    fight_type = "恶龙带队"
                    break
            if fight_type == '':
                resMiJing1, _ = TomatoOcrText(405, 588, 480, 611, "秘境之间")  # 秘境邀请
                if resMiJing1:
                    fight_type = "秘境带队"
                    break
            if fight_type == '':
                resMengYan1, _ = TomatoOcrText(404, 587, 480, 611, "梦魇狂潮")  # 梦魇邀请
                if not resMengYan1:
                    resMengYan1, _ = TomatoOcrText(443, 590, 481, 612, "狂潮")  # 梦魇邀请
                if resMengYan1:
                    fight_type = "梦魇带队"
                    break
            if fight_type == '':
                # bitmap = screen.capture(380, 583, 510, 615)
                # resJueJing1 = TomatoOcrFindRange("绝境挑战", 0.9, 380, 583, 510, 615, match_mode='fuzzy',
                #                                  bitmap=bitmap)  # 绝境邀请
                resJueJing1, _ = TomatoOcrText(405, 589, 480, 612, "绝境挑战")  # 绝境邀请
                if resJueJing1:
                    fight_type = "绝境带队"
                    break
            if fight_type == '':
                # resZhongMo1 = TomatoOcrFindRange("终末战", 0.9, 380, 583, 510, 615, match_mode='fuzzy',
                #                                  bitmap=bitmap)  # 终末战邀请
                resZhongMo1, _ = TomatoOcrText(406, 589, 461, 610, "终末战")  # 绝境邀请
                if resZhongMo1:
                    fight_type = "终末战带队"
                    break
                if fight_type == '':
                    resDiaoCha1 = TomatoOcrFindRange("调查队", 0.9, 380, 583, 510, 615, match_mode='fuzzy')  # 调查队邀请
                    if resDiaoCha1:
                        fight_type = "调查队带队"
                        break
            if fight_type == '':
                res1, _ = TomatoOcrText(404, 587, 480, 611, "忆战回环")  # 忆战回环邀请
                res2, _ = TomatoOcrText(442, 588, 480, 609, "回环")  # 忆战回环邀请
                if res1 or res2:
                    fight_type = "忆战回环带队"
                    break

            if fight_type == '':
                res1, _ = TomatoOcrText(405, 587, 462, 611, "大暴走")  # 大暴走
                res2, _ = TomatoOcrText(460, 614, 498, 637, "大王")  # 大暴走
                if res1 or res2:
                    fight_type = "暴走带队"
                    break

            if 功能开关['斗歌会自动接收邀请'] == 1 and fight_type == '':
                res1, _ = TomatoOcrText(385, 612, 483, 637, "斗歌金元花")  # 斗歌金元花
                res2, _ = TomatoOcrText(407, 591, 461, 610, "斗歌会")  # 斗歌会
                if res1 or res2:
                    fight_type = "斗歌会带队"
                    break

            if fight_type == '':
                res1, _ = TomatoOcrText(442, 588, 479, 609, "之形")  # 桎梏之形
                if res1:
                    fight_type = "桎梏之形带队"
                    break

            if fight_type == '':
                res1, _ = TomatoOcrText(382, 609, 524, 639, "三打三守三魔头")  # 三魔头邀请
                res2, _ = TomatoOcrText(380, 613, 460, 640, "三打三守")  # 三魔头邀请
                if res1 or res2:
                    fight_type = "三魔头带队"
                    break

            # if fight_type == '':
            #     fight_type = '暴走带队'
    return fight_type


def has_common_chars(A, B, min_length=4):
    if A == B:
        return True

    # 将字符串转换为集合以获取唯一字符
    set_A = set(A)
    set_B = set(B)

    # 计算两个集合的交集
    common_chars = set_A.intersection(set_B)

    # 检查交集的大小是否至少为4
    return len(common_chars) >= min_length
