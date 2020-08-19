import sys
import pandas as pd
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import QMainWindow, QApplication


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        self.kiwoom.OnEventConnect.connect(self.event_connect)




        


    def event_connect(self,err_code):
        if err_code == 0:
            print("로그인 성공")
            tl = QLabel(self)
            tl.setText("로그인 성공")
            ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
            kospi_code_list = ret.split(';')
            kospi_code_name_list = []

            # fw = open("code.csv","w")
            # fw.write("종목코드" + ',' + "종목명" + '\n')
            #
            # fa = open('code.csv','a')
            for x in kospi_code_list:
                name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
                kospi_code_name_list.append(name)
                # fa.write(x + ',' + name + '\n')
            data = {"종목 코드" : kospi_code_list,"종목명":kospi_code_name_list}
            pddata = pd.DataFrame(data)
            pddata.to_csv("code.csv",encoding='euc-kr') #한글깨짐 utf-8-sig


            print(data)
            # fa.close()
            myWindow.show()



    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
        kospi_code_list = ret.split(';')
        kospi_code_name_list = []

        for x in kospi_code_list:
            name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
            kospi_code_name_list.append(x + " : " + name)

        self.listWidget.addItems(kospi_code_name_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()

    app.exec_()