import multiprocessing
import time

import pywinauto
import win32com.client
import pandas as pd
from DataHandler import CSVHandler, DataUtility
from connect.VersionUpdate import Win32Function

done_li = []


def cybosapi_start():
    print("프로그램 실행")
    app = pywinauto.application.Application()
    app.start("C:/DAISHIN/STARTER/ncStarter.exe") # 대신증권 API 설치 경로를 입력해주세요.
    print("프로그램 실행 확인")
    api_title = Win32Function.check_window('CYBOS Starter', 20)
    if api_title != 0:
        time.sleep(3)
        print("프로그램 실행 확인 완료")
        Win32Function.click_item("CYBOS Starter", 338)
        time.sleep(3)
        Win32Function.input_string("CYBOS Starter", 157, "***") # * 부분에 비밀번호를 넣어 주세요.
        Win32Function.input_string("CYBOS Starter", 158, "***") # * 부분에 공인인증서 비밀번호를 넣어주세요
        Win32Function.click_item("CYBoS Starter", 203)
        noti_title = Win32Function.check_window("공지사항", 60)
        if noti_title != 0:
            Win32Function.close_win("공지사항")
        else:
            print("없습니다.")

    else:
        print("CYBOS is not started")
    api_login_status()


def api_login_status():
    instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    if instCpCybos.IsConnect == 1:
        print("연결 성공")


    else:

        print("연결 실패")
        print("프로그램 실행 대기")
        time.sleep(3)

        cybosapi_start()
    return instCpCybos.IsConnect


def get_code():
    file = "cyboscode.csv"
    columns_list = ['stock_code','stock_name']
    CodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    codeList = CodeMgr.GetStockListByMarket(1)
    data_list =[]
    for i, code in enumerate(codeList):
        name = CodeMgr.CodeToName(code)
        data_sub_list = [code,name]
        data_list.append(data_sub_list)
    CSVHandler.pd_write(file,data_list,columns_list)
    return codeList
