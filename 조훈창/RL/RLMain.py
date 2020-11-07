import os
import pandas as pd
import numpy as np
import RLEnvTrain,RLAgent
from tqdm import tqdm
from datetime import datetime
import DataPreProcessing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
pre = DataPreProcessing.DataPreProcessing()
code = 'A035720'
df = pre.change_csv(code,category='d')
df_train,df_test = pre.train_test_split(code,category='d')


step = len(df_train)
env = RLEnvTrain.RLEnv(df_train)
agent = RLAgent.Agent(gamma = 0.98,
                      eps_start = 0.8,
                      eps_end=0.01,
                      eps_decay_steps = 800,
                      eps_exponential_decay = 0.99,
                      replay_capacity = int(1e6),
                      batch_size=step-1,
                      tau = 10,
                      code = code,
                      V_nn='DNN',
                      P_nn = 'CNN',
                      method='A2C') #policy value A2C

reward_list = []
action_List = []
quant_list =[]
re_list =[]
stock_cnt_list = []
for k in range(100):
    # 학습 날짜 시간 디렉토리
    now = datetime.now()
    now = now.strftime('%Y%m%d')
    if not os.path.isdir('.\\reward\\re_'+now+'\\'):
        os.mkdir('.\\reward\\re_'+now+'\\')
    obs = env.reset()
    agent.reset()
    sub_action_list = []
    sub_quant_list=[]
    sub_re_list = []
    sub_stock_cnt = []

    df_prev = df.iloc[:119].copy()
    data = obs.reshape(1, -1)
    data = pd.DataFrame(data, columns=df.columns)
    df_prev = pd.concat([df_prev, data], ignore_index=True)
    obs = pre.add_feature(df_prev)
    #for i in tqdm(range(int(len(df_obs)*0.8))):
    for i in tqdm(range(step)):

        # 관측 데이터로 예측한 가치신경망, 정책 신경망 예측값
        value_per, policy_per = agent.predict_action_per(obs)
        
        
        action = agent.policy(value_per, policy_per)
        
        # 현재 잔고 및 주식 보유 수량 
        init_cash,stock_cnt = env.init_cash,env.total_stock
        
        # 현재 주식 가격
        cu_price = obs[1] # close
        quant = agent.decide_quant(action,value_per, policy_per,init_cash,cu_price)


        # 매도 매수 가능 한 경우 확인
        if not env.validation_(action, quant, cu_price):
            action = 0
            quant = 0



        next_obs, reward, done, info = env.next_step(action, quant)
        if done:
            break
        data = next_obs.reshape(1, -1)
        data = pd.DataFrame(data, columns=df_prev.columns)
        df_prev = pd.concat([df_prev, data], ignore_index=True)
        next_obs = pre.add_feature(df_prev)

        #
        agent.memorize_transition(obs,action,reward,next_obs,0.0 if done else 1.0,value_per, policy_per)
        if agent.train:
            agent.experience_replay()

        sub_stock_cnt.append(stock_cnt)
        sub_re_list.append(reward)
        sub_action_list.append(action)
        sub_quant_list.append(quant)
        obs = next_obs




    # experience 초기화
    #agent.reset()
    # 시각화
    # 지금 시간

    re_list.append(sub_re_list)
    df_re = pd.DataFrame(re_list)

    df_re.to_csv('.\\reward\\re_'+now+'\\re_'+str(k)+'.csv', index=False)

    stock_cnt_list.append(sub_stock_cnt)
    action_List.append(sub_action_list)
    quant_list.append(sub_quant_list)
    reward_list.append(env.reward)
    print(np.round(env.reward,4))
    print('------------')


df_reward = pd.DataFrame(reward_list)
df_action = pd.DataFrame(action_List)
df_quant = pd.DataFrame(quant_list)
df_stock_cnt = pd.DataFrame(stock_cnt_list)


df_reward.to_csv('.\\reward.csv',index=False)
df_action.to_csv('.\\action.csv',index=False)
df_quant.to_csv('.\\quant.csv',index=False)
df_stock_cnt.to_csv('.\\stock_cnt.csv',index=False)