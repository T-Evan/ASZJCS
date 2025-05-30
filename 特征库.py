from ascript.android import plug
from ascript.android.ui import Dialog
from ascript.android.screen import FindImages
# 导入上下文环境包,方便导入图片地址
from ascript.android.system import R
from ascript.android import action
from ascript.android.screen import CompareColors
import time
from .res.ui.ui import switch_lock
from .res.ui.ui import TimeoutLock


def swipe(x1, y1, x2, y2, dur=500):
    # print(x1, y1, x2, y2)
    action.slide(x1, y1, x2, y2, dur)
    # action.Touch.down(x1, y1, dur)
    # action.Touch.move(x2, y2, dur)
    # action.Touch.up(x2, y2, dur)


def click(x, y, dur=200):
    action.click(x, y, dur)

def clickV2(x, y, dur=200):
    action.Touch.down(x, y, dur)
    action.Touch.up(x, y, dur)


def sleep(s):
    time.sleep(s)


def compareColors(colorStr, diff=0.9):
    res = CompareColors.compare(colorStr, diff)
    if res:
        return True
    else:
        return False


def imageFind(name, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, timeLock=10):
    try:
        try:
            # with TimeoutLock(timeLock):
            path = R.res(f"/img/{name}.png")  # 这里替换为你的图片地址
            res = FindImages.find_template(path, [x1, y1, x2, y2], confidence=confidence1)
        except RuntimeError as e:
            print(f"imageFind获取锁超时")
            return False, 0, 0
        if res:
            # 检查 res 中是否有 center_x 和 center_y 键
            if "center_x" in res and "center_y" in res:
                x, y = res["center_x"], res["center_y"]
                print(f"imageFind识别成功: {name}")
                return True, x, y
            else:
                # 如果缺少键，返回默认值
                print(f"imageFind识别失败: {name}")
                return False, 0, 0
        else:
            print(f"imageFind未识别: {name}")
            return False, 0, 0
    except Exception as e:
        print(f"imageFind发生异常: {e}")
        return False, 0, 0


def imageFindAll(name, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, timeLock=10):
    try:
        try:
            # with TimeoutLock(timeLock):
            path = R.res(f"/img/{name}.png")  # 这里替换为你的图片地址
            res = FindImages.find_all_template(path, [x1, y1, x2, y2], confidence=confidence1)
        except RuntimeError as e:
            print(f"imageFind获取锁超时")
            return False, []
        if len(res) > 0:
            print(f"imageFind识别成功: {name}")
            return True, res
        else:
            # 如果缺少键，返回默认值
            print(f"imageFind识别失败: {name}")
            return False, []
    except Exception as e:
        print(f"imageFind发生异常: {e}")
        return False, []


def imageFindClick(name, sleep1=1, confidence1=0.7, x1=0, y1=0, x2=720, y2=1280, offsetX=0, offsetY=0):
    try:
        try:
            # with TimeoutLock():
            path = R.res(f"/img/{name}.png")  # 这里替换为你的图片地址
            res = FindImages.find_template(path, [x1, y1, x2, y2], confidence=confidence1)
        except RuntimeError as e:
            print(f"imageFindClick获取锁超时")
            return False
        if res:
            # 检查 res 中是否有 center_x 和 center_y 键
            if "center_x" in res and "center_y" in res:
                x, y = res["center_x"], res["center_y"]
                click(x + offsetX, y + offsetY)
                sleep(sleep1)
                print(f"imageFindClick识别成功: {name}")
                return True
            else:
                print(f"imageFindClick识别失败: {name}")
                return False
        else:
            print(f"imageFindClick识别错误: {name}")
            return False
    except Exception as e:
        print(f"imageFindClick发生异常: {e}")
        return False

