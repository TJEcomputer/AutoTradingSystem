import os
import pandas as pd
import log_recorder
import numpy as np
from tqdm import tqdm


class DataPreProcessing:
    def __init__(self, path = f'.\\DB\\CSV\\'):
        # 필요 변수 선언
        self.name = 'DataPreProcessing'
        self.path = path
        self.logging = log_recorder.Log().dir_recorder('RL','Dataprepro')

        # DataPreProcessing 클래스 객체 생성시 필요한 폴더 생성
        self.mkdir = self.make_dir(path)

    def change_csv(self,code='A000020',category='d'):
        if code is None:
            self.logging.info('변환할 데이터가 없습니다.')
            return
        load_file = code + '.csv'
        path = '.\\DB\\CSV\\daily\\'
        load_path = path + load_file
        df = pd.read_csv(load_path)
        if category == 'm':
            path = '.\\DB\\CSV\\min\\'
            load_path = path + load_file
            df = pd.read_csv(load_path)
            df = self.min_preprocessing(df)
        df = df
        df.sort_values(by='date',inplace=True)
        df_stock = df[['date','open','close','high','low','volume']].copy()
        df_stock['prev_close'] = df_stock['close'].shift(1)
        df_stock['prev_diff'] = df_stock['close'] - df_stock['prev_close']
        df_stock['prev_volume'] = df_stock['volume'].shift(1)
        df_stock['volume_diff'] = df_stock['volume'] - df_stock['prev_volume']
        df_stock.dropna(inplace=True)
        df_stock_ch = df_stock[['prev_close','close','prev_diff','open','high','low','volume','prev_volume','volume_diff']].copy()
        df_stock_ch.reset_index(inplace=True)
        df_stock_ch.drop(['index'],axis=1,inplace=True)
        df_stock_ch['profit'] = 0
        df_stock_ch['cash'] = 0
        df_stock_ch['volume'].replace(0, method='ffill', inplace=True)
        save_path = path + code +'_ch.csv'
        df_stock_ch.to_csv(save_path,index=False)
        return df_stock_ch

    def min_preprocessing(self,df):
        df_bean = self.make_bean(df)
        df_merged = pd.merge(df,df_bean,on=['date','time'],how='outer').sort_values(by=['date','time'],ascending=True)
        df_merged=df_merged.astype(float)
        df_merged[['volume','tr_amount']]=df_merged[['volume','tr_amount']].fillna(0.0)
        df_merged[['close','sales_qu','purchase_qu']]=df_merged[['close','sales_qu','purchase_qu']].fillna(method='ffill')
        df_merged['open'] = df_merged['open'].combine_first(df_merged['close'])
        df_merged['high'] = df_merged['high'].combine_first(df_merged['close'])
        df_merged['low'] = df_merged['low'].combine_first(df_merged['close'])
        close = df_merged['close']
        prev_close = close.shift(1)
        df_merged['prev'] = (close - prev_close)
        return df_merged

    def make_dir(self,path=None):
        if path is None:
            path = self.path
        dir_list = ['min','daily','month']
        for dir in dir_list:
            path_dir = path + dir +'\\'
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

    def make_bean(self,df):

        df_time = df[df['time'] == 1630]['date'].values
        date = df['date'].drop_duplicates().values
        datetime = []

        date = np.array(date)
        for date_el in tqdm(date):
            time_range = range(901, 1531)
            if date_el in df_time:
                time_range = range(901, 1631)
            for i in time_range:
                if i % 100 <= 59:
                    datetime.append([date_el,i])
        df_bean = pd.DataFrame(datetime,columns=['date','time'])
        return df_bean

    def train_test_split(self,code,day=252,year=1,test_year=1,full_year =5,category='d',sel=None):
        if category == 'm':
            day = 30
            day = day * 390
            test_year = 1
            full_year =3
        df = self.change_csv(code, category=category)
        df_prev = df.iloc[-1*day*(year*full_year) - 120:-1*day*(year*full_year),:].copy()

        df_prev.reset_index(drop=True,inplace=True)
        df_train = df.iloc[-1*day*(year*full_year):-1*day*year*test_year].copy()

        df_train.reset_index(drop=True,inplace=True)
        df_test = df.iloc[-1*day*year*test_year:].copy()

        df_test.reset_index(drop=True,inplace=True)
        if sel == None:

            return df_train,df_test,df_prev
        if sel =='prev':
            return df_prev


    def add_feature(self,df):

        df = df.copy()
        windows = [5, 10, 20, 60, 120]
        for window in windows:
            df[f'close_ma{window}'] = df['close'].rolling(window).mean()
            df[f'volume_ma{window}'] = df['volume'].rolling(window).mean()
            df[f'close_ma_latio{window}'] = (df['close'] - df[f'close_ma{window}']) / df[f'close_ma{window}']
            df[f'volume_ma_latio{window}'] = (df['volume'] - df[f'volume_ma{window}']) / df[f'volume_ma{window}']
        data = df.iloc[-1]
        data = data.values

        return data

# if __name__ == '__main__':
#     pre = DataPreProcessing()
#     code = 'A000020'
#     pre.change_csv(code,category='m')
#     df = pd.read_csv('.\\DB\\CSV\\min\\A000020.csv')
#     pre.train_test_split(df)