def get_code2():

    stock_data = win32com.client.Dispatch("Dscbo1.StockMst2")
    stock_df = pd.read_csv('C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\volume100.csv')
    stock_code_list = stock_df['stock_code'].tolist()
    N = len(stock_code_list)
    for nn in range(N//100+1):

        code = ''
        start = nn *100
        end = nn*100+100
        if end > N or ( N<100 and end<N):
            end = N
        stock_code_list_split = stock_code_list[start:end]
        for k in stock_code_list_split:
            if k != stock_code_list_split[-1]:
                code += k +','
            else:
                code += k

        print(code)
        stock_data.SetInputValue(0,code)
        stock_data.BlockRequest()
        data_size = stock_data.GetHeaderValue(0)
        for i in range(data_size):
            stock_code = stock_data.GetDataValue(0,i)
            stock_current_price = stock_data.GetDataValue(3,i)
            print(str(start)+':'+str(end) + ' ' + str(i) + ' ',stock_code,stock_current_price)

        time.sleep(0.4)


def marketeye():
    stock_data = win32com.client.Dispatch("CpSysDib.MarketEye")
    stock_df = pd.read_csv('C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\cyboscode.csv',encoding='utf-8-sig')
    columns_list = ['stock_code', 'stock_name','stock_time',  'current_price', 'open', 'high', 'low', 'volume',
                      'prev_close']
    rq_list = [0, 1, 2, 4, 5, 6, 7, 10, 12, 17, 23]
    stock_code_list = stock_df['종목코드'].tolist()
    N = len(stock_code_list)
    data_list = []
    for nn in range(N//200+1):
        time.sleep(0.4)
        start = nn*200
        end = nn*200+200
        if end > N:
            end = N

        stock_code_list_split = stock_code_list[start:end]


        stock_data.SetInputValue(0,rq_list)
        stock_data.SetInputValue(1, stock_code_list_split)
        stock_data.SetInputValue(2,1)
        stock_data.BlockRequest()
        cnt = stock_data.GetHeaderValue(2)
        for i in range(cnt):
            stock_code = stock_data.GetDataValue(0,i)
            stock_time = stock_data.GetDataValue(1, i)
            compare_sign = stock_data.GetDataValue(2, i)
            current_price = stock_data.GetDataValue(3, i)
            open = stock_data.GetDataValue(4, i)
            high = stock_data.GetDataValue(5, i)
            low = stock_data.GetDataValue(6, i)
            volume = stock_data.GetDataValue(7, i)
            market_state = stock_data.GetDataValue(8, i)
            stock_name = stock_data.GetDataValue(9, i)
            prev_close = stock_data.GetDataValue(10, i)
            data_sub_list =[stock_code,stock_name,stock_time,current_price,open,high,low,volume,prev_close]
            data_list.append(data_sub_list)
    CSVHandler.pd_write('stockdata.csv',data_list,columns_list)
def get_volume_top100():
    stock_df = pd.read_csv('C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\stockdata.csv',encoding='utf-8-sig')
    stock_df.sort_values(by='volume',ascending=False,inplace=True,ignore_index=True)
    stock_split = stock_df.iloc[:101]
    stock_split.to_csv('C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\volume100.csv',encoding='utf-8-sig',index=False)
def get_data(code, filename, end=0, start=19900101, Dm='m', update=0, col_='m'):
    if col_ == "m":
        col_li = ['date', 'time', 'open', 'high', 'low', 'close', 'prev', 'volume', 'tr_amount', 'sales_qu',
                  'purchase_qu']
        rq_li = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11]
    elif col_ == "D":
        col_li = ['date', 'time', 'open', 'high', 'low', 'close', 'prev', 'volume', 'tr_amount', 'sales_qu',
                  'purchase_qu', 'li_share', 'market_cap', 'fr_cu_holding', 'fr_cu_ratio', 'ad_pr_ratio', 'in_net_buy',
                  'up_do', 'up_do_ratio', 'deposit', 'st_turnover', 'tr_es_ratio', 'sign']
        rq_li = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 16, 17, 19, 20, 22, 23, 24, 25, 26, 37]
    stock_data = win32com.client.Dispatch("CpSysDib.StockChart")
    stock_data.SetInputValue(0, code)
    stock_data.SetInputValue(1, ord('1'))
    stock_data.SetInputValue(2, end)
    stock_data.SetInputValue(3, start)
    stock_data.SetInputValue(5, rq_li)

    stock_data.SetInputValue(6, ord(Dm))
    stock_data.SetInputValue(7, 1)
    stock_data.SetInputValue(8, 1)
    stock_data.SetInputValue(9, 1)

    res_full_li = []
    datacnt = 0
    while True:
        stock_data.BlockRequest()
        rqStatus = stock_data.GetDibStatus()
        rqRet = stock_data.GetDibMsg1()
        if rqStatus != 0:
            print("통신상태", rqStatus, rqRet)
            return False

        numVal = stock_data.GetHeaderValue(3)

        for i in range(numVal):
            # date = stock_data.GetDataValue(0,i) # 0. 날짜
            # time = stock_data.GetDataValue(1, i)# 1. 시간
            # start = stock_data.GetDataValue(2, i)# 2. 시가
            # high = stock_data.GetDataValue(3, i)# 3. 고가
            # low = stock_data.GetDataValue(4, i)# 4. 저가
            # close = stock_data.GetDataValue(5, i)# 5. 종가
            # prev = stock_data.GetDataValue(6, i)# 6. 전일대비 (37대비부호와 같이 사용)
            # volume = stock_data.GetDataValue(7, i)# 8. 거래량
            # tr_amount = stock_data.GetDataValue(8, i)# 9. 거래대금
            # sales_qu = stock_data.GetDataValue(9, i)# 10. 누적체결매도수량
            # purchase_qu = stock_data.GetDataValue(10, i)# 11. 누적체결매수수량
            # con_sign = stock_data.GetDataValue(11, i)# 37. 대비부호
            # res_li = [date,time,start,high,low,close,prev,volume,tr_amount,sales_qu,purchase_qu,con_sign]
            # res_li = []
            # for col in range(len(col_li)):
            #     data = stock_data.GetDataValue(col, i)
            #     res_li.append(data)
            res_li = list(map(lambda x: stock_data.GetDataValue(x, i), range(len(col_li))))
            res_full_li.append(res_li)
            print(res_li)
        datacnt += numVal
        if stock_data.Continue == False:
            break
    if update == 0:
        CSVHandler.pd_write(filename, res_full_li, col_li)
    elif update == 1:
        CSVHandler.pd_update(filename, res_full_li, col_li, Dm=Dm)
    elif update == 2:
        CSVHandler.pd_append(filename, res_full_li, col_li)


def thema_data():
    stock_data = win32com.client.Dispatch("Dscbo1.CpSvr8561")
    stock_data.BlockRequest()
    header = stock_data.GetHeaderValue(0)
    thema_data_li = []
    for i in range(header):
        thema_data_list=[]
        thema_code =stock_data.GetDataValue(0,i)
        thema_index = stock_data.GetDataValue(1,i)
        thema_name = stock_data.GetDataValue(2,i)
        thema_data_list = [thema_index,thema_code,thema_name]
        thema_data_li.append(thema_data_list)
    CSVHandler.pd_write('thema\\themadata.csv',thema_data_li,['thema_index','thema_code','thema_name'])

