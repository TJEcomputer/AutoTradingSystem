import csv

import pandas as pd

from DataHandler import DataUtility

_path = 'C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\'
res_li = ['date', 'time', 'open', 'high', 'low', 'close', 'prev', 'volume', 'tr_amount', 'sales_qu', 'purchase_qu']
def csv_reader(name):
    filename = _path+name
    f = open(filename,'r',encoding='utf-8-sig')
    data = csv.reader(f)
    data_list = []
    for i in data:
        data_list.append(i)
    return data_list
    f.close()



def csv_writer_a(name,rows):
    filename = _path+name
    f = open(filename,'a',encoding='utf-8-sig',newline='')
    wr = csv.writer(f)

    wr.writerow(rows)
    f.close()

def csv_writer_w(name,rows):
    filename = _path+name
    f = open(filename,'w',encoding='utf-8-sig',newline='')
    wr = csv.writer(f)

    wr.writerow(rows)
    f.close()

def pd_write(name,res_li,col_li):
    filename = _path + name
    df_data=pd.DataFrame(res_li,columns=col_li)
    df_data.to_csv(filename,index=False,encoding='utf-8-sig')

def pd_update(name,res_li,col_li,Dm = "m"):
    filename = _path + name
    df_dic = pd.DataFrame(res_li, columns=col_li)
    df_data = pd.read_csv(filename)
    if Dm == "m":
        df_merge = DataUtility.df_merge_(df_dic)

        if df_merge["date"].iloc[-1] == df_data["date"].iloc[0]:
            tt= df_data[df_data["date"] == df_data["date"].iloc[0]].index
            df_data.drop(tt,inplace=True)

        df_data = pd.merge(df_data,df_merge,on=col_li,how='outer').sort_values(by=['date','time'],ascending=False)
    else:


        if df_dic["date"].iloc[-1] == df_data["date"].iloc[0]:
            tt = df_data[df_data["date"] == df_data["date"].iloc[0]].index
            df_data.drop(tt, inplace=True)

        df_data = pd.merge(df_data,df_dic,on=col_li,how='outer').sort_values(by=['date','time'],ascending=False)
    if df_data.isnull().sum().sum() != 0:
        close = df_data['close']
        prev_close = close.shift(-1)
        df_data['prev'] = df_data['prev'].fillna(close - prev_close)
    print(df_data)
    df_data.to_csv(filename,index=False,encoding='utf-8-sig')

def pd_append(name,res_li,col_li):


    filepath = _path + name
    df_st = pd.read_csv(filepath)

    if df_st.isnull().sum().sum() != 0 :
        df_dic = pd.DataFrame(res_li, columns=col_li)
        df_merge = pd.merge(df_st, df_dic, on=col_li, how='outer')
        df_merge.sort_values(by=['date', 'time'], ascending=False, inplace=True)
        df_merge.reset_index(drop=True, inplace=True)
        df_merge[['volume', 'tr_amount']] = df_merge[['volume', 'tr_amount']].fillna(0)
        df_merge[['close',  'sales_qu', 'purchase_qu']] = df_merge[['close',  'sales_qu', 'purchase_qu']].fillna(method='bfill')
        df_merge['open'] = df_merge['open'].combine_first(df_merge['close'])
        df_merge['high'] = df_merge['high'].combine_first(df_merge['close'])
        df_merge['low'] = df_merge['low'].combine_first(df_merge['close'])
        close = df_merge['close']
        prev_close = close.shift(-1)
        df_merge['prev'] = df_merge['prev'].fillna(close - prev_close)
        df_index = df_merge[df_merge['time'] == 0].index
        df_merge.drop(df_index, inplace=True)
        df_merge.fillna(0,inplace=True)
        df_merge.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(df_merge)
    else:
        print("Nan 값이 없습니다. ")

def null_fill(code):
    filename = "min\\"+code+".csv"
    dt_li = [1530, 1529]

    dt = DataUtility.get_date_time(filename, data_type="time")
    if dt_li != dt:
        print(code + " 결측치 채우기 시작")
        filename = _path + "min\\"+code + ".csv"
        df_dic = pd.read_csv(filename)
        df_dic = DataUtility.df_merge_(df_dic)
        df_dic.to_csv(filename, index=False, encoding='utf-8-sig')
        print(df_dic)
        print(code + " 결측치 채우기 완료")
    else:
        print(code + "작업이 완료 되었습니다.")



