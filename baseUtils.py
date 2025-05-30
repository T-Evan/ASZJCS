# 导包
import json

from .特征库 import *
from ascript.android.ui import Dialog
from .tomato_ocr import tomatoOcr
from ascript.android import screen
from .res.ui.ui import switch_lock
# from .res.ui.ui import switch_ocr_apk_lock
from ascript.android.system import R
from ascript.android import plug
from .res.ui.ui import TimeoutLock
from ascript.android.screen import Ocr
from .res.ui.ui import 任务记录
import random


# plug.load("BDS_OcrText")
# from BDS_OcrText import *

# # 导入http模块
# import requests
#
# # 指定下载文件的地址
# url = 'https://www.baidu.com/img/flexible/logo/pc/result@2.png' # 目标下载链接
# # 通过get获取数据
# r = requests.get(url)
#
# # 保存文件至sd卡下的1.png
# with open (R.res("/OcrText.apk"), 'wb') as f:
#     f.write(r.content)

# ocr = BDS_OcrText('rcgd5ncvb5ywtge2mzqqzte6kcf9qbyt', R.res("/OcrText.apk"), 2)


# def ocrFind(keyword, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280):
#     if TimeoutLock(switch_lock).acquire_lock():
#         ocrRe = ocr.ocr_result([[x1, y1, x2, y2]])
#         TimeoutLock(switch_lock).release_lock()
#     else:
#         print(f"ocrFind获取锁超时-{keyword}")
#         return False
#     center_x = 0
#     center_y = 0
#     # 遍历 data['lines'] 列表
#     for line in ocrRe['lines']:
#         # 检查每行的 text 是否等于 '4'
#         if line['text'] == keyword:
#             box = line['box']
#             x1, y1, x2, y2 = box
#             # 计算中心位置
#             center_x = (x1 + x2) / 2
#             center_y = (y1 + y2) / 2
#             print(f"ocrFind识别成功-{keyword}|{center_x}|{center_y}")
#             return True
#     print(f"ocrFind识别失败-{keyword}")
#     return False
#
#
# def ocrFindRange(keyword, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, whiteList='', timeLock=10):
#     try:
#         if whiteList == '':
#             whiteList = keyword
#         if TimeoutLock(switch_lock, timeLock).acquire_lock():
#             # print(f"取锁成功-{keyword}")
#             ocrRe = ocr.ocr_result([], whiteList, x1, y1, x2, y2)
#             TimeoutLock(switch_lock, timeLock).release_lock()
#         else:
#             print(f"ocrFindRange获取锁超时-{keyword}")
#             return False
#         center_x = 0
#         center_y = 0
#         # 遍历 data['lines'] 列表
#         for line in ocrRe['lines']:
#             # 检查每行的 text 是否等于 '4'
#             if line['text'] == keyword:
#                 box = line['box']
#                 rx1, ry1, rx2, ry2 = box
#                 # 计算中心位置
#                 center_x = (rx1 + rx2) / 2
#                 center_y = (ry1 + ry2) / 2
#         if center_x > 0 and center_y > 0:
#             print(f"ocrFindRange识别成功-{keyword}|{center_x}|{center_y}")
#             return True
#         print(f"ocrFindRange识别失败-{keyword}|{ocrRe}")
#         return False
#     except Exception as e:
#         print(f"ocrFindRange发生异常: {e}")
#         return False
#
#
# def ocrFindRangeClick(keyword, sleep1=1, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, whiteList='', timeLock=10):
#     try:
#         if whiteList == '':
#             whiteList = keyword
#         if TimeoutLock(switch_lock, timeLock).acquire_lock():
#             ocrRe = ocr.ocr_result([], whiteList, x1, y1, x2, y2)
#             TimeoutLock(switch_lock, timeLock).release_lock()
#         else:
#             print(f"ocrFindRangeClick获取锁超时-{keyword}")
#             return False
#         center_x = 0
#         center_y = 0
#         # 遍历 data['lines'] 列表
#         for line in ocrRe['lines']:
#             # 检查每行的 text 是否等于 '4'
#             if line['text'] == keyword:
#                 box = line['box']
#                 rx1, ry1, rx2, ry2 = box
#                 # 计算中心位置
#                 center_x = (rx1 + rx2) / 2
#                 center_y = (ry1 + ry2) / 2
#         if center_x > 0 and center_y > 0:
#             tapSleep(center_x + x1, center_y + y1)
#             sleep(sleep1)
#             print(f"ocrFindRangeClick识别成功-{keyword}|{center_x}|{center_y}")
#             return True
#         print(f"ocrFindRangeClick识别失败-{keyword}|{ocrRe}")
#         return False
#     except Exception as e:
#         print(f"ocrFindRangeClick发生异常: {e}")
#         return False
#
#
# def ocrFindClick(keyword, sleep1=1, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280):
#     try:
#         if TimeoutLock(switch_lock).acquire_lock():
#             ocrRe = ocr.ocr_result([[x1, y1, x2, y2]])
#             TimeoutLock(switch_lock).release_lock()
#         else:
#             print(f"ocrFindClick获取锁超时-{keyword}")
#             return False
#         # print(ocrRe)
#         center_x = 0
#         center_y = 0
#         # 遍历 data['lines'] 列表
#         for line in ocrRe['lines']:
#             # 检查每行的 text 是否等于 '4'
#             if line['text'] == keyword:
#                 box = line['box']
#                 x1, y1, x2, y2 = box
#                 # 计算中心位置
#                 center_x = (x1 + x2) / 2
#                 center_y = (y1 + y2) / 2
#         if center_x > 0 and center_y > 0:
#             tapSleep(center_x, center_y)
#             sleep(sleep1)
#             print(f"ocrFindClick识别成功-{keyword}|{center_x}|{center_y}")
#             return True
#         print(f"ocrFindClick识别失败-{keyword}|{ocrRe}")
#         return False
#     except Exception as e:
#         print(f"ocrFindClick发生异常: {e}")
#         return False
#

