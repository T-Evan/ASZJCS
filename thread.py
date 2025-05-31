import threading
from .child_notice import main as notice_main
from .res.ui.ui import 功能开关
import multiprocessing
from java.lang import Runnable, Thread
from java import dynamic_proxy


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
