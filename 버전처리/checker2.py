import time

import pywinauto
import Win32Function

class update_start:

    def __init__(self):
        pass



    def version_checker(self,count):
        i = 0
        while i < count:
            i = i + 1
            print(" version checking....")
            time.sleep(10)
            print(" version checking start")
            api_hwnd = Win32Function.check_window('Open API Login')
            if api_hwnd != 0:
                title_list = ["opstarter", "opversionup", "업그레이드 확인", "Open API"]
                for title in title_list:
                    time.sleep(1)
                    title_hwnd = Win32Function.check_window(title)
                    print(title +" is checking ... ")
                    if title_hwnd != 0:
                        print(title + " find...")
                        if title == "opstarter":


                            Win32Function.click_item(title,2)

                        elif title == "opversionup":
                            Win32Function.click_item(title, 2)

                        elif title == "업그레이드 확인":
                            Win32Function.click_item(title, 2)

                        elif title == "Open API":
                            Win32Function.click_item(title, 2)

                    else:
                        print(title + " is not existed")
            else:
                print("API is not found")
                break
                return False

if __name__ == "__main__":
    update = update_start()

    while True:
     update.version_checker(30)