def TomatoOcrTextRange(confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, whiteList='', timeLock=10, bitmap=''):
    try:
        try:
            with TimeoutLock(timeLock):
                if bitmap == '':
                    ocrRe = tomatoOcr.find_all(
                        license="DMR1H6IXOPL1RVESWHBDZT1MHBZEBFXX|4QCPZJ2CMS75C99YB0LGQANO", remark="仗剑挂机助手",
                        rec_type="ch-3.0", box_type="rect", ratio=1.9, threshold=0.3, return_type='json', ocr_type=3,
                        run_mode='fast', capture=[x1, y1, x2, y2])
                else:
                    ocrRe = tomatoOcr.find_all(
                        license="DMR1H6IXOPL1RVESWHBDZT1MHBZEBFXX|4QCPZJ2CMS75C99YB0LGQANO", remark="仗剑挂机助手",
                        rec_type="ch-3.0", box_type="rect", ratio=1.9, threshold=0.3, return_type='json', ocr_type=3,
                        run_mode='fast', bitmap=bitmap)
            # print(ocrRe)
        except RuntimeError as e:
            print(f"TomatoOcrTextRange获取锁超时")
            return False
        center_x = 0
        center_y = 0
        if ocrRe != "":
            ocrReJson = json.loads(ocrRe)
            # print(f"TomatoOcrTextRange识别成功-{ocrReJson}")
            return True, ocrReJson
        else:
            print(f"TomatoOcrTextRange识别失败")
            return False, []
    except Exception as e:
        print(f"TomatoOcrTextRange发生异常: {e}")
        return False, []


def shijieShoutText():
    res, ocrReJson = TomatoOcrTextRange(x1=61, y1=781, x2=287, y2=1090)
    # print(res, ocrReJson)
    player_messages = {}
    if res:
        current_player = '默认'
        player_messages[current_player] = []
        found_world = False
        for line in ocrReJson:
            words = line.get('words', '')
            if '世界' in words:
                # 提取“世界”后的部分作为玩家名称
                parts = words.split('世界', 1)
                if len(parts) > 1:
                    player_name = parts[1].strip()
                    player_name = (player_name.replace('[', '').replace('【', '').replace('】', '').replace(']', '').
                                   replace('）', '').replace('(', '').replace('（', '').replace('）', '').replace(' ', ''))
                    # print(player_name)
                    if player_name != '':
                        current_player = player_name
                        player_messages[player_name] = []
                        found_world = False
                    else:
                        found_world = True
                else:
                    found_world = True
            elif found_world:
                # 如果未找到“世界”，则将当前行的words内容作为玩家名称
                current_player = words.strip()
                player_messages[current_player] = []
                found_world = False
            elif current_player:
                # 将当前行的words内容添加到当前玩家的发言列表中
                player_messages[current_player].append(words)
    print(player_messages)
    return player_messages


