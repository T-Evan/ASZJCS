# 导包
from ascript.android import plug
from ascript.android.ui import Dialog
from ascript.android import system

plug.load("TomatoOcr:1.1.1")
try:
    from TomatoOcr import TomatoOcr
except Exception as e:
    Dialog.confirm("初始化完成，请重新启动脚本", "初始化完成")
    system.exit()

global tomatoOcr
# global tomatoOcrJson
def init_tomatoOcr():
    ocr = TomatoOcr()
    ocr.setContext(rec_type="ch-3.0")

    ocr.setLicense("","仗剑挂机助手")

    ocr.setRecType("ch-3.0")
    ocr.setDetBoxType("rect")
    ocr.setDetUnclipRatio(1.9)
    ocr.setRecScoreThreshold(0.3)
    ocr.setReturnType("text")
    ocr.setRunMode("fast")
    # ocr.setBinaryThresh("0")
    global tomatoOcr
    tomatoOcr = ocr

def init_tomatoOcrJson():
    ocr = TomatoOcr()
    ocr.setContext(rec_type="ch-3.0")

    ocr.setLicense("","仗剑挂机助手")

    ocr.setRecType("ch-3.0")
    ocr.setDetBoxType("rect")
    ocr.setDetUnclipRatio(1.9)
    ocr.setRecScoreThreshold(0.3)
    ocr.setReturnType("json")
    # ocr.setBinaryThresh("0")
    global tomatoOcrJson
    tomatoOcrJson = ocr

init_tomatoOcr()  # 初始化
# init_tomatoOcrJson()  # 初始化