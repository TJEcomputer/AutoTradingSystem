import os
import numpy as np
import tensorflow as tf
from random import sample
from tensorflow import keras
from collections import deque
from sklearn.preprocessing import MinMaxScaler
class Agent:
    if not os.path.isfile('.\\DA000020.h5'):
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(9, input_shape=(9,), activation='relu'))
        model.add(keras.layers.Dense(9, activation='relu'))
        model.add(keras.layers.Dense(3))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.save('.\\DA000020.h5')
        model.save_weights('.\\DA000020_weight.h5')

        #신경망 모델 업데이트

    def __init__(self,gamma = 0.99,
                 eps_start = 0.5,
                 eps_end=0.01,
                 eps_decay_steps = 250,
                 eps_exponential_decay = 0.99,
                 replay_capacity = int(1e6),
                 batch_size=100,
                 tau = 20):
        self.gamma = gamma

        # action
        self.hold = 0
        self.buy = 1
        self.sell = 2

        self.action_list = [self.hold,self.buy,self.sell]

        # policy
        self.eps = eps_start

        # model

        self.Q_model = keras.models.load_model('.\\DA000020.h5')
        self.Q_model.load_weights('.\\DA000020_weight.h5')

        self.Q_model_target = keras.models.clone_model(self.Q_model)


        # memorize
        self.episode_reward =0
        self.episode = self.episode_length =self.train_episodes=0
        self.reward_history = []
        self.steps_per_episode = []
        self.total_steps = self.train_steps = 0
        self.eps_decay_steps = eps_decay_steps
        self.eps_decay = (eps_start - eps_end) / eps_decay_steps
        self.eps_exponential_decay = eps_exponential_decay
        self.experience = deque([],maxlen = replay_capacity)

        #replay
        self.batch_size = batch_size
        self.loss_list = []


        # utility
        self.train = True
        self.idx = tf.range(batch_size)
        self.tau = tau
        self.scaler = MinMaxScaler()
    def policy(self,obs):
        self.total_steps +=1
        expolitation = np.random.rand()
        action = 0
        if expolitation < self.eps:
            action = np.random.randint(0,len(self.action_list))
        else:
            obs = np.array(obs).reshape(-1,1)
            obs = self.scaler.fit_transform(obs)
            obs = np.reshape(obs,(1,9))
            pred = self.Q_model.predict(obs)
            action = np.argmax(pred)

        return action
#wdwd
    def do(self,action):

        reward = 0
        if action == 0:
            reward = -3
            print('관망')
        if action ==1:
            reward = 5
            print('매수')
        if action == 2:
            reward = -1
            print('매도')
        return reward

    def build_model(self):
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(9,input_shape=(1,),activation='relu'))
        model.add(keras.layers.Dense(9,activation='relu'))
        model.add(keras.layers.Dense(3))
        model.compile(loss='mean_squared_error',optimizer='adam')
        model.save('.\\DA000020.h5')
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
        obs = self.scaler.fit_transform(obs)
        obs = np.array(obs).reshape(-1,9)
        next_obs = self.scaler.fit_transform(next_obs)
        next_obs = np.array(next_obs).reshape(-1,9)
        next_Q_val = self.Q_model.predict_on_batch(next_obs)
        best_action = tf.argmax(next_Q_val,axis=1)
        next_q_val_target = self.Q_model_target.predict_on_batch(next_obs)

        next_q_val_target = next_q_val_target.numpy()
        best_action = tf.cast(best_action, tf.int32).numpy()


        target_Q_val = tf.gather_nd(next_q_val_target,tf.stack((self.idx,tf.cast(best_action,tf.int32)),axis=1))
        targets = reward + not_done *self.gamma * target_Q_val


        Q_val = self.Q_model.predict_on_batch(obs)
        Q_val = Q_val.numpy()
        targets = targets.numpy()
        for i,j in zip(self.idx.numpy(),action):
            Q_val[i,j] = targets[i]
        #loss = self.Q_model.fit(obs,Q_val,epochs=2,batch_size=self.batch_size,validation_split=0.1,callbacks=[keras.callbacks.ModelCheckpoint('.\\DA000020.h5',save_best_only=True),keras.callbacks.EarlyStopping(patience=20,monitor='val_loss')])
        loss = self.Q_model.train_on_batch(obs,Q_val)
        self.Q_model.save_weights('.\\DA000020_weight.h5')
        self.Q_model.load_weights('.\\DA000020_weight.h5')
        self.loss_list.append(loss)
        if self.total_steps% self.tau ==0:
            self.update_target()





