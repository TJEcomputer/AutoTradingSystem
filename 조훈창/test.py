import log_recorder
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import configure
import os
from matplotlib import gridspec
import DataPreProcessing

class test:
    def __init__(self):
        self.logging = log_recorder.Log().dir_recorder('RL','visualize')
        self.pre = DataPreProcessing.DataPreProcessing()

    def save_point(self,path,*args):
        if not os.path.exists(path):
            os.makedirs(path)


    def visualizing(self,date=None,category='d'):
        if date is None:
            self.logging.info('시각화할 날짜를 입력해 주세요.')
        path = f'.\\Test\\re_{date}\\'
        if category=='m':
            path = f'.\\Test\\re_{date}_m\\'
        if not os.path.exists(path):
            self.logging.info('현재 해당 폴더가 없습니다. 확인해 주세요.')
        action = pd.read_csv(path+'action.csv')
        quant = pd.read_csv(path+'quant.csv')
        reward = pd.read_csv(path+'reward.csv')
        reward['1'] = 0.0
        stock_cnt = pd.read_csv(path+'stock_cnt.csv')
        obs = pd.read_csv(path+'obs.csv')
        chart_de = pd.read_csv(path+'chart.csv')
        chart = self.pre.change_feature(chart_de)
        chart['date'] = chart_de['date']
        chart['time'] = chart_de['time']
        chart = self.pre.add_feature_df(chart)
        chart[['date','time']] = chart[['date','time']].astype(int)
        chart['datetime'] = chart['date'].astype('str')
        if chart['time'].sum() != 0:
            chart['datetime'] = chart['date'].astype('str') + chart['time'].apply(lambda x: str(x).zfill(4))
        chart['action'] = action['0']
        chart['profit'] = reward['0']
        chart['stock_cnt'] = stock_cnt['0']
        chart['profit_price'] = chart['close'] * chart['profit'].apply(lambda x : 1+x/100)
        chart['diff'] = chart['close'] - chart['open']
        chart['low_high'] = chart['high'] - chart['open']
        chart['color'] = chart['diff'].apply(lambda x: 'red'  if x >0 else 'blue' )


        action_cnt = action['0'].value_counts()
        xticks=[chart['datetime'].values[0],chart['datetime'].values[-1]]
        windows = [5, 10, 20, 60, 120]
        fig = plt.figure(figsize=(1920,900))
        spec = gridspec.GridSpec(ncols=2,nrows=3,height_ratios=[3,1,1],width_ratios=[4,1])
        ax1 =fig.add_subplot(spec[0])
        ax1.plot(chart['close'],label='close')
        ax1.bar(chart['datetime'],height=chart['close']-chart['open'],bottom=chart['open'],width=0.8,color= chart['color'],label ='chart')
        ax1.legend()
        ax1.set_xticks(xticks)

        ax1.legend()

        ax2 = fig.add_subplot(spec[1])
        ax2.pie(action_cnt.values,labels=action_cnt.index,autopct='%1.1f%%')

        ax3 = fig.add_subplot(spec[2])
        ax3.plot(chart['datetime'],chart['close'],label='close')
        ax3.plot(chart['datetime'],chart['profit_price'],label='Profit')
        ax3.scatter(x = chart['datetime'][chart['action']==2],y=chart['close'][chart['action']==2],c='blue',label='Sell')
        ax3.scatter(x = chart['datetime'][chart['action']==1],y=chart['close'][chart['action']==1],c='red',label='Buy')
        for i in chart['datetime'][chart['action']==1].values:
            ax1.axvline(x=i,color='r')
            xticks.append(i)
        ax3.set_xticks(xticks)
        ax3.legend()



        ax5 = fig.add_subplot(spec[4])
        ax5.bar(chart['datetime'],chart['volume'],color=chart['color'],label='volume')
        for i in windows:

            ax5.plot(chart[f'volume_ma{i}'],label=f'volume_ma{i}')
        ax5.set_xticks(xticks)
        ax5.set_ylim([0,60000])
        plt.grid()
        plt.show()


if __name__ == '__main__':
    test = test()
    test.visualizing(20201109,category='m')