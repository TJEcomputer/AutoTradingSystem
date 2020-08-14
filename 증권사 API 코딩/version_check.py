import os
import time
import psutil  # 실행중인 프로세스 및 시스템 활용 라이브러리
from pywinauto import application
import subprocess


def check_version():
    app = application.Application()
    app.start("C:/KiwoomFlash3/Bin/NKMiniStarter.exe")
    print(app)
    title = ""
    dlg = app.window(title_re=title)


    #
    # cert_ctrl = dlg.Edit1
    # cert_ctrl.set_focus()
    # cert_ctrl.type_keys('dhdhfh')
    # print(cert_ctrl)
    # cert_ctrl = dlg.Edit2
    # cert_ctrl.set_focus()
    # cert_ctrl.type_keys('vldpfh12')
    #
    # cert_ctrl = dlg.Edit3
    # cert_ctrl.set_focus()
    # cert_ctrl.type_keys('vldpfh157!')
    #
    # btn_ctrl = dlg.Button0
    # btn_ctrl.click()
    #
    # time.sleep(30)
    # status = subprocess.call("taskkill /im nkmini.exe")
    # print(status)
    # time.sleep(5)
    #
    # status = subprocess.call("taskkill /im nkmini.exe")
    # print(status)



if __name__ == "__main__":
    check_version()
