# ui.py 为初始化加载文件
import sys
import traceback
import json
import gc

# 导入动作模块
from .res.ui.ui import 功能开关
from .res.ui.ui import 任务记录
from .startUp import StartUp
from .daily import DailyTask
from .fuBen import FuBenTask
from .jueSe import JueSeTask
from .gongHui import GongHuiTask
from .res.ui.ui import 初始化任务记录
from .baseUtils import *
import time
from ascript.android.ui import Dialog
import pymysql
from datetime import datetime
from ascript.android.system import Device
from ascript.android.ui import Loger
from ascript.android import system
from ascript.android.action import Path
from .thread import *
from ascript.android.system import ShellListener

# ldE.set_log_level(10)  # Debug
# ldE.set_log_level(20)  # Info
# ldE.set_log_level(30)  # Warn
# ldE.set_log_level(40)  # ERROR

初始化任务记录()


def kamiActive():
    db = pymysql.connect(
        host="8.140.162.237",  # 开发者后台,创建的数据库 “主机地址”
        port=3307,  # 开发者后台,创建的数据库 “端口”
        user='yiwan233',  # 开发者后台,创建的数据库 “用户名”
        password='233233',  # 开发者后台,创建的数据库 “初始密码”
        database='db_dev_12886',  # 开发者后台 ,创建的 "数据库"
        charset='utf8mb4'  ""
    )  # 连接数据库
    cursor = db.cursor()
    sql = "SELECT * FROM kami WHERE kami != '' and kami LIKE %s"
    # 使用参数化查询
    功能开关['激活码'] = 功能开关['激活码'].strip()
    cursor.execute(sql, (功能开关['激活码'],))
    results = cursor.fetchall()

    # 循环遍历所有数据
    kami = ''
    device_id = ''
    expire_time = 0
    device_available_num = ''
    for row in results:
        # 我们的表数据,总共4列,因此逐个获取每列数据
        kami = row[0]
        device_id = row[1]
        expire_time = row[3]
        device_available_num = row[5]

    if kami == '':
        now_device_id = '"' + Device.id() + '"'
        # 判断设备是否激活过试用
        sql = "SELECT * FROM kami WHERE device_id LIKE %s and kami = ''"
        # 使用参数化查询
        cursor.execute(sql, now_device_id)
        results = cursor.fetchall()
        for row in results:
            device_id = row[1]
            expire_time = row[3]
        if device_id == '':
            expire_time = int(time.time()) + 86400 * 0.5  # 日卡
            dt_object = datetime.fromtimestamp(expire_time)
            formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            now_device_id = Device.id()
            device_ids = json.dumps(now_device_id)
            # 构造 SQL 语句
            sql = "Insert into kami (device_id,expire_time,kami) Values (%s,%s,'')"
            # 使用参数化查询
            cursor.execute(sql, (device_ids, expire_time))
            db.commit()  # 不要忘了提交,不然数据上不去哦
            activeInfo = '试用卡密激活成功，过期时间：' + formatted_date
            Toast(activeInfo, 3000)
        if device_id != '':
            # 判断首次激活
            if expire_time == 0:
                expire_time = int(time.time()) + 86400 * 0.5  # 日卡
                dt_object = datetime.fromtimestamp(expire_time)
                formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                now_device_id = Device.id()
                device_ids = json.dumps(now_device_id)
                # 构造 SQL 语句
                sql = "UPDATE kami SET device_id = %s, expire_time = %s WHERE device_id LIKE %s and kami == ''"
                # 使用参数化查询
                cursor.execute(sql, (device_ids, expire_time, kami))
                db.commit()  # 不要忘了提交,不然数据上不去哦
                activeInfo = '试用卡密激活成功，过期时间：' + formatted_date
                Toast(activeInfo, 3000)
            if expire_time != 0:
                dt_object = datetime.fromtimestamp(expire_time)
                formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                # 判断卡密是否过期
                if int(time.time()) > expire_time:
                    activeInfo = '卡密已过期，过期时间：' + formatted_date
                    Dialog.confirm(activeInfo, "激活码失效")
                    Toast(activeInfo, 3000)
                    sleep(2)
                    system.exit()
                else:
                    activeInfo = '试用已激活，' + '过期时间：' + formatted_date
                    Toast(activeInfo, 3000)
                    sleep(2)

    # activeInfo = '卡密不存在，请重新输入'
    # Dialog.confirm(activeInfo, "激活码失效")
    # Toast(activeInfo, 3000)
    # system.exit()
    if kami != '':
        # 判断首次激活
        if expire_time == 0:
            if 'test' in kami:
                expire_time = int(time.time()) + 86400 * 1  # 日卡
            else:
                expire_time = int(time.time()) + 86400 * 30  # 月卡
            dt_object = datetime.fromtimestamp(expire_time)
            formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            now_device_id = Device.id()
            device_ids = json.dumps(now_device_id)
            # 构造 SQL 语句
            sql = "UPDATE kami SET device_id = %s, expire_time = %s WHERE kami = %s"
            # 使用参数化查询
            cursor.execute(sql, (device_ids, expire_time, kami))
            db.commit()  # 不要忘了提交,不然数据上不去哦
            activeInfo = '卡密激活成功，过期时间：' + formatted_date
            Toast(activeInfo, 3000)
        if expire_time != 0:
            dt_object = datetime.fromtimestamp(expire_time)
            formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            # 判断卡密是否过期
            if int(time.time()) > expire_time:
                activeInfo = '卡密已过期，过期时间：' + formatted_date
                Dialog.confirm(activeInfo, "激活码失效")
                Toast(activeInfo, 3000)
                sleep(2)
                system.exit()
            # 判断登录设备数
            now_device_id = Device.id()
            device_ids = json.loads(device_id)
            if now_device_id in device_id:
                activeInfo = '已激活，' + '过期时间：' + formatted_date
                Toast(activeInfo, 3000)
                sleep(2)
            else:
                # 判断已激活设备数
                if len(device_ids) >= device_available_num:
                    activeInfo = '已超过可激活设备数量'
                    Dialog.confirm(activeInfo, "激活码失效")
                    Toast(activeInfo, 3000)
                    sleep(2)
                    system.exit()
                else:
                    # 激活当前设备
                    device_ids.append(now_device_id)
                    set_device_ids = json.dumps(device_ids)
                    # 构造 SQL 语句
                    sql = "UPDATE kami SET device_id = %s WHERE kami = %s"
                    # 使用参数化查询
                    cursor.execute(sql, (set_device_ids, kami))
                    db.commit()  # 不要忘了提交,不然数据上不去哦
                    activeInfo = '激活新设备成功，' + '过期时间：' + formatted_date
                    Toast(activeInfo, 3000)
                    sleep(2)

    # 执行完之后要记得关闭游标和数据库连接
    cursor.close()
    # 执行完毕后记得关闭db,不然会并发连接失败哦
    db.close()


