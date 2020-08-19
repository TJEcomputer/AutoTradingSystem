import time

import pywinauto
from connect.VersionUpdate import Win32Function_st
from connect.VersionUpdate.log_record import log_recorder
class update_start:

    def __init__(self):
        pass

    def KOAStart(self):
        logger = log_recorder.recorder_time("checkerKOAStart")
        logger.info('KOAStiudio Start')
        time.sleep(1)
        self.app = pywinauto.application.Application()
        self.app.start("C:/Users/TJ/Desktop/python/KOAStudioSA/KOAStudioSA.exe")
        ko_title = Win32Function_st.check_window('KOA StudioSA ver 2.20', 10)
        if ko_title != 0:
            time.sleep(3)
            logger.info("파일(F) -> Open API 실행")
            self.app.KOAStudioSA.send_keystrokes("%{F}")
            time.sleep(1)
            self.app.KOAStudioSA.send_keystrokes("{ENTER}")

        else:
            logger.info("KOAStudio is not started")

    def api_login(self,callback=None):
        logger = log_recorder.recorder_time("api_login")
        api_title = Win32Function_st.check_window('Open API Login', 15)
        if api_title != 0:
            time.sleep(2)
            logger.info(" input password")
            Win32Function_st.input_string('Open API Login',1001,"vldpfh12")
            time.sleep(2)
            logger.info(" click Login Button")
            Win32Function_st.click_item('Open API Login',1)
            time.sleep(1)
            logger.info("login 실행")
            if callback is not None and str(type(callback)) == "<class 'function'>":
                logger.info("start " + callback)
                time.sleep(1)
                callback()

        else:
            logger.info("API is not started")

    def version_checker(self,count = 15):
        logger = log_recorder.recorder_time("version_checker")
        i = 0
        time.sleep(15)
        a = True


        logger.info(" version checking....")

        logger.info(" version checking start")
        while i < count:
            api_hwnd = Win32Function_st.check_window('Open API Login')
            if api_hwnd != 0:
                title_list = ["opstarter", "opversionup", "Open API"]
                for title in title_list:
                    time.sleep(1)
                    title_hwnd = Win32Function_st.check_window(title)
                    logger.info(title +" is checking ... ")
                    if title_hwnd != 0:
                        logger.info(title + " find...")
                        if title == "opstarter":
                            ko_title = Win32Function_st.check_window('KOA StudioSA ver 2.20', 10)
                            if ko_title != 0:
                                self.app.KOAStudioSA.send_keystrokes("%{F4}")
                            time.sleep(2)
                            Win32Function_st.click_item(title,2)
                            time.sleep(10)
                        elif title == "opversionup":
                            Win32Function_st.click_item(title, 2)
                        elif title == "Open API":
                            Win32Function_st.click_item(title, 2)

                    else:
                        logger.info(title + " is not existed")
            else:
                logger.info("API is not found")
                title = "업그레이드 확인"
                title_hwnd = Win32Function_st.check_window(title)
                logger.info(title + " is checking ... ")
                if title_hwnd != 0:
                    logger.info(title + " find...")
                    Win32Function_st.click_item(title, 1)
                    i = i + 1
                else:
                    logger.info(title + " is not found")
                    a = False
                    break
                    return a
        return a


def checker_rr():

    logger = log_recorder.recorder_time("main")
    update = update_start()
    update.KOAStart()
    update.api_login()
    i = 0
    while i < 10:
        t = update.version_checker(10)
        if t ==False:
            logger.info("end")
            break
    ko_title = Win32Function_st.check_window('KOA StudioSA ver 2.20', 10)
    if ko_title != 0:
        Win32Function_st.close_win('KOA StudioSA ver 2.20')
        logger.info("Version Update 완료")
    else:
        logger.info("Version Update 완료")


