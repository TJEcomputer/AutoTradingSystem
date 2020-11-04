import os
import numpy as np
import tensorflow as tf
from random import sample
from tensorflow import keras
from collections import deque
import RLBuildModel
class Agent:


    def __init__(self,gamma = 0.99,
                 eps_start = 0.7,
                 eps_end=0.01,
                 eps_decay_steps = 800,
                 eps_exponential_decay = 0.99,
                 replay_capacity = int(1e6),
                 batch_size=400,
                 tau = 20,
                 code = 'DA000020',
                 nn = 'LSTM'):
        self.gamma = gamma
        self.code = code
        self.nn = nn
        self.path = f'.\\model\\{nn}\\{code}.h5'
        # action
        self.hold = 0
        self.buy = 1
        self.sell = 2

        self.action_list = [self.hold,self.buy,self.sell]

        # policy
        self.eps = eps_start

        # model

        self.Q_model = RLBuildModel.Models(self.code,nn=self.nn)

        self.Q_model_target = RLBuildModel.Models(self.code,nn=self.nn,trainable = False)



        # memorize
        self.episode_reward =0
        self.episode = self.episode_length =self.train_episodes=0
        self.reward_history = []
        self.steps_per_episode = []
        self.total_steps = self.train_steps = 0
        self.eps_decay_steps = eps_decay_steps
        self.eps_decay = (eps_start - eps_end) / eps_decay_steps
        self.eps_exponential_decay = eps_exponential_decay
        self.replay_capacity = replay_capacity
        self.experience = deque([],maxlen = replay_capacity)

        #replay
        self.batch_size = batch_size
        self.loss_list = []


        # utility
        self.train = True
        self.idx = tf.range(batch_size)
        self.tau = tau

    def reset(self):
        self.experience = deque([],maxlen = self.replay_capacity)

    def policy(self,obs):
        self.total_steps +=1
        expolitation = np.random.rand()
        if expolitation < self.eps:
            action = np.random.randint(0,len(self.action_list))
            action_per = expolitation
        else:

            pred = self.Q_model.predict(obs)
            pred = pred.reshape(3,)
            action = np.argmax(pred)
            action_per = pred[action] # -/ 1>0
        return action, action_per

    def update_target(self):
        return self.Q_model_target.set_weights(self.Q_model.get_weights())

    def memorize_transition(self,obs,action,reward,next_obs,not_done):
        if not_done:
            self.episode_reward += reward
            self.episode_length += 1
        else:
            if self.train:
                if self.episode < self.eps_decay_steps:
                    self.eps -= self.eps_decay
                else:
                    self.eps *= self.eps_exponential_decay
            self.episode += 1
            self.reward_history.append(self.episode_reward)
            self.steps_per_episode.append(self.episode_length)
            self.episode_reward, self.episode_length = 0,0
        self.experience.append((obs,action,reward,next_obs,not_done))

    def experience_replay(self):
        if self.batch_size > len(self.experience):
            return
        minibatch = map(np.array,zip(*sample(self.experience,self.batch_size)))
        obs,action,reward,next_obs,not_done = minibatch
        next_Q_val = self.Q_model.predict_on_batch(next_obs)
        best_action = tf.argmax(next_Q_val,axis=1)
        best_action = tf.cast(best_action, tf.int32).numpy()
        next_q_val_target = self.Q_model_target.predict_on_batch(next_obs)


        target_Q_val = tf.gather_nd(next_q_val_target,tf.stack((self.idx,tf.cast(best_action,tf.int32)),axis=1))
        targets = reward + not_done *self.gamma * target_Q_val
        targets = targets.numpy()
        Q_val = self.Q_model.predict_on_batch(obs) # Q_value 테이블 생성
       # print(obs)
       # print(Q_val, Q_val.shape,type(Q_val))



        idx = self.idx.numpy()
        Q_val[idx,action] = targets[idx]
        #print(Q_val,Q_val.shape,'Q_val')

        loss = self.Q_model.train_on_batch(obs,Q_val)
        self.Q_model.save(self.path)
        self.Q_model.save_weights(f'.\\model\\{self.nn}\\{self.code}_weight.h5')
        self.loss_list.append(loss)
        if self.total_steps% self.tau ==0:
            self.update_target()



    def decide_quant(self,action,action_per,cash,stock_cnt,cu_price):
        quant = 0
        if action == 1:
            quant = cash//int(cu_price) * action_per
        if action == 2:
            quant = int(stock_cnt * action_per)
        if action ==0:
            quant = 0
        return quant


