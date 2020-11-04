import os
import test
import pandas as pd
import numpy as np
import RLEnvTrain,RLAgent
from tqdm import tqdm
from datetime import datetime
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

code = 'DA000040'
df = pd.read_csv(f'.\\DB\\CSV\\daily\\{code}_ch.csv')
df['profit'] = 0
df['volume'].replace(0,method='ffill',inplace=True)

df_obs = df.iloc[119:int(len(df)*0.8),:].copy()
df_obs = df_obs.reset_index()
df_obs = df_obs.drop(['index'],axis =1)



env = RLEnvTrain.RLEnv(df_obs)
agent = RLAgent.Agent(gamma = 0.98,
                 eps_start = 0.8,
                 eps_end=0.01,
                 eps_decay_steps = 800,
                 eps_exponential_decay = 0.99,
                 replay_capacity = int(1e6),
                 batch_size=4000,
                 tau = 50,
                 code = code,
                 nn = 'CNN')
reward_list = []
action_List = []
quant_list =[]
re_list =[]
for k in range(100):
    # 학습 날짜 시간 디렉토리
    now = datetime.now()
    now = now.strftime('%Y%m%d')
    if not os.path.isdir('.\\reward\\re_'+now+'\\'):
        os.mkdir('.\\reward\\re_'+now+'\\')
    obs = env.reset()

    sub_action_list = []
    sub_quant_list=[]
    sub_re_list = []

    df_prev = df.iloc[:119].copy()
    data = obs.reshape(1, -1)
    data = pd.DataFrame(data, columns=df.columns)
    df_prev = pd.concat([df_prev, data], ignore_index=True)
    obs = test.add_feature(df_prev)
    for i in tqdm(range(int(len(df_obs)*0.8))):
        action,action_per = agent.policy(obs)
        cash,stock_cnt = env.cash,env.total_stock
        price = obs[1] # close
        quant = agent.decide_quant(action,action_per,cash,stock_cnt,price)



        if not env.validation_(action, quant, price):
            action = 0
            quant = 0
        sub_action_list.append(action)
        sub_quant_list.append(quant)
        next_obs, reward, done, info = env.next_step(action, quant)
        data = next_obs.reshape(1, -1)
        data = pd.DataFrame(data, columns=df_prev.columns)
        df_prev = pd.concat([df_prev, data], ignore_index=True)
        next_obs = test.add_feature(df_prev)
        sub_re_list.append(reward)

        agent.memorize_transition(obs,action,reward,next_obs,0.0 if done else 1.0)
        if agent.train:
            agent.experience_replay()
        if done:
            break
        obs = next_obs
    # experience 초기화
    #agent.reset()
    # 시각화
    # 지금 시간

    re_list.append(sub_re_list)
    df_re = pd.DataFrame(re_list)

    df_re.to_csv('.\\reward\\re_'+now+'\\re_'+str(k)+'.csv', index=False)

    action_List.append(sub_action_list)
    quant_list.append(sub_quant_list)
    reward_list.append(env.reward)
    print(np.round(env.reward,4))
    print('------------')


df_reward = pd.DataFrame(reward_list)
df_action = pd.DataFrame(action_List)
df_quant = pd.DataFrame(quant_list)

df_reward.to_csv('.\\reward.csv',index=False)
df_action.to_csv('.\\action.csv',index=False)
df_quant.to_csv('.\\quant.csv',index=False)