def TomatoOcrFindRange(keyword='T^&*', confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, whiteList='', timeLock=10,
                       match_mode='exact', bitmap='', keywords=None):
    try:
        if whiteList == '':
            whiteList = keyword
        if keywords is None:
            keywords = []
        try:
            with TimeoutLock(timeLock):
                if bitmap == '':
                    ocrRe = tomatoOcr.find_all(
                        license="DMR1H6IXOPL1RVESWHBDZT1MHBZEBFXX|4QCPZJ2CMS75C99YB0LGQANO", remark="仗剑挂机助手",
                        rec_type="ch-3.0", box_type="rect", ratio=1.9, threshold=0.3, return_type='json', ocr_type=3,
                        run_mode='fast', capture=[x1, y1, x2, y2])
                else:
                    ocrRe = tomatoOcr.find_all(
                        license="DMR1H6IXOPL1RVESWHBDZT1MHBZEBFXX|4QCPZJ2CMS75C99YB0LGQANO", remark="仗剑挂机助手",
                        rec_type="ch-3.0", box_type="rect", ratio=1.9, threshold=0.3, return_type='json', ocr_type=3,
                        run_mode='fast', bitmap=bitmap)
            # print(ocrRe)
        except RuntimeError as e:
            print(f"TomatoOcrFindRange获取锁超时-{keyword}")
            return False, 0, 0
        center_x = 0
        center_y = 0
        ocrReJson = json.loads(ocrRe)
        for line in ocrReJson:
            lineWords = line.get('words', '')
            isFind = False
            if match_mode == 'fuzzy':
                if keyword in lineWords:
                    isFind = True
            elif match_mode == 'exact':
                if lineWords == keyword:
                    isFind = True
            else:
                raise ValueError(f"无效的匹配模式: {match_mode}")
            for key in keywords:
                if key['match_mode'] == 'fuzzy':
                    if key['keyword'] in lineWords:
                        print(f"TomatoOcrFindRange-fuzzy-别成功-{lineWords}")
                        isFind = True
                        break
                elif key['match_mode'] == 'exact':
                    if lineWords == key['keyword']:
                        print(f"TomatoOcrFindRange-exact-识别成功-{lineWords}")
                        isFind = True
                        break
                else:
                    raise ValueError(f"无效的匹配模式: {key['match_mode']}")
            if isFind:
                box = line.get('location')
                rx1, ry1 = box[0][0], box[0][1]
                rx2, ry2 = box[3][0], box[3][1]
                # 计算中心位置
                center_x = round((rx1 + rx2) / 2)
                center_y = round((ry1 + ry2) / 2)
        if center_x > 0 and center_y > 0:
            print(f"TomatoOcrFindRange识别成功-{keyword}-{keywords}|{center_x}|{center_y}")
            return True, center_x + x1, center_y + y1
        # print(f"TomatoOcrFindRange识别失败-{keyword}|{ocrRe}")
        print(f"TomatoOcrFindRange识别失败-{keyword}-{keywords}")
        return False, 0, 0
    except Exception as e:
        print(f"TomatoOcrFindRange发生异常: {e}")
        return False, 0, 0


def PaddleOcrFindRangeClick(keyword='T^&*', sleep1=0.9, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, whiteList='',
                            timeLock=5,
                            match_mode='exact', offsetX=0, offsetY=0, keywords=None):
    try:
        if whiteList == '':
            whiteList = keyword
        if keywords is None:
            keywords = []
        if match_mode == 'exact':
            ocrReJson = Ocr().paddleocr_v3(rect=[x1, y1, x2, y2], pattern=f'{keyword}')
        elif match_mode == 'fuzzy':
            ocrReJson = Ocr().paddleocr_v3(rect=[x1, y1, x2, y2], pattern=f'*{keyword}.*')
        else:
            raise ValueError(f"无效的匹配模式: {match_mode}")
        # print(ocrRe)
        if ocrReJson is not None:
            for line in ocrReJson:
                tapSleep(line.center_x + offsetX, line.center_y + offsetY, sleep1)
                print(f"PaddleOcrFindRangeClick识别成功-{keyword}-{keywords}|{line.center_x}|{line.center_y}")
                return True
        else:
            # print(f"PaddleOcrFindRangeClick识别失败-{keyword}|{ocrRe}")
            print(f"PaddleOcrFindRangeClick识别失败-{keyword}-{keywords}")
            return False
    except Exception as e:
        print(f"PaddleOcrFindRangeClick发生异常: {e}")
        return False


def TomatoOcrFindRangeClick(keyword='T^&*', sleep1=0.7, confidence1=0.9, x1=0, y1=0, x2=720, y2=1280, whiteList='',
                            timeLock=5,
                            match_mode='exact', offsetX=0, offsetY=0, bitmap='', keywords=None):
    try:
        if whiteList == '':
            whiteList = keyword
        if keywords is None:
            keywords = []
        try:
            with TimeoutLock(timeLock):
                if bitmap == '':
                    ocrRe = tomatoOcr.find_all(
                        license="DMR1H6IXOPL1RVESWHBDZT1MHBZEBFXX|4QCPZJ2CMS75C99YB0LGQANO", remark="仗剑挂机助手",
                        rec_type="ch-3.0", box_type="rect", ratio=1.9, threshold=0.3, return_type='json', ocr_type=3,
                        run_mode='fast', capture=[x1, y1, x2, y2])
                else:
                    ocrRe = tomatoOcr.find_all(
                        license="DMR1H6IXOPL1RVESWHBDZT1MHBZEBFXX|4QCPZJ2CMS75C99YB0LGQANO", remark="仗剑挂机助手",
                        rec_type="ch-3.0", box_type="rect", ratio=1.9, threshold=0.3, return_type='json', ocr_type=3,
                        run_mode='fast', bitmap=bitmap)
            # print(ocrRe)
        except RuntimeError as e:
            print(f"TomatoOcrFindRangeClick获取锁超时-{keyword}")
            return False
        center_x = 0
        center_y = 0
        if ocrRe == "":
            print(f"TomatoOcrFindRangeClick识别为空-{keyword}")
            return False
        try:
            ocrReJson = json.loads(ocrRe)
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e} - OCR Result: {ocrRe}")
            return False
        for line in ocrReJson:
            # print(line)
            lineWords = line.get('words', '')
            isFind = False
            if match_mode == 'fuzzy':
                if keyword in lineWords:
                    isFind = True
            elif match_mode == 'exact':
                if lineWords == keyword:
                    isFind = True
            else:
                raise ValueError(f"无效的匹配模式: {match_mode}")

            for key in keywords:
                if key['match_mode'] == 'fuzzy':
                    if key['keyword'] in lineWords:
                        isFind = True
                        break
                elif key['match_mode'] == 'exact':
                    if lineWords == key['keyword']:
                        isFind = True
                        break
                else:
                    raise ValueError(f"无效的匹配模式: {key['match_mode']}")

            if isFind:
                box = line.get('location')
                rx1, ry1 = box[0][0], box[0][1]
                rx2, ry2 = box[3][0], box[3][1]
                # 计算中心位置
                center_x = (rx1 + rx2) / 2
                center_y = (ry1 + ry2) / 2
                break
        if center_x > 0 or center_y > 0:
            tapSleep(center_x + x1 + offsetX, center_y + y1 + offsetY, sleep1)
            print(f"TomatoOcrFindRangeClick识别成功-{keyword}-{keywords}|{center_x}|{center_y}")
            return True
        # print(f"TomatoOcrFindRangeClick识别失败-{keyword}|{ocrRe}")
        print(f"TomatoOcrFindRangeClick识别失败-{keyword}-{keywords}")
        return False
    except Exception as e:
        print(f"TomatoOcrFindRangeClick发生异常: {e}")
        return False


