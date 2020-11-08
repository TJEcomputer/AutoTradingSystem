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
        self.cash = 1000000
        self.init_cash = 1000000
    def reset(self):
        self.iloc = 0
        self.stock_list = []
        self.total_stock = 0
        self.price_list = []
        self.profit_list = []
        self.init_cash = 1000000
        self.cash = 1000000
        self.reward =0
        return self.obs()

    # 실제 환경과 테스트환경 분리
    def obs(self):
        obs = None
        if self.iloc < len(self.df):
            obs = self.df.iloc[self.iloc].values
            obs[9] = self.reward
            obs[10] = self.cash
        return obs

    def next_step(self,action,quant):

        cu_price = self.obs()[1]
        self.price_list.append(cu_price)

        done = False

        if action == 0:
            self.stock_list.append([0,0])
           # print('Hold',reward)

        if action == 1:
            self.total_stock += quant
            self.stock_list.append([quant, cu_price])
            profit_charged = self.profit(action,cu_price, quant)
            self.cash -= int(profit_charged)

        if action == 2:

            self.total_stock += -1 * quant
            self.stock_list.append([-1 * quant, cu_price])
            profit_charged = self.profit(action,cu_price, quant)
            self.cash += int(profit_charged)

        portfolio = self.cash + cu_price * self.total_stock
        self.reward = (portfolio - self.init_cash) / self.init_cash * 100
        if action == 0 and self.total_stock==0:
            self.reward = 0
        self.profit_list.append(self.reward)
        # 리워드 어떻게 줄지
        self.iloc += 1
        next_obs = self.obs()
        if next_obs is None:
            done = True
        info = None
        return next_obs,self.reward,done,info


    def validation_(self,action,quant,price,stock_cnt):
        profit_charged = int(self.profit(action,price,quant))
        if quant <=0:
            action =0
            quant =0
        if action==1:
            if (profit_charged > self.cash):
                action = 0
                quant = 0
        if action ==2:
            if quant > stock_cnt:
                quant = stock_cnt
                if quant == 0:
                    action = 0
        return action,quant

    def profit(self,action,cu_price,quant):
        profit = int(cu_price) * quant
        charge = 0
        profit_charged = 0
        additional_charge = 0
        tax = 0.25
        if profit <= 200000:
            charge = 0.498132
            additional_charge = 0
        elif profit <= 1000000:
            charge = 0.1672959
            additional_charge = 700
        elif profit > 1000000 and profit <=5000000:
            charge = 0.1572959
            additional_charge = 900
        elif profit > 5000000 and profit <=10000000:
            charge = 0.1472959
            additional_charge = 1000
        elif profit > 10000000 and profit <=30000000:
            charge = 0.1372959
            additional_charge = 1200
        elif profit > 30000000 and profit <=50000000:
            charge = 0.1272959
            additional_charge = 1500
        elif profit > 50000000 and profit <=200000000:
            charge = 0.0972959
            additional_charge = 0
        elif profit > 200000000 :
            charge = 0.0772959
            additional_charge = 0
        if action ==1:
            profit_charged = profit * (1 + (charge / 100)) + additional_charge
        if action == 2:
            profit_charged = profit * (1 + ((charge+tax) / 100)) + additional_charge
        return profit_charged

