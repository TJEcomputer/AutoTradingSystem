import pandas as pd
import talib as ta
import os
import multiprocessing
class create_talib:
    def __init__(self):
        self.dbpath = 'C:\\Users\\TJ\\Desktop\\python\\kiwoomtrading\\DB\\CSV\\daily\\'
    def preprocessing(self,df=None):
        if df.empty:
            print(' DataFrame is None')
        else:
            df.sort_values(by='date', ascending=True, inplace=True)
        return df
    def get_df(self,filename = 'DA000020.csv'):
        df = pd.read_csv(self.dbpath + filename)
        df = self.preprocessing(df)
        return df
    def add_SMA(self,df,periods = [5,10,20,30,60,120]):

        for i in periods:
            period = str(i)
            df['SMA_'+period] = ta.SMA(df['close'],timeperiod=i)
        return df
    def add_BBANDS(self,df,periods = [5,10,20,30,60,120], nbdevup=2, nbdevdn=2, matype=0):
        for i in periods:
            period = str(i)
            df['BBANDS_'+period + '_UPPER'],df['BBANDS_'+period + '_MIDDLE'],df['BBANDS_'+period + '_LOWER'] = ta.BBANDS(df['close'],timeperiod = i, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype)
        return df

    def add_DEMA(self, df, periods=[5, 10, 20, 30, 60, 120]):
        for i in periods:
            period = str(i)
            df['DEMA_' + period] = ta.DEMA(df['close'], timeperiod=i)
        return df
    def add_EMA(self, df, periods=[5, 10, 20, 30, 60, 120]):
        for i in periods:
            period = str(i)
            df['EMA_' + period] = ta.EMA(df['close'], timeperiod=i)
        return df
    def add_HT_TRENDLINE(self, df):
        df['HT_TRENDLINE_'] = ta.HT_TRENDLINE(df['close'])
        return df
    def add_KAMA(self, df, periods=[5, 10, 20, 30, 60, 120]):
        for i in periods:
            period = str(i)
            df['KAMA_' + period] = ta.KAMA(df['close'], timeperiod=i)
        return df
    def add_MA(self, df, periods=[5, 10, 20, 30, 60, 120], matype=0):
        for i in periods:
            period = str(i)
            df['MA_' + period] = ta.MA(df['close'], timeperiod=i, matype=matype)
        return df
    def add_MAMA(self, df):
        df['MAMA_'],df['FAMA_'] = ta.MAMA(df['close'])
        return df
    def add_MIDPOINT(self, df, periods=[5, 10, 14, 20, 30, 60, 120]):
        for i in periods:
            period = str(i)
            df['MIDPOINT_' + period] = ta.MIDPOINT(df['close'], timeperiod=i )
        return df

    def add_MIDPRICE(self, df, periods=[5, 10,14, 20, 30, 60, 120]):
        for i in periods:
            period = str(i)
            df['MIDPRICE_' + period] = ta.MIDPRICE(df['high'],df['low'], timeperiod=i )
        return df

    def add_SAR(self, df, acceleration=0, maximum=0):

        df['SAR_'] = ta.SAR(df['high'],df['low'], acceleration=acceleration, maximum=maximum )
        return df
    def add_SAREXT(self, df, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0):

        df['SAREXT_'] = ta.SAREXT(df['high'],df['low'], startvalue=startvalue, offsetonreverse=offsetonreverse, accelerationinitlong=accelerationinitlong, accelerationlong=accelerationlong, accelerationmaxlong=accelerationmaxlong, accelerationinitshort=accelerationinitshort, accelerationshort=accelerationshort, accelerationmaxshort=accelerationmaxshort)
        return df
    def add_T3(self, df, periods=[5, 10, 20, 30, 60, 120], vfactor=0):
        for i in periods:
            period = str(i)
            df['T3_' + period] = ta.T3(df['close'], timeperiod=i, vfactor=vfactor)
        return df
    def add_TEMA(self, df, periods=[5, 10, 20, 30, 60, 120]):
        for i in periods:
            period = str(i)
            df['TEMA_' + period] = ta.TEMA(df['close'], timeperiod=i)
        return df
    def add_TRIMA(self, df, periods=[5, 10, 20, 30, 60, 120]):
        for i in periods:
            period = str(i)
            df['TRIMA_' + period] = ta.TRIMA(df['close'], timeperiod=i)
        return df
    def add_WMA(self, df, periods=[5, 10, 20, 30, 60, 120]):
        for i in periods:
            period = str(i)
            df['WMA_' + period] = ta.WMA(df['close'], timeperiod=i)
        return df

    def add_all_talib(self,filename):
        df = self.get_df(filename)

        self.add_SMA(df)
        self.add_BBANDS(df)
        self.add_DEMA(df)
        self.add_EMA(df)
        self.add_HT_TRENDLINE(df)
        self.add_KAMA(df)
        self.add_MA(df)
        self.add_MAMA(df)
        self.add_MIDPOINT(df)
        self.add_MIDPRICE(df)
        self.add_SAR(df)
        self.add_SAREXT(df)
        self.add_T3(df)
        self.add_TEMA(df)
        self.add_TRIMA(df)

        df.to_csv(self.dbpath + 'daily_ta\\ta_'+filename)
        print(filename)
        return df

if __name__ == '__main__':
    talib_ = create_talib()
    # filename = 'DA000020.csv'
    # df = create_talib.get_df(filename)
    # df = create_talib.add_all_talib(df)
    # df.to_csv(create_talib.dbpath + 'daily_ta\\ta_' +filename )
    filenames = os.listdir(talib_.dbpath)

    print("데이터 수집 시작")
    # Multi Process 시작 > processes 개수 결정 > Maximum 현재 PC사양 *2
    pool = multiprocessing.Pool(processes=6)  # 최대 8개
    # 실행할 메소드 , 반복할 List 입력
    pool.map(talib_.add_all_talib, filenames)
    pool.close()
    pool.join()