print('卡密联网激活开始')
kamiActive()
print('卡密联网激活完成')


# debug
# action.Touch.down(127,1000, 1500)  # 长按
# action.Touch.up(127,1000, 1500)
# from ascript.android.screen import FindColors
# system.exit()


def main():
    try:
        start_up = StartUp(f'{功能开关["游戏包名"]}')
        dailyTask = DailyTask()
        fuBenTask = FuBenTask()
        jueSeTask = JueSeTask()
        gongHuiTask = GongHuiTask()

        runThreadNotice()
        runThreadMijingTeam()

        # 处理休息时间
        need_run_minute = safe_int(功能开关.get("定时运行", 0))  # 分钟
        if need_run_minute == '':
            need_run_minute = 0
        need_wait_minute = safe_int(功能开关.get("定时休息", 0))  # 分钟
        if need_wait_minute == '':
            need_wait_minute = 0
        need_switch_account_minute = safe_int(功能开关.get("定时切账号", 0))  # 分钟
        if need_switch_account_minute == '':
            need_switch_account_minute = 0
        total_wait = need_run_minute * 60
        total_switch_account_minute = need_switch_account_minute * 60
        任务记录["定时休息-倒计时"] = time.time()
        任务记录["任务重置-倒计时"] = time.time()
        任务记录["切换账号-倒计时"] = time.time()

        # dailyTask.主线探索()
        # system.exit()

        start_up.multiAccount()
        while True:
            try:
                # 启动app
                start_up.start_app()
                if 功能开关["日常总开关"] == 0 and 功能开关["副本总开关"] == 0 and 功能开关["公会总开关"] == 0:
                    Toast('未开启总开关，请检查功能配置')
                    sleep(3)

                # 日常（优先领取）
                dailyTask.dailyTask()

                # 副本
                fuBenTask.fuBenTask()

                # 角色
                jueSeTask.jueSeTask()

                # 公会
                gongHuiTask.gongHuiTask()

                # 日常（最后领取）
                dailyTask.dailyTaskEnd()

                # 定时休息
                current_time = int(time.time())

                # 获取当前设备运行的APP信息
                gc.collect()

                # 将时间戳转换为 datetime 对象
                # 判断执行时间超过4小时（重置每日任务）
                if current_time - 任务记录["任务重置-倒计时"] > 60 * 60 * 2:
                    Toast(f"执行时间超过2小时，重置每日任务")
                    sleep(1.5)
                    初始化任务记录(False)
                    任务记录["任务重置-倒计时"] = int(time.time())

                if total_wait != 0 and current_time - 任务记录["定时休息-倒计时"] >= total_wait:
                    Toast(f"休息 {need_wait_minute} 分钟")
                    sleep(1.5)
                    功能开关["fighting"] = 0
                    功能开关["needHome"] = 0
                    action.Key.home()
                    初始化任务记录(False)
                    sleep(need_wait_minute * 60)
                    任务记录["定时休息-倒计时"] = int(time.time())

                # 定时切账号
                current_time = int(time.time())
                if total_switch_account_minute != 0:
                    if current_time - 任务记录["切换账号-倒计时"] >= total_switch_account_minute:
                        Toast(f"运行 {need_switch_account_minute} 分钟，准备切换账号")
                        sleep(1.5)
                        初始化任务记录(False)
                        start_up.switchAccount()
                        print(功能开关)
                        任务记录["切换账号-倒计时"] = int(time.time())
                    else:
                        tmpMinute = round((current_time - 任务记录["切换账号-倒计时"]) / 60, 2)
                        tmpDiffMinute = round(
                            need_switch_account_minute - ((current_time - 任务记录["切换账号-倒计时"]) / 60), 2)
                        Toast(f"运行 {tmpMinute} 分钟，{tmpDiffMinute} 分后切换账号")
                        sleep(1.5)

                sleep(0.5)
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
                        ["com.leiting.zjcs", "com.leiting.zjcs.bilibili", "com.m88.zjcs.j", "com.m88.zjcs.h","com.m88.zjcs.g","com.m88.idleXX","com.leiting.zjcs.b","com.m88.zjcs.b"])
                    start_up = StartUp(f'{功能开关["游戏包名"]}')

    except Exception as e:
        # 处理异常
        # 获取异常信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # 输出异常信息和行号
        file_name, line_number, _, _ = traceback.extract_tb(exc_traceback)[-1]
        error_message = f"发生错误2: {e} 在文件 {file_name} 第 {line_number} 行"
        # 显示对话框
        print(error_message)
        if error_message != '':
            Dialog.confirm(error_message)
        else:
            Toast('检测到执行出现异常，请联系群主反馈')
    sys.exit()


main()
