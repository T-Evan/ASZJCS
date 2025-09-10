# 导包
from ascript.android import system
from six import print_
from ascript.android.system import ShellListener

from .特征库 import *
from ascript.android.ui import Dialog
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .res.ui.ui import switch_lock
from .baseUtils import *
import shutil
import os
import sys
from ascript.android import system
from ascript.android.screen import FindColors
import sys
import traceback
from ascript.android.system import Device


class StartUp:
    # 构造器
    def __init__(self, app_name):
        self.app_name = app_name

    # 实例方法
    def start_app(self):
        global 功能开关
        # r = system.shell(f"start -n com.xd.cfbmf")
        tryTimes = 0

        max_attempt = 45

        display = Device.display()
        # 屏幕宽度
        if display.widthPixels != 720 or display.heightPixels != 1280:
            Toast(f'分辨率为 {display.widthPixels} * {display.heightPixels}，请检查分辨率是否正确')
            Dialog.confirm("屏幕分辨率不为 720 * 1280，请重新设置", "分辨率错误")
            r = system.shell(f"wm size 720x1280", L())
            r = system.shell(f"wm density 320", L())
            display = Device.display()
            if display.widthPixels != 720 or display.heightPixels != 1280:
                Dialog.confirm("屏幕分辨率已设置为 720 * 1280", "分辨率已调整")

        for attempt in range(max_attempt):
            tryTimes = tryTimes + 1

            system.open(self.app_name)

            # 判断是否已在首页
            shou_ye1 = self.返回首页()
            if shou_ye1:
                return True

            res1, _ = TomatoOcrText(231, 562, 485, 609, "登录", match_mode='fuzzy')
            if res1:
                return True

            # 识别是否进入登录页
            login1, _ = TomatoOcrText(618, 77, 693, 108, "服务器")  # 首页服务器选择
            if login1:
                Toast('准备进入游戏')
                self.login()
            else:
                re, _ = TomatoOcrText(317, 72, 401, 118, '公告')
                if re:
                    Toast('关闭公告页')
                    tapSleep(334, 1237)  # 点击空白处，关闭登录页公告
                    res1, _ = TomatoOcrText(231, 562, 485, 609, "登录", match_mode='fuzzy')
                    if res1:
                        return True
                    tapSleep(334, 1237)  # 点击空白处

            # 识别是否在更新中
            re, _, _ = TomatoOcrFindRange("正在", match_mode='fuzzy', x1=180, y1=976, x2=311, y2=1008)
            if re:
                Toast(f'启动游戏，等待更新中')
                sleep(15)

            if tryTimes > 2:
                self.世界聊天检查()

            # 判断是否已在首页
            shou_ye1 = self.返回首页()
            if not shou_ye1:
                # 不在首页，尝试开始返回首页
                # 开始异步处理返回首页
                功能开关["needHome"] = 1
                功能开关["fighting"] = 0
                Toast('正在返回首页')
                tapSleep(52, 1229)
                TomatoOcrTap(457, 721, 525, 754, '确定', sleep1=1.5)
                # tapSleepV2(52, 1229)
            Toast(f'启动游戏，等待加载中，{attempt}/{max_attempt}')

            sleep(1)  # 等待游戏启动

        print('启动游戏失败，尝试重启游戏')
        # 结束应用
        r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
        # 重启游戏
        return self.start_app()

    def 世界聊天检查(self):
        for k in range(2):
            re = FindColors.find(
                "34,1224,#020202|42,1233,#020202|51,1224,#020202|31,1235,#E2E2E2|51,1234,#E2E2E2",
                rect=[14, 735, 82, 1264], diff=0.95)
            if re:
                Toast('世界聊天关闭1')
                tapSleep(re.x, re.y)
            re = FindColors.find("33,828,#000000|43,839,#070707|51,834,#0A0A0A|30,841,#E1E1E1|51,841,#E2E2E2",
                                 rect=[4, 616, 98, 1208], diff=0.95)
            if re:
                Toast('世界聊天关闭2')
                tapSleep(re.x, re.y)

    def 返回首页(self):
        if 功能开关["fighting"] == 1:
            sleep(2)
            return True

        # 判断是否已在首页
        shou_ye1 = CompareColors.compare(
            "320,1221,#DADE71|369,1218,#746661|356,1169,#FEDCE3|403,1223,#CDD068")  # 判断底部家园图标（已点亮）
        if not shou_ye1:
            re1 = CompareColors.compare("353,1186,#FFD1DA|361,1204,#AC8B7B|358,1251,#756361")  # 匹配底部家园图标(未点亮)
            re2 = CompareColors.compare("395,1175,#D44444|400,1173,#FAF3F3|403,1173,#DF5050")  # 匹配底部家园图标(未点亮-红点)
            if re1 or re2:
                Toast('返回首页')
                tapSleep(358, 1223, 1)
                shou_ye1 = CompareColors.compare(
                    "320,1221,#DADE71|369,1218,#746661|356,1169,#FEDCE3|403,1223,#CDD068")  # 判断底部家园图标（已点亮）
                if not shou_ye1:
                    shou_ye1, _ = TomatoOcrText(329, 1248, 390, 1278, '家园')  # 判断底部家园图标（已点亮）
        if shou_ye1:
            if 任务记录['玩家名称'] == '' or 任务记录['玩家名称'] == 0:
                _, 任务记录['玩家名称'] = TomatoOcrText(105, 17, 268, 48, '登录玩家名称')
            Toast('已进入游戏')
            功能开关["needHome"] = 0
            return True
        return False

    def login(self):
        sleep(0.5)
        login1 = False
        login1, _ = TomatoOcrText(618, 77, 693, 108, "服务器")  # 首页服务器选择

        if not login1:
            return self.start_app()

        for i in range(2):
            login1, _ = TomatoOcrText(618, 77, 693, 108, "服务器")  # 首页服务器选择
            if login1:
                Toast(f'等待进入游戏')
                tapSleep(345, 1052, 2)

        shou_ye = False
        for loopCount in range(4):
            shou_ye1, _ = TomatoOcrText(333, 1249, 386, 1276, '家园')
            if shou_ye1:
                Toast('已进入游戏')
                shou_ye = True
                sleep(0.5)  # 等待 3 秒
            tapSleep(682, 17)  # 点击空白处

        # if not shou_ye:
        #     return self.start_app()

        return shou_ye

    def switchAccount(self):
        功能开关["fighting"] = 0
        功能开关["needHome"] = 0
        if 任务记录['当前任务账号'] != "":
            tmpAccount = safe_int(任务记录['当前任务账号'])
            tmpAccount = tmpAccount + 1  # 切换下一账号
            for i in range(tmpAccount, 6):
                if 功能开关['账号' + str(i) + '开关'] == 1 or 功能开关['账号' + str(i) + '开关'] == "true":
                    任务记录['当前任务账号'] = i
                    return self.loadAccount(i)

            # 循环一遍后，重新执行
            for i in range(1, 6):
                if 功能开关['账号' + str(i) + '开关'] == 1 or 功能开关['账号' + str(i) + '开关'] == "true":
                    任务记录['当前任务账号'] = i
                    return self.loadAccount(i)
                return None
            return None
        return None

    def multiAccount(self):
        for k in range(25):
            try:
                system.open(self.app_name)
            except Exception as e:
                # 处理异常
                # 获取异常信息
                exc_type, exc_value, exc_traceback = sys.exc_info()
                # 输出异常信息和行号
                file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
                error_message = f"发生错误1: {e} 在文件 {file_name} 第 {line_number} 行"
                # 显示对话框
                print(error_message)
                if '没有找到' in error_message:
                    print('尝试切换游戏版本')
                    功能开关['游戏包名'] = random.choice(
                        ["com.leiting.zjcs", "com.leiting.zjcs.bilibili", "com.m88.zjcs.j", "com.m88.zjcs.h",
                         "com.zjcs.android.jp",
                         "com.m88.zjcs.n",
                         "com.m88.zjcs.g", "com.m88.idleXX", "com.leiting.zjcs.b", "com.m88.zjcs.b", "com.m88.zjcs.f"])
                    self.app_name = f'{功能开关["游戏包名"]}'

        if 功能开关['账号1保存']:
            self.saveAccount(1)

        if 功能开关['账号2保存']:
            self.saveAccount(2)

        if 功能开关['账号3保存']:
            self.saveAccount(3)

        if 功能开关['账号4保存']:
            self.saveAccount(4)

        if 功能开关['账号5保存']:
            self.saveAccount(5)

        # 指定账号启动
        if 功能开关['选择启动账号'] != "" and 功能开关['选择启动账号'] != 0 and 功能开关['选择启动账号'] != "0":
            self.loadAccount(功能开关['选择启动账号'])

    def saveAccount(self, account_name):
        account_name = str(account_name)
        old_path1 = f"/data/data/{功能开关['游戏包名']}/shared_prefs"
        new_path1 = f"/data/data/{功能开关['游戏包名']}/accountConfig" + account_name + "_shared_prefs"

        # 删除文件夹
        r = system.shell(f"rm -rf {new_path1} 2>/dev/null")
        # shutil.rmtree(new_path1, ignore_errors=True)
        # 新建文件夹
        # r = system.shell(f"mkdir -p {new_path1}")
        # os.makedirs(new_path1, exist_ok=True)
        # 复制文件夹
        flag1 = system.shell(f"cp -r -a {old_path1} {new_path1}")
        # flag1 = shutil.copytree(old_path1, new_path1, dirs_exist_ok=True)

        old_path2 = f"/data/data/{功能开关['游戏包名']}/app_webview"
        new_path2 = f"/data/data/{功能开关['游戏包名']}/accountConfig" + account_name + "_app_webview"

        # 删除文件夹
        r = system.shell(f"rm -rf {new_path2} 2>/dev/null")
        # shutil.rmtree(new_path2, ignore_errors=True)
        # 新建文件夹
        # r = system.shell(f"mkdir -p {new_path2}")
        # os.makedirs(new_path2, exist_ok=True)
        # 复制文件夹
        flag2 = system.shell(f"cp -r -a {old_path2} {new_path2}")
        # flag2 = shutil.copytree(old_path2, new_path2, dirs_exist_ok=True)

        # 复制文件夹及里面所有文件
        if flag1 is None and flag2 is None:
            Dialog.confirm(f"已保存账号 {account_name} 登录信息！请重新启动后继续配置")
        else:
            Dialog.confirm("保存失败！请检查是否授予root权限")
        system.exit()
        return True

    def loadAccount(self, account_name):
        global 功能开关
        for k in range(25):
            try:
                system.open(self.app_name)
            except Exception as e:
                # 处理异常
                # 获取异常信息
                exc_type, exc_value, exc_traceback = sys.exc_info()
                # 输出异常信息和行号
                file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
                error_message = f"发生错误1: {e} 在文件 {file_name} 第 {line_number} 行"
                # 显示对话框
                print(error_message)
                if '没有找到' in error_message:
                    print('尝试切换游戏版本')
                    功能开关['游戏包名'] = random.choice(
                        ["com.leiting.zjcs", "com.leiting.zjcs.bilibili", "com.m88.zjcs.j", "com.m88.zjcs.h",
                         "com.zjcs.android.jp",
                         "com.m88.zjcs.n",
                         "com.m88.zjcs.g", "com.m88.idleXX", "com.leiting.zjcs.b", "com.m88.zjcs.b", "com.m88.zjcs.f"])
                    self.app_name = f'{功能开关["游戏包名"]}'

        try:
            account_name = str(account_name)
            Toast('加载账号' + account_name)
            # 结束应用
            # r = system.shell("am kill com.xd.cfbmf", L())
            r = system.shell(f"am force-stop {功能开关['游戏包名']}", L())
            print(r)
            oldPath1 = f"/data/data/{功能开关['游戏包名']}/shared_prefs/"
            # 删除文件夹
            r = system.shell(f"rm -rf {oldPath1} 2>/dev/null", L())
            new_path1 = f"/data/data/{功能开关['游戏包名']}/accountConfig" + account_name + "_shared_prefs/"
            flag1 = system.shell(f"cp -r -a {new_path1} {oldPath1}", L())
            # configNum = 功能开关['账号' + str(account_name) + '配置']
            # if configNum != 0 and configNum != '' and configNum != '0':
            #     Toast(f'加载账号{account_name} + 加载配置{configNum}')
            #     功能开关 = loadConfig(configNum, account_name)

            system.open(f"{功能开关['游戏包名']}")
        except Exception as e:
            # 处理异常
            # 获取异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            # 输出异常信息和行号
            file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
            error_message = f"发生错误: {e} 在文件 {file_name} 第 {line_number} 行"
            # 显示对话框
            print(error_message)


class L(ShellListener):
    def commandOutput(self, i: int, s: str):
        print('?', s)

    def commandTerminated(self, i: int, s: str):
        pass

    def commandCompleted(self, i: int, i1: int):
        pass
