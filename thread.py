import threading
from .child_notice import main as notice_main
from .child_mijing_team import main as mijing_team
from .res.ui.ui import 功能开关
import multiprocessing
from java.lang import Runnable, Thread
from java import dynamic_proxy

class RunThreadMijingTeam(dynamic_proxy(Runnable)):
    def __init__(self):
        super().__init__()

    def run(self):
        print("启动自动入队处理线程")
        mijing_team()

def runThreadMijingTeam():
    try:
        r = RunThreadMijingTeam()
        t = Thread(r)
        t.start()
    except RuntimeError as e:
        print(f"自动入队处理线程 Error: {e}")

class RunThreadNotice(dynamic_proxy(Runnable)):
    def __init__(self):
        super().__init__()

    def run(self):
        print("启动空白弹窗处理线程")
        notice_main()


def runThreadNotice():
    try:
        r = RunThreadNotice()
        t = Thread(r)
        t.start()
    except RuntimeError as e:
        print(f"空白弹窗处理线程 Error: {e}")