def thema_stock():
    thema_df = pd.read_csv('C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\thema\\themadata.csv')
    thema_code_list = thema_df['thema_code'].tolist()
    thema_name_list = thema_df['thema_name'].tolist()
    stock_data = win32com.client.Dispatch("Dscbo1.CpSvr8561T")
    data_list = []
    column_list = ['data_code','thema_name','stock_code','stock_name','stock_current_print']
    for thema_code,thema_name in zip(thema_code_list,thema_name_list):
        stock_data.SetInputValue(0,thema_code)
        stock_data.BlockRequest()
        data_code = stock_data.GetHeaderValue(0)
        data_size = stock_data.GetHeaderValue(1)
        data_comment = stock_data.GetHeaderValue(2)

        for i in range(data_size):
            stock_code = stock_data.GetDataValue(0,i)
            stock_name = stock_data.GetDataValue(1,i)
            stock_current_print = stock_data.GetDataValue(2,i)
            data_sub_list = [data_code,thema_name,stock_code,stock_name,stock_current_print]
            data_list.append(data_sub_list)
    CSVHandler.pd_write('thema\\themacodelist.csv',data_list,column_list)
def update_date(code):
    filename = "min\\" + code + ".csv"
    print(code + "업데이트 시작")
    now = DataUtility.datetime_now()

    if DataUtility.file_exists(filename) == True:
        last = DataUtility.get_date_time(filename, data_type="last")
        next_last = DataUtility.get_date_time(filename, data_type="next_last")

        if str(last) == "0":
            print(code + " 데이터가 없습니다.")
            get_data(code, filename=filename)
            CSVHandler.null_fill(code)
            append_data(code)
            update_date(code)
            print(code + " 입력 완료")
        else:
            print(code + " 파일이 있습니다.")
            print(code + " : " + str(last) + "부터 " + str(now) + "까지 업데이트 시작")
            get_data(code, filename=filename, start=last, update=1)
            done_li.append(code)
            print(len(done_li))
            print(code + "업데이트 완료")
    elif DataUtility.file_exists(filename) == False:
        print(code + " 파일이 없습니다.")
        get_data(code, filename=filename)
        CSVHandler.null_fill(code)
        append_data(code)
        update_date(code)
        print(code + " 입력 완료")


def update_date_daily(code):
    filename = "daily\\D" + code + ".csv"
    print(code + "업데이트 시작")
    now = DataUtility.datetime_now()

    if DataUtility.file_exists(filename) == True:
        last = DataUtility.get_date_time(filename, data_type="last")
        next_last = DataUtility.get_date_time(filename, data_type="next_last")
        if str(last) == "0":
            print(code + " 데이터가 없습니다.")
            get_data(code, filename=filename, Dm="D", col_='D')
            update_date_daily(code)
            print(code + " 입력 완료")
        else:
            print(code + " 파일이 있습니다.")
            print(code + " : " + str(last) + "부터 " + str(now) + "까지 업데이트 시작")
            get_data(code, filename=filename, start=last, Dm="D", update=1, col_='D')
            done_li.append(code)
            print(len(done_li))
            print(code + "업데이트 완료")

    elif DataUtility.file_exists(filename) == False:
        print(code + " 파일이 없습니다.")
        get_data(code, filename=filename, Dm="D", col_='D')

        update_date_daily(code)
        print(code + " 입력 완료")


def append_data(code):
    _path = 'C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\'
    filename = "min\\" + code + ".csv"

    if DataUtility.file_exists(filename):

        df_st = pd.read_csv(_path + filename)

        if df_st.isnull().sum().sum() != 0:
            first_date = DataUtility.get_date_time(filename, data_type="prev_first")
            print(code + " 데이터 입력")
            get_data(code, filename, end=first_date, start=(first_date - 5), Dm='D', update=2, col_='m')
            print(code + "추가 완료 완료")
        else:
            print(code + "결측치가 없습니다.")
    else:
        print(code + " 파일이 없습니다.")


def processing_(code):
    update_date(code)
    update_date_daily(code)


def recolumns(code):
    _path = 'C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\'
    filename = "min\\" + code + ".csv"
    filepath = _path + filename
    df_st = pd.read_csv(filepath)
    df_st.rename({'start': 'open'}, axis='columns', inplace=True)
    df_st.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(filename)


if __name__ == "__main__":

    status_ = api_login_status()
    if status_ == 1:

        print("데이터 수집 시작")
        while True:
            now = time.time()
            tm = time.localtime(now)
            now_str = time.strftime('%H:%M',tm)
            time.sleep(0.1)
            if now_str == "15:02":
                print('break'+now_str)
                break
            print(now_str)
            get_code2()
        thema_data()
        thema_stock()
        print("수집 완료")