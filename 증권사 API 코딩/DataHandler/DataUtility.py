import os.path
import datetime
import pandas as pd
import numpy as np
from DataHandler import CSVHandler

# Date Utility

# 변수 선언
_path = "c:\\users\\TJ\\desktop\\python\\kiwoomtrading\\DB\\CSV\\"
df_merge = pd.DataFrame()

# 현재 년/월/일
def datetime_now():
    dtN = datetime.datetime.now()
    now_dt = dtN.strftime("%Y%m%d")
    return int(now_dt)


def datetime_now_deco(func):
    def wrapper():
        now_dt = datetime_now()

        func(now_dt)

    return wrapper


@datetime_now_deco
def create_db_dir(now_dt):
    dir_ = _path + now_dt
    if os.path.isdir(dir_):
        print("있습니다.")

    else:
        os.makedirs(dir_)
        print(now_dt + " 디렉토리 생성")
    return dir


def file_exists(name):
    path = _path
    filename = path + name
    bool_ = False
    if os.path.isfile(filename):
        bool_ = True
    return bool_


def code_list():
    code_num = []
    code_li = CSVHandler.csv_reader("cyboscode.csv")
    for i in range(1, len(code_li)):
        code_num.append(code_li[i][0])
    return code_num


def file_checker(path=_path):
    file_list = []
    code_li = code_list()
    for code in code_li:
        filename = "min\\" + code + ".csv"
        full_path = path + filename
        if os.path.isfile(full_path):
            file_list.append(code)
    return file_list


def not_exists_file():
    """

    Returns
    -------
    code_s
    """
    exists_file_li = file_checker()
    code_li = code_list()
    code_s = pd.Series(data=code_li, index=code_li)
    # for file in exists_file_li:
    #     code_s = code_s.drop(file)
    code_s = code_s.drop([x for x in exists_file_li])
    code_s = code_s.tolist()
    return code_s


def get_date_time(filename, data_type=None):

    global dt, dtT

    filepath = _path + filename
    if file_exists(filename):
        if pd.read_csv(filepath).empty:
            dtT = 0
        else:
            if data_type == "next_last":
                dfT = pd.read_csv(filepath)["date"].iloc[0]
                dtT = datetime.datetime.strptime(str(dfT), '%Y%m%d') + datetime.timedelta(days=1)
                dtT = int(dtT.strftime('%Y%m%d'))

            elif data_type == "last":


                dtT = pd.read_csv(filepath)["date"].iloc[0]


            elif data_type == "prev_first":
                dfT = pd.read_csv(filepath)["date"].iloc[-1]
                dtT = datetime.datetime.strptime(str(dfT), '%Y%m%d') - datetime.timedelta(days=1)
                dtT = int(dtT.strftime('%Y%m%d'))

            elif data_type == "time":
                dtT = pd.read_csv(filepath)["time"].iloc[0:2].tolist()

        return dtT


# 파라미터로 넘겨 받은 데이터의 타입에 따라 process를 진행 후 date_list를 반환한다.
def date_list_(data_):
    date_du = data_["date"].drop_duplicates()  # 날짜데이터 "date"컬럼 > 중복값들 합치기
    date_list = date_du.tolist()  # 중복 값이 합쳐진 DataFrame을 List로 만들어 변수에 저장
    return date_list  # List 반환


# 9:01 ~ 15:30 까지의 시간데이터 List를 반환하는 time_list_()
def time_list_():
    time_li = np.arange(901, 1531)
    del_li = list(map(lambda x: x % 100 > 59, time_li))
    time_li = np.delete(time_li, del_li)
    return time_li


# DataFrame을 Parameter로 받아 날짜/시간 DataFrame을 반환하는 df_bean_()
def df_bean_(data_):
    dt_li = []  # [날짜,시간]으로 이루어진 list를 담을 list를 선언한다.
    time_li = time_list_()  # time_list_()를 통해 장중 시간 list를 가져온다.
    date_li = np.array(date_list_(data_))
    # parameter로 받은 DataFrame을 date_list_()의 argument로 넘겨주어 날짜 리스트를 반환받는다.
    # 이를 np.array를 통해서 ndarray로 만든다.

    for date in date_li:  # 날짜 데이터 리스트의 요소들을 꺼낸다
        for time in time_li:  # 시간 데이터 리스트의 요소들을 꺼낸다.
            dt_li.append([date, time])  # 날짜별 시간 데이터들을 [날짜,시간] List로 만들어 dt_li에 넣는다.
    dt_bean = pd.DataFrame(dt_li, columns=['date', 'time'])  # dt_li를 데이터로 하고 columns명이 date, time인 DateFrame을 만든다.
    return dt_bean  # dt_bean 을 반환한다.


def df_merge_(df_dic):
    df_merge = pd.merge(df_dic, df_bean_(df_dic), on=['date', 'time'], how='outer')
    df_merge.sort_values(by=['date', 'time'], ascending=False, inplace=True)
    df_merge.reset_index(drop=True, inplace=True)
    df_merge[['volume', 'tr_amount']] = df_merge[['volume', 'tr_amount']].fillna(0)
    df_merge[['close', 'sales_qu', 'purchase_qu']] = df_merge[['close', 'sales_qu', 'purchase_qu']].fillna(
        method='bfill')
    df_merge['open'] = df_merge['open'].combine_first(df_merge['close'])
    df_merge['high'] = df_merge['high'].combine_first(df_merge['close'])
    df_merge['low'] = df_merge['low'].combine_first(df_merge['close'])
    close = df_merge['close']
    prev_close = close.shift(-1)
    df_merge['prev'] = (close - prev_close)
    return df_merge


def drop_row(df_):

    df_index = df_[df_['time'] == 0].index
    df_.drop(df_index, inplace=True)

    return df_

