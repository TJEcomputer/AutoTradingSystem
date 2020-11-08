import os
import pandas as pd
import numpy as np
import time
import RLEnvTrain,RLAgent
from tqdm import tqdm
from datetime import datetime
import DataPreProcessing
import log_recorder
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'




class TestEnv:
    def __init__(self):
        self.logging = log_recorder.Log().dir_recorder('RL','test')
        self.prev = None
        self.pre = DataPreProcessing.DataPreProcessing()

    def set(self,df):
        self.prev = df

    def test(self,code,day=252,year=1,test_year=1,full_year=5,test_month=1,full_month=5,category='d',eps=0.05):
        now = datetime.now()
        now = now.strftime('%Y%m%d')

        path = '.\\DB\\CSV\\daily\\'
        if category =='m':
            path = '.\\DB\\CSV\\min\\'
            day = 20
            day = day * 390
            test_year= test_month
            full_year = full_month
            now = now + '_m'
        filename = code + '_ch.csv'
        chartfile = code +'.csv'
        if not os.path.exists(path + filename):
            self.logging.info('파일 생성')
            self.pre.change_csv(code,category=category)
        if not os.path.exists('.\\Test\\re_' + now):
            os.makedirs('.\\Test\\re_' + now)

        self.logging.info('테스트 데이터 분리')
        df_chart = pd.read_csv(path +chartfile)
        if category=='m':

            df_chart = self.pre.min_preprocessing(df_chart)
        df_chart_split = df_chart.iloc[-1*day*year*test_year:]
        df_chart_split.to_csv('.\\Test\\re_' + now + '\\chart.csv', index=False)
        df_chart = self.pre.change_feature(df_chart)
        df_test = df_chart.iloc[-1 * day * year * test_year:]
        df_prev = df_chart.iloc[-1*day*year*test_year-120:-1*day*year*test_year]
        step = len(df_test)
        env = RLEnvTrain.RLEnv(df_test)
        agent = RLAgent.Agent(gamma=0.98,
                              eps_start=eps,
                              eps_end=0.01,
                              eps_decay_steps=800,
                              eps_exponential_decay=0.99,
                              replay_capacity=int(1e6),
                              batch_size=step - 1,
                              tau=10,
                              code=code,
                              V_nn='DNN',
                              P_nn='CNN',
                              method='A2C')  # policy value A2C

        reward_list = []
        action_List = []
        quant_list = []
        stock_cnt_list = []
        obs_list = []

        obs = env.reset()
        agent.reset()

        if not os.path.isdir('.\\Test\\re_' + now + '\\'):
            os.makedirs('.\\Test\\re_' + now + '\\')

        df_prev = df_prev
        data = obs.reshape(1, -1)
        data = pd.DataFrame(data, columns=df_chart.columns)
        df_prev = pd.concat([df_prev, data], ignore_index=True)
        obs = self.pre.add_feature(df_prev)
        step = len(df_test)
        self.logging.info('테스트 시작')

        for i in tqdm(range(step)):
            # 관측 데이터로 예측한 가치신경망, 정책 신경망 예측값
            value_per, policy_per = agent.predict_action_per(obs)

            action = agent.policy(value_per, policy_per)

            # 현재 잔고 및 주식 보유 수량
            init_cash, stock_cnt = env.init_cash, env.total_stock

            # 현재 주식 가격
            cu_price = obs[1]  # close
            quant = agent.decide_quant(action, value_per, policy_per, init_cash, cu_price)

            # 매도 매수 가능 한 경우 확인

            action,quant =  env.validation_(action, quant, cu_price,stock_cnt)

            next_obs, reward, done, info = env.next_step(action, quant)
            if next_obs is not None:
                data = next_obs.reshape(1, -1)
                data = pd.DataFrame(data, columns=df_prev.columns)
                df_prev = pd.concat([df_prev, data], ignore_index=True)
                next_obs = self.pre.add_feature(df_prev)

            reward_list.append(reward)
            action_List.append(action)
            quant_list.append(quant)
            stock_cnt_list.append(stock_cnt)
            obs_list.append(obs)


            obs = next_obs

        df_reward = pd.DataFrame(reward_list)
        df_action = pd.DataFrame(action_List)
        df_quant = pd.DataFrame(quant_list)
        df_stock_cnt = pd.DataFrame(stock_cnt_list)
        df_obs = pd.DataFrame(obs_list)



        df_reward.to_csv('.\\Test\\re_' + now + '\\reward.csv', index=False)
        df_action.to_csv('.\\Test\\re_' + now + '\\action.csv', index=False)
        df_quant.to_csv('.\\Test\\re_' + now + '\\quant.csv', index=False)
        df_stock_cnt.to_csv('.\\Test\\re_' + now + '\\stock_cnt.csv', index=False)
        df_obs.to_csv('.\\Test\\re_' + now + '\\obs.csv', index=False)
        self.logging.info(f'reward : {reward} | 테스트 끝')

if __name__ == '__main__':
    T = TestEnv()
    T.test('A035720',category='m')



