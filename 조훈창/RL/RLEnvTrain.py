import numpy as np
import pandas as pd
class RLEnv:
    def __init__(self,df,max_quantity = 10):
        self.df = df
        self.iloc = 0
        self.done = False
        self.stock_list = []
        self.total_stock = 0
        self.price_list = []
        self.profit_list = []
        self.max_quantity = max_quantity
        self.cash = 10000000
    def reset(self):
        self.iloc = 0
        self.stock_list = []
        self.total_stock = 0
        self.price_list = []
        self.profit_list = []
        self.init_cash = 10000000
        self.cash = 10000000
        self.portfolio =10000000
        self.reward =0
        return self.obs()


    def obs(self):
        obs = None
        if self.iloc < len(self.df):
            obs = self.df.iloc[self.iloc].values
        return obs

    def next_step(self,action,quant):

        cu_price = self.obs()[1]
        profit = self.profit(cu_price)
        self.price_list.append(cu_price)

        done = False

        if self.iloc +1 >= len(self.df):
            done = True

        if action == 0:


            self.profit_list.append(profit)
            self.stock_list.append([0,0])
           # print('Hold',reward)

        if action == 1:


            self.profit_list.append(profit)
            self.total_stock += quant
            self.stock_list.append([quant, cu_price])
            self.cash -= cu_price * quant
          #  print('Buy',reward,'Qunt:' , quant)
        if action == 2:


            self.profit_list.append(profit)
            self.total_stock += -1 * quant
            self.stock_list.append([-1 * quant, cu_price])
            self.cash += cu_price * quant
          #  print('Sell',reward,'Qunt:' , quant)
        self.portfolio = self.cash + cu_price * self.total_stock
        self.reward = (self.portfolio - self.init_cash) / self.init_cash * 100
        # 리워드 어떻게 줄지
        self.iloc += 1
        next_obs = self.obs()
        info = None
        return next_obs,self.reward,done,info


    def validation_(self,action,quant,price):
        if action==1 and  (quant * price) > self.cash:
            return False
        elif action==2 and quant > self.total_stock:
            return False

        return True

    def profit(self,cu_price):
        holding_stock = 0
        cu_stock = 0
        profit = 0
        if self.total_stock != 0:
            for stock in self.stock_list:
                holding_stock += stock[0] * stock[1]
            cu_stock = cu_price * self.total_stock
            profit = (cu_stock - holding_stock) / holding_stock * 100
       # print('cu_price',cu_price ,'cu_stock : ',cu_stock,'holding : ',holding_stock,' total_stock : ',self.total_stock)
       # print('profit',profit)
        return profit

# if __name__ == '__main__':
#     cc = RLEnv(pd.read_csv('.\\DB\\CSV\\daily\\DA000020_ch.csv'))
#     cc.obs()