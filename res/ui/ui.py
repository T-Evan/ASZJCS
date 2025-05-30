# __init__.py 为初始化加载文件
# 导入-节点检索库
import json
import time
import pymysql

from ascript.android.system import R
# 导入-屏幕检索库
from ascript.android.ui import WebWindow
from ascript.android.ui import Dialog
import threading
import sys
from ascript.android import system
# 向悬浮菜单中新增按钮
from ascript.android.ui import FloatWindow
from ascript.android.system import R
# 导入-屏幕检索库
from ascript.android.ui import WebWindow
# from ascript.android.ui import Loger
from datetime import datetime, timedelta
from time import sleep

config = None


def tunner(k, v):
    global config
    # print(k, v)
    # print(k)
    # print(v)

    if k == "guan" and v == "关闭":
        config = "exit"
    if k == "submit":
        res = json.loads(v)
        config = res
        # print(type(config))
    if k == "加载" and v == "成功":
        print('加载成功')


formW = WebWindow(R.ui("ui.html"))
formW.size('100vw', '100vh')
formW.tunner(tunner)  # 在这里设置消息通道
formW.background("#FFFFFF")
formW.show()
from threading import Lock

while True:
    # print("循环等待中")
    time.sleep(1)
    if config == "exit":
        Dialog.toast('取消执行', 5, 3 | 48, 200, 0)
        system.exit()
    if config:
        Dialog.toast('资源加载中 - 请等待30s', 5, 3 | 48, 200, 0)
        # time.sleep(2)
        break

import time


class TimeoutLock:
    def __init__(self, timeLock=10, lock=''):
        self.lock = lock
        if lock == '':
            self.lock = switch_lock
        self.timeout = timeLock

    def acquire_lock(self):
        start_time = time.time()
        while (time.time() - start_time) < self.timeout:
            if self.lock.acquire(False):
                return True
            time.sleep(0.2)
        print(f"尝试获取锁超时，耗时: {time.time() - start_time} 秒")
        return False

    def release_lock(self):
        if self.lock.locked():
            self.lock.release()

    def __enter__(self):
        acquired = self.acquire_lock()
        if not acquired:
            raise RuntimeError("无法在指定时间内获取锁")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release_lock()
        # print("锁已成功释放")


# 初始化锁
global switch_lock
switch_lock = threading.Lock()
# global switch_ocr_apk_lock  # apk ocr 识别锁
# switch_ocr_apk_lock = Lock()
功能开关 = {}
功能开关 = config
if 功能开关['选择游戏版本'] == "公测服":
    功能开关['游戏包名'] = "com.leiting.zjcs"
elif 功能开关['选择游戏版本'] == "内测服":
    功能开关['游戏包名'] = "com.leiting.zjcs.b"

# thread_main_paused = False
# thread_main_cond = threading.Condition()

任务记录 = {
    "提示-并发锁": 0,
    "喊话-并发锁": 0,
    "启动时间": time.time(),
}


def 初始化任务记录(initAll=True):
    # 日常
    任务记录.update({
        "首页卡死检测-倒计时": 0,
        "强化装备-倒计时": 0,
        "小推车-倒计时": 0,
        "小木床-倒计时": 0,
        "探索生命补充-倒计时": 0,

        "邮件领取": 0,
        "每日签到": 0,
        "成长试炼": 0,
        "启程签到": 0,
        "菜就多躺": 0,
        "每日商店": 0,

        "巡礼之证": 0,
        "月卡领取": 0,
        "启程好礼": 0,
        "幻想学院": 0,
        "魔法文具": 0,

        "公会挂机奖励": 0,
        "公会捐赠": 0,
    })


def tunner(k, v):
    print(k, v)
