import pandas as pd
import numpy as np
import RLEnvTrain,RLAgent
import time
from tqdm import tqdm

df = pd.read_csv('.\\DB\\CSV\\daily\\DA000020_ch.csv')

env = RLEnvTrain.RLEnv(df)
agent = RLAgent.Agent()

for k in range(100):
    obs = env.reset()

    for i in tqdm(range(1000)):

        quant = 1 # 매수매도 수량

        action = agent.policy(obs)

        price = obs[1]
        if not env.validation_(action, quant, price):
            action = 0
            quant = 0
        next_obs, reward, done, info = env.next_step(action, quant)
        agent.memorize_transition(obs,action,reward,next_obs,0.0 if done else 1.0)
        if agent.train:
            agent.experience_replay()
        if done:
            break
        obs = next_obs

    # 시각화
    

    print(np.round(env.reward,3))
    print('------------')