# 速度慢、精度高、适合极小区域（单个字/数字）识别精准匹配
def TomatoOcrText(x1, y1, x2, y2, keyword,match_mode='exact'):
    try:
        # 传入图片路径或者Bitmap
        # res = ocr.ocrFile(R.img("logo.png"))
        try:
            with TimeoutLock():
                bitmap = screen.capture(x1, y1, x2, y2)
                tomatoOcr.setReturnType('json')
                ocrText = tomatoOcr.ocrBitmap(bitmap, 2)
            # print(ocrText)
        except RuntimeError as e:
            print(f"TomatoOcrText获取锁超时")
            return False, ''
        if ocrText != '' and ocrText is not None:
            ocrReJson = json.loads(ocrText)
            lineWords = ''
            lineWords = ocrReJson.get('words', '')
            if match_mode == 'fuzzy':
                if lineWords != "" and keyword in lineWords:
                    print(f"oText识别成功-{keyword}|{lineWords}")
                    return True, lineWords
            if match_mode == 'exact':
                if lineWords != "" and lineWords == keyword:
                    print(f"oText识别成功-{keyword}|{lineWords}")
                    return True, lineWords
            print(f"oText识别失败-不匹配-{keyword}|{lineWords}")
            return False, lineWords
        else:
            print(f"oText识别失败-不匹配-{keyword}|{ocrText}")
            return False, ocrText
    except Exception as e:
        print(f"toOcr发生异常: {e}")
        return False, ''


def TomatoOcrTap(x1, y1, x2, y2, keyword, offsetX=0, offsetY=0, sleep1=0.6,match_mode='exact'):
    try:
        try:
            with TimeoutLock():
                bitmap = screen.capture(x1, y1, x2, y2)
                tomatoOcr.setReturnType('json')
                ocrText = tomatoOcr.ocrBitmap(bitmap, 2)
            # print(ocrText)
        except RuntimeError as e:
            print(f"TomatoOcrTap获取锁超时")
            return False
        if ocrText != '' and ocrText is not None:
            ocrReJson = json.loads(ocrText)
            lineWords = ''
            lineWords = ocrReJson.get('words', '')
            if match_mode == 'fuzzy':
                if lineWords != "" and keyword in lineWords:
                    tapSleep(x1 + offsetX, y1 + offsetY, sleep1)
                    print(f"oTap识别成功-{keyword}|{lineWords}|{x1}|{y1}")
                    return True
            if match_mode == 'exact':
                if lineWords != "" and lineWords == keyword:
                    tapSleep(x1 + offsetX, y1 + offsetY, sleep1)
                    print(f"oTap识别成功-{keyword}|{lineWords}|{x1}|{y1}")
                    return True
            print(f"oTap识别失败-不匹配-{keyword}|{lineWords}")
            return False
        else:
            print(f"oTap识别失败-不匹配-{keyword}|{ocrText}")
            return False
    except Exception as e:
        print(f"toOcrTap发生异常: {e}")
        return False


lastToast = []
lastToastTime = 0


def generate_random_color():
    colors = ["#ffa400", "#ffa631", "#fa8c35", "#00bc12", "#0aa344", "#6b6882", "#ca6924", "#789262",
              "#758a99", "#177cb0", "#4b5cc4", "#8d4bbb", "#4c8dae", "#b0a4e3", "#cca4e3", "#c93756",
              "#f05654", "#7b68ee"]
    return random.choice(colors)


def Toast(content, tim=1000):
    if 任务记录['提示-并发锁'] == 1:
        return
    global lastToast
    global lastToastTime
    nowTime = time.time()
    # 重复提示，2s 1次
    if content in lastToast and nowTime - lastToastTime < 5:
        return
    if nowTime - lastToastTime > 5:
        lastToast = []
    lastToast.append(content)
    lastToastTime = nowTime
    print(f"提示-{content}")
    Dialog.toast(content, tim, 3 | 48, 200, 0)


def tapSleep(x, y, s=0.8, dur=200):
    click(x, y, dur)
    sleep(s)


def tapSleepV2(x, y, s=0.8, dur=200):
    clickV2(x, y, dur)
    sleep(s)


def safe_int(value):
    """
    尝试将给定的值转换为整数，如果失败则返回默认值 0。
    """
    try:
        # 兜底子母o
        if value == "。" or value == "o" or value == "O" or value == "c" or value == "C":
            return 0
        return int(value)
    except (TypeError, ValueError):
        return ""


def safe_int_v2(value):
    """
    尝试将给定的值转换为整数，如果失败则返回默认值 0。
    """
    try:
        # 兜底子母o
        if value == "o" or value == "O":
            return 0
        return int(value)
    except (TypeError, ValueError):
        return 0


def safe_float_v2(value):
    """
    尝试将给定的值转换为小数，如果失败则返回默认值 0。
    """
    try:
        # 兜底子母o
        if value == "o" or value == "O":
            return 0
        return float(value)
    except (TypeError, ValueError):
        return 0
