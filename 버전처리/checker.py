import time

import pywinauto
import Win32Function

class update_start:

    def __init__(self):
        pass

    def KOAStart(self):
        print("KOAStiudio Start")
        time.sleep(1)
        self.app = pywinauto.application.Application()
        self.app.start("C:/Users/CC/Desktop/KOAStudioSA/KOAStudioSA.exe")
        ko_title = Win32Function.check_window('KOA StudioSA ver 2.20', 10)
        if ko_title != 0:

            time.sleep(3)
            print("파일(F) -> Open API 실행")
            self.app.KOAStudioSA.send_keystrokes("%{F}")
            time.sleep(1)
            self.app.KOAStudioSA.send_keystrokes("{ENTER}")

        else:
            print("KOAStudio is not started")

    def api_login(self,callback=None):
        api_title = Win32Function.check_window('Open API Login', 15)
        if api_title != 0:
            time.sleep(2)
            print(" input password")
            Win32Function.input_string('Open API Login',1001,"vldpfh12")
            time.sleep(2)
            print(" click Login Button")
            Win32Function.click_item('Open API Login',1)
            time.sleep(1)
            print("login 실행")
            if callback is not None and str(type(callback)) == "<class 'function'>":
                print("start " + callback)
                time.sleep(1)
                callback()

        else:
            print("API is not started")

    def version_checker(self,count = 15):
        i = 0
        time.sleep(15)
        a = True
        while i < count:

            print(" version checking....")

            print(" version checking start")
            api_hwnd = Win32Function.check_window('Open API Login')
            if api_hwnd != 0:
                title_list = ["opstarter", "opversionup", "Open API"]
                for title in title_list:
                    time.sleep(1)
                    title_hwnd = Win32Function.check_window(title)
                    print(title +" is checking ... ")
                    if title_hwnd != 0:
                        print(title + " find...")
                        if title == "opstarter":
                            ko_title = Win32Function.check_window('KOA StudioSA ver 2.20', 10)
                            if ko_title != 0:
                                self.app.KOAStudioSA.send_keystrokes("%{F4}")
                            Win32Function.click_item(title,2)
                            time.sleep(10)
                        elif title == "opversionup":
                            Win32Function.click_item(title, 2)
                        elif title == "Open API":
                            Win32Function.click_item(title, 2)

                    else:
                        print(title + " is not existed")
            else:
                print("API is not found")
                title = "업그레이드 확인"
                title_hwnd = Win32Function.check_window(title)
                print(title + " is checking ... ")
                if title_hwnd != 0:
                    print(title + " find...")
                    Win32Function.click_item(title, 1)
                    i = i + 1
                else:
                    print(title + " is not found")
                    a = False
                    break
                    return a
        return a


if __name__ == "__main__":
    update = update_start()
    update.KOAStart()
    update.api_login()
    i = 0
    while i < 10:
        t = update.version_checker(10)
        if t ==False:
            print("end")
            break
    ko_title = Win32Function.check_window('KOA StudioSA ver 2.20', 10)
    if ko_title != 0:
        self.app.KOAStudioSA.send_keystrokes("%{F4}")
    else:
        print("완료")