# plug.load("ld")  # 这里是版本号
# try:
#     from ld.android import *
# except Exception as e:
#     Dialog.confirm("初始化完成，请重新启动脚本", "初始化完成")
#
# 特征 = {
#     '启动应用': OcrQuery().mlkitocr_v2().rect_half_bottom().pattern('启动应用'),
#     '启动应用-允许': OcrQuery().mlkitocr_v2().rect_half_bottom().pattern('允许'),
#
#     '登录页-公告': OcrQuery().mlkitocr_v2().rect_half_top().pattern('公告'),
#     '登录页-开始冒险之旅': OcrQuery().paddleocr_v3().rect_half_bottom().pattern('开始冒险之旅'),
#     '登录页-开始冒险': OcrQuery().paddleocr_v3().rect_half_bottom().pattern('开始冒险'),
#
#     '首页-冒险手册': OcrQuery().paddleocr_v3().rect_half_top().rect_half_right().pattern('冒险手册'),
#     '首页-新手试炼': OcrQuery().paddleocr_v3().rect_half_top().rect_half_right().pattern('试炼'),
#     # '首页-冒险': ImageQuery().find_template().rect_half_bottom().img('shouye_maoxian.png'),
#     '首页-冒险': OcrQuery().paddleocr_v3().rect_half_bottom().pattern('^冒险$'),
#     '首页-营地': OcrQuery().paddleocr_v3().rect_half_left().rect_half_bottom().pattern('^营地$'),
#     '首页-挑战首领': ImageQuery().find_template().rect_half_right().img('挑战首领.png'),
#     '首页-新关卡已解锁': OcrQuery().paddleocr_v3().rect_half_top().rect_half_right().pattern('已解锁'),
#     '首页-前往新关卡': ImageQuery().find_template().rect_half_right().img('首页-前往新关卡.png'),
#     # '首页-营地': ImageQuery().find_template().rect_half_bottom().img('首页-营地.png'),
#
#     '营地-旅行活动': OcrQuery().mlkitocr_v2().rect_half_left().rect_half_bottom().pattern('旅行活动'),
#     '营地-仓鼠百货': ImageQuery().find_template().rect_half_top().img('仓鼠百货.png'),
#     '营地-仓鼠百货2': ImageQuery().find_template().rect_half_top().img('仓鼠百货2.png'),
#     '仓鼠百货-仓鼠百货': OcrQuery().mlkitocr_v2().rect(268, 1203, 359, 1236).pattern('仓鼠百货'),
#     '仓鼠百货-免费': OcrQuery().mlkitocr_v2().pattern('免费'),  # 免费金币箱
#     '仓鼠百货-最大': OcrQuery().mlkitocr_v2().pattern('最大'),
#     # '仓鼠百货-购买': OcrQuery().mlkitocr_v2().pattern('购买'),
#     '仓鼠百货-购买': ImageQuery().find_template().img('商店购买.png'),
#     '仓鼠百货-商品已售罄': OcrQuery().mlkitocr_v2().pattern('商品已售罄'),
#     '仓鼠百货-星星经验': ImageQuery().find_template().img('星星经验.png'),
#     '仓鼠百货-全价兽粮': ImageQuery().find_template().img('全价兽粮.png'),
#     '仓鼠百货-超级成长零食三折': ImageQuery().find_template().img('超级成长零食三折.png'),
#     '仓鼠百货-黑烬突破石五折': ImageQuery().find_template().img('黑烬突破石五折.png'),
#     '仓鼠百货-经验补剂五折': ImageQuery().find_template().img('经验补剂五折.png'),
#     '营地-秘宝': ImageQuery().find_template().rect_half_top().img('营地秘宝.png'),
#     '招式创造-能量': ImageQuery().find_template().rect_half_top().img('招式创造能量.png').confidence(0.8),
#     '招式创造-能量2': ImageQuery().find_template().rect_half_top().img('招式创造能量2.png').confidence(0.8),
#     '营地-月签到': ImageQuery().find_template().img('月签到.png'),
#     '营地-月签到-累计奖励': ImageQuery().find_template().img('月签到-累计奖励.png'),
#     '营地-纸飞机': ImageQuery().find_template().img('纸飞机.png'),
#     '活动-登录好礼': ImageQuery().find_template().img('登录好礼.png'),
#     '活动-登录好礼-领取': ImageQuery().find_template().img('活动-登录好礼-领取.png'),
#     '活动-摸鱼': OcrQuery().paddleocr_v3().rect_half_right().pattern('摸鱼'),
#     '活动-摸鱼中': ImageQuery().find_template().img('摸鱼中.png'),
#     '秘宝-能量': ImageQuery().find_template().img('秘宝能量.png').confidence(0.8),
#     # '秘宝-能量': OcrQuery().paddleocr_v3().pattern('x100'),
#     # '秘宝-加号': ImageQuery().find_template().rect_half_top().rect_half_right().img('秘宝加号.png'),
#     '秘宝-补充能源': OcrQuery().paddleocr_v3().rect_half_top().rect_half_right().pattern('补充能源'),
#     '秘宝-暗月深林': ImageQuery().find_template().img('暗月深林.png'),
#     '秘宝-艾特拉火山': ImageQuery().find_template().img('艾特拉火山.png'),
#     '秘宝-鲁尔绿洲': ImageQuery().find_template().img('鲁尔绿洲.png'),
#     '秘宝-燃烧塔': ImageQuery().find_template().img('燃烧塔.png'),
#     '结伴-当前地图': ImageQuery().find_template().img('当前地图.png'),
#     '结伴-当前地图2': ImageQuery().find_template().img('当前地图2.png'),
#     '结伴-组队增益': ImageQuery().find_template().img('组队增益.png'),
#     '结伴-加入': ImageQuery().find_template().img('结伴-加入.png'),
#     '手册-领取': ImageQuery().find_template().img('手册-领取.png'),
#
#     '旅人-一键强化': ImageQuery().find_template().img('一键强化.png'),
#     '旅人-技能升级': ImageQuery().find_template().img('技能升级.png'),
#     '旅人-最大': OcrQuery().mlkitocr_v2().pattern('最大'),
#     '旅人-猫猫果木': ImageQuery().find_template().img('猫猫果木.png'),
#
#     '旅团-任务': OcrQuery().paddleocr_v3().pattern('旅团任务'),
#     '旅团-捐献': OcrQuery().paddleocr_v3().pattern('捐献'),
#     '旅团-领取': OcrQuery().paddleocr_v3().pattern('领取'),
#     '旅团-唤兽琴弦': ImageQuery().find_template().img('旅团-唤兽琴弦.png'),
#     '旅团-全价兽粮': ImageQuery().find_template().img('旅团-全价兽粮.png'),
#     '旅团-超级成长零食': ImageQuery().find_template().img('旅团-超级成长零食.png'),
#     '旅团-原材料': ImageQuery().find_template().img('旅团-原材料.png'),
#     '旅团-史诗经验': ImageQuery().find_template().img('旅团-史诗经验.png'),
#     '旅团-优秀经验': ImageQuery().find_template().img('旅团-优秀经验.png'),
#     '旅团-普通经验': ImageQuery().find_template().img('旅团-普通经验.png'),
#     '旅团-金币': ImageQuery().find_template().img('旅团-金币.png'),
#     '旅团-最大': OcrQuery().paddleocr_v3().pattern('最大'),
#     '旅团-购买': OcrQuery().paddleocr_v3().pattern('购买'),
#
#     '试炼-秘境之间': ImageQuery().find_template().img('秘境之间.png'),
#     '秘境-创建队伍': ImageQuery().find_template().img('秘境-创建队伍.png'),
#     '秘境-创建队伍2': OcrQuery().paddleocr_v3().pattern('创建队伍'),
#     '秘境-地图-原野': OcrQuery().paddleocr_v3().rect_half_left().pattern('原野'),
#     '秘境-地图-森林': OcrQuery().paddleocr_v3().rect_half_left().pattern('森林'),
#     '秘境-地图-沙漠': OcrQuery().paddleocr_v3().rect_half_left().pattern('沙漠'),
#     '秘境-地图-海湾': OcrQuery().paddleocr_v3().rect_half_left().pattern('海湾'),
#     '秘境-地图-深林': OcrQuery().paddleocr_v3().rect_half_left().pattern('深林'),
#     '秘境-地图-冰原': OcrQuery().paddleocr_v3().rect_half_left().pattern('冰原'),
#     '秘境-地图-火山': OcrQuery().paddleocr_v3().rect_half_left().pattern('火山'),
#     '秘境-地图-高原': OcrQuery().paddleocr_v3().rect_half_left().pattern('高原'),
#     '秘境-地图-绿洲': OcrQuery().paddleocr_v3().rect_half_left().pattern('绿洲'),
#     '秘境-地图-火原': OcrQuery().paddleocr_v3().rect_half_left().pattern('火原'),
#     '秘境-地图-下城': OcrQuery().paddleocr_v3().rect_half_left().pattern('下城'),
#     '秘境-地图-上城': OcrQuery().paddleocr_v3().rect_half_left().pattern('上城'),
#     '秘境-地图-万象': OcrQuery().paddleocr_v3().rect_half_left().pattern('万象'),
#     '秘境-地图-旷野': OcrQuery().paddleocr_v3().rect_half_left().pattern('旷野'),
#     '秘境-地图-悬崖': OcrQuery().paddleocr_v3().rect_half_left().pattern('悬崖'),
#     '秘境-地图-群岛': OcrQuery().paddleocr_v3().rect_half_left().pattern('群岛'),
#     '秘境-匹配中': OcrQuery().paddleocr_v3().pattern('匹配中'),
#     '试炼-恶龙大通缉': ImageQuery().find_template().img('恶龙大通缉.png'),
#     '恶龙-开始匹配': OcrQuery().paddleocr_v3().pattern('开始匹配'),
#     '恶龙-开始匹配2': OcrQuery().mlkitocr_v2().pattern('开始匹配'),
#     '恶龙-宝箱已开启': ImageQuery().find_template().img('恶龙-宝箱已开启.png'),
#
#     '暴走-烈焰-橙色': ColorQuery("347,370,#78441B|375,370,#784C26|382,361,#775745|372,351,#F09E3A|348,355,#B2722A").rect(206,306,533,438).diff(0.85),
#     '暴走-烈焰-紫色': ColorQuery("374,353,#A54DE9").rect(206,306,533,438).diff(0.9),
#     '暴走-烈焰-紫色2': ColorQuery("375,369,#47366A|374,356,#BE74F7|345,358,#A653EC").rect(206,306,533,438).diff(0.9),
#     '暴走-水地块': ImageQuery().find_template().rect(333,647,639,913).confidence(0.8).img('地标-水.png'),
#     '暴走-水地块2': ImageQuery().find_template().rect(333,647,639,913).confidence(0.8).img('地标-水2.png'),
#     '暴走-水地块3': ImageQuery().find_template().rect(333,647,639,913).confidence(0.8).img('地标-水3.png'),
#
#     '战斗-准备': OcrQuery().mlkitocr_v2().pattern('^准备$'),
#     '战斗-开启挑战': OcrQuery().mlkitocr_v2().pattern('^开启挑战$'),
#     '战斗-确定': OcrQuery().mlkitocr_v2().pattern('^确定$'),
#     '战斗-开始': OcrQuery().mlkitocr_v2().pattern('^开始$'),
#     '战斗中-等级': OcrQuery().mlkitocr_v2().rect_half_left().rect_half_top().pattern('等级'),
#     '战斗中-你被击败了': OcrQuery().mlkitocr_v2().pattern('你被击败了'),
#     '战斗中-放弃': OcrQuery().mlkitocr_v2().pattern('放弃'),
#     '战斗中-队伍': OcrQuery().mlkitocr_v2().rect_half_right().pattern('队伍'),
#     '战斗中-喊话': ImageQuery().find_template().rect_half_right().img('战斗-喊话.png'),
#     '战斗结束-宝箱尚未开启': OcrQuery().mlkitocr_v2().pattern('宝箱尚未开启'),
#     '战斗结束-通关奖励': OcrQuery().mlkitocr_v2().pattern('通关奖励'),  # 战斗结束页，宝箱提示
#     '战斗结束-开启': OcrQuery().mlkitocr_v2().pattern('开启'),  # 结算页，宝箱提示
#     '战斗结束-是否开启': OcrQuery().mlkitocr_v2().pattern('是否开启'),  # 结算页，宝箱提示
#     '战斗结束-点赞': ImageQuery().find_template().rect_half_top().img('dianzan.png'),
#     '战斗结束-开启宝箱': ImageQuery().find_template().rect_half_bottom().img('宝箱-开启.png'),
#     '战斗结束-开启宝箱2': ImageQuery().find_template().img('宝箱-开启2.png'),
#     '战斗结束-自动准备': OcrQuery().mlkitocr_v2().rect_half_bottom().pattern('自动准备'),  # 战斗结束页，自动准备提示 -- 快速返回房间
#     '战斗结束-点赞队友1': ImageQuery().find_template().rect_half_top().img('点赞1.png'),
#     '战斗结束-点赞队友2': ImageQuery().find_template().rect_half_top().img('点赞2.png'),
#
#     '首页-正在组队': OcrQuery().mlkitocr_v2().rect_half_right().pattern('^正在组队$'),
#     '首页-匹配中': OcrQuery().mlkitocr_v2().rect_half_right().pattern('^匹配中$'),
#     '队伍-匹配中': OcrQuery().mlkitocr_v2().pattern('^匹配中$'),
#     '队伍-匹配中2': ImageQuery().find_template().img('队伍-匹配中.png'),
#     '队伍-离开队伍': OcrQuery().mlkitocr_v2().rect_half_top().rect_half_right().text('^离开队伍$'),
#
#     '全屏-确定': OcrQuery().mlkitocr_v2().pattern('^确定$'),
#     '全屏-确认': OcrQuery().mlkitocr_v2().pattern('^确认$'),
#
#     '返回-1': OcrQuery().mlkitocr_v2().rect(7, 1066, 216, 1273).pattern('返回'),
#     '返回-2': ImageQuery().find_template().rect_half_left().rect_half_bottom().img('返回_1.png'),
#     '返回-3': OcrQuery().mlkitocr_v2().rect(7, 1066, 216, 1273).pattern('回'),
#     '返回-4': ImageQuery().find_template().rect_half_left().rect_half_bottom().img('返回_2.png'),
#
#     '点击空白处-1': OcrQuery().mlkitocr_v2().rect_half_bottom().pattern('空白处'),
#
# }
# ldC = 零动框架(特征)
# ldE = LDFramework(特征)
