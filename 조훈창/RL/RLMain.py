import os
import pandas as pd
import numpy as np
import RLEnvTrain,RLAgent
from tqdm import tqdm
from datetime import datetime
import RLtest
import log_recorder
import DataPreProcessing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
pre = DataPreProcessing.DataPreProcessing()
logging = log_recorder.Log().dir_recorder('RL','Main')
Test = RLtest.TestEnv()
code = 'A035720'
print(f'{code} 학습을 시작합니다.')

df = pre.change_csv(code,category='d')
print(f'데이터셉 분리 학습을 시작합니다.')
df_train,df_test,df_prev = pre.train_test_split(code,category='d')

step = len(df_train)
print(f'한 학습당 step : {step}')
#step = 10
print(f'학습 환경 구성')
env = RLEnvTrain.RLEnv(df_train)
print(f'학습 에이전트 구성')
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
                      method='A2C',
                      tick='d') #policy value A2C

reward_list = []
action_List = []
quant_list =[]
re_list =[]
stock_cnt_list = []
print('학습 시작')
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

    df_prev = pre.train_test_split(code,category='d',sel='prev')
    data = obs.reshape(1, -1)
    data = pd.DataFrame(data, columns=df.columns)
    df_prev = pd.concat([df_prev, data], ignore_index=True)
    obs = pre.add_feature(df_prev)
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


        agent.memorize_transition(obs,action,reward,next_obs,0.0 if done else 1.0,value_per, policy_per)
        #if agent.train:
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


    stock_cnt_list.append(sub_stock_cnt)
    action_List.append(sub_action_list)
    quant_list.append(sub_quant_list)
    reward_list.append(env.reward)
    print(np.round(env.reward,4))
    print(f'다음 데이터가 없습니다. {k}번째 에피소드가 끝났습니다.')
    print('------------')


df_reward = pd.DataFrame(reward_list)
df_action = pd.DataFrame(action_List)
df_quant = pd.DataFrame(quant_list)
df_stock_cnt = pd.DataFrame(stock_cnt_list)
df_re = pd.DataFrame(re_list)

df_re.to_csv('.\\reward\\re_'+now+'\\re_'+str(now)+'.csv', index=False)
df_reward.to_csv('.\\reward\\re_'+now+'\\reward_'+str(now)+'.csv',index=False)
df_action.to_csv('.\\reward\\re_'+now+'\\action_'+str(now)+'.csv',index=False)
df_quant.to_csv('.\\reward\\re_'+now+'\\quant_'+str(now)+'.csv',index=False)
df_stock_cnt.to_csv('.\\reward\\re_'+now+'\\stock_cnt_'+str(now)+'.csv',index=False)
print('학습 끝')
# 테스트 시작

print('테스트 시작')
Test.test(code)
print('테스트 끝')

