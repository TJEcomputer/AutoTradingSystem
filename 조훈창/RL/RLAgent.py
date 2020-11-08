import numpy as np
import tensorflow as tf
from random import sample
from collections import deque
import RLBuildModel


class Agent:

    def __init__(self, gamma=0.99,
                 eps_start=0.7,
                 eps_end=0.01,
                 eps_decay_steps=800,
                 eps_exponential_decay=0.99,
                 replay_capacity=int(1e6),
                 batch_size=400,
                 tau=100,
                 code='DA000020',
                 V_nn='DNN',
                 P_nn='CNN',
                 method='A2C',
                 feature_num=31,
                 tick='d'):
        self.gamma = gamma
        self.code = code
        self.V_nn = V_nn
        self.P_nn = P_nn
        self.V_path = f'.\\model\\{V_nn}\\value\\'
        self.P_path = f'.\\model\\{P_nn}\\policy\\'
        self.method = method
        # action
        self.hold = 0
        self.buy = 1
        self.sell = 2

        self.action_list = [self.hold, self.buy, self.sell]
        # utility
        self.train = True
        self.idx = tf.range(batch_size)
        self.tau = tau
        self.input_shape = feature_num
        self.step_shape = 1
        self.feature_num = feature_num
        self.tick = tick

        # policy
        self.eps = eps_start

        # model

        # self.Q_model = RLBuildModel.Models(self.code,nn=self.nn)
        # self.Q_model_target = RLBuildModel.Models(self.code,nn=self.nn,trainable = False)
        self.Q_model, self.Q_model_target = self.create_V_model(method=method, V_nn=V_nn)
        self.P_model, self.P_model_target = self.create_P_model(method=method, P_nn=P_nn)
        self.models = RLBuildModel.Models()
        # memorize
        self.episode_reward = 0
        self.episode = self.episode_length = self.train_episodes = 0
        self.reward_history = []
        self.steps_per_episode = []
        self.total_steps = self.train_steps = 0
        self.eps_decay_steps = eps_decay_steps
        self.eps_decay = (eps_start - eps_end) / eps_decay_steps
        self.eps_exponential_decay = eps_exponential_decay
        self.replay_capacity = replay_capacity
        self.experience = deque([], maxlen=replay_capacity)

        # replay
        self.batch_size = batch_size
        self.Q_value_loss_list = []
        self.policy_loss_list = []



    def reset(self):
        self.experience = deque([], maxlen=self.replay_capacity)

    def create_V_model(self, method, V_nn):
        models = RLBuildModel.Models()
        Q_model = None
        Q_model_target = None
        if method == 'A2C' or method == 'Value':
            Q_model = models.build_model(input_num=self.feature_num,code = self.code, nn=V_nn,path = self.V_path,category='value' ,activation='linear',tick=self.tick)
            Q_model_target = models.build_model(input_num=self.feature_num,code = self.code, nn=self.V_nn,path = self.V_path,category='value', activation='linear', trainable=False,tick=self.tick)
        return Q_model, Q_model_target

    def create_P_model(self, method, P_nn):
        models = RLBuildModel.Models()
        P_model = None
        P_model_target = None
        if method == 'A2C' or method == 'policy':
            P_model = models.build_model(input_num=self.feature_num,code = self.code, nn=P_nn,path = self.P_path,category='policy', activation='sigmoid',tick=self.tick)
            P_model_target = models.build_model(input_num=self.feature_num,code = self.code, nn=P_nn,path = self.P_path,category='policy', activation='sigmoid', trainable=False,tick=self.tick)
        return P_model, P_model_target

    def predict_action_per(self, obs):
        #p_obs = v_obs = obs
        value_per = None
        policy_per = None
        if self.Q_model != None:
            obs = self.obs_reshape(obs,self.V_nn)
            value_per = self.Q_model.predict(obs).flatten()

        if self.P_model != None:
            obs = self.obs_reshape(obs, self.P_nn)
            policy_per = self.P_model.predict(obs).flatten()
        return value_per, policy_per

    def policy(self, value_per, policy_per):
        self.total_steps += 1
        exploration = np.random.rand()
        if exploration < self.eps:
            action = np.random.randint(0, len(self.action_list))

        else:
            # 예측 값 선정 행동을 결정하는 정책 신경망 값을 우선
            pred = policy_per
            if policy_per is None:
                pred = value_per
            action = np.argmax(pred)
        return action

    def update_target(self):
        self.Q_model_target.set_weights(self.Q_model.get_weights())
        self.P_model_target.set_weights(self.P_model.get_weights())
        return

    def memorize_transition(self, obs, action, reward, next_obs, not_done, value_per, policy_per):
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
            self.episode_reward, self.episode_length = 0, 0
        self.experience.append((obs, action, reward, next_obs, not_done, value_per, policy_per))

    def experience_replay(self):
        if self.batch_size > len(self.experience):
            return

        minibatch = map(np.array, zip(*sample(self.experience, self.batch_size)))
        obs, action, reward, next_obs, not_done, value_per, policy_per = minibatch

        if self.method == 'A2C':
            Q_value_loss, policy_loss = self.A2C(obs,action,reward,next_obs,not_done,value_per,policy_per)
            self.Q_value_loss_list.append(Q_value_loss)
            self.policy_loss_list.append(policy_loss)
            filename = self.code
            if self.tick=='m':
                filename = self.code +'_m.h5'
            self.Q_model.save(self.V_path + f'{filename}.h5')
            self.Q_model.save_weights(self.V_path + f'{filename}_weight.h5')
            self.P_model.save(self.P_path + f'{self.code}.h5')
            self.P_model.save_weights(self.P_path + f'{filename}_weight.h5')

        if self.method == 'ActorCritic':
            Q_value_loss, policy_loss = self.ActorCritic(obs,action,reward,next_obs,not_done,value_per,policy_per)
            self.Q_value_loss_list.append(Q_value_loss)
            self.policy_loss_list.append(policy_loss)
            filename = self.code
            if self.tick == 'm':
                filename = self.code + '_m.h5'
            self.Q_model.save(self.V_path + f'{filename}.h5')
            self.Q_model.save_weights(self.V_path + f'{filename}_weight.h5')
            self.P_model.save(self.P_path + f'{self.code}.h5')
            self.P_model.save_weights(self.P_path + f'{filename}_weight.h5')

        if self.method == 'value':
            Q_value_loss = self.Q_value(obs,action,reward,next_obs,not_done)
            self.Q_value_loss_list.append(Q_value_loss)
            filename = self.code
            if self.tick == 'm':
                filename = self.code + '_m.h5'
            self.Q_model.save(self.V_path + f'{filename}.h5')
            self.Q_model.save_weights(self.V_path + f'{filename}_weight.h5')

        if self.method == 'policy':
            policy_loss = self.Policy_gradient(obs,action,reward,policy_per)
            self.policy_loss_list.append(policy_loss)
            filename = self.code
            if self.tick == 'm':
                filename = self.code + '_m.h5'
            self.P_model.save(self.P_path + f'{filename}.h5')
            self.P_model.save_weights(self.P_path + f'{filename}_weight.h5')
        if self.total_steps % self.tau == 0:
            self.update_target()


    def Q_value(self,obs,action,reward,next_obs,not_done):
        obs = self.batch_reshape(obs,self.V_nn)
        next_obs = self.batch_reshape(next_obs,self.V_nn)
        next_Q_val = self.Q_model.predict_on_batch(next_obs)
        best_action = tf.argmax(next_Q_val, axis=1)
        best_action = tf.cast(best_action, tf.int32).numpy()
        next_q_val_target = self.Q_model_target.predict_on_batch(next_obs)
        target_Q_val = tf.gather_nd(next_q_val_target, tf.stack((self.idx, tf.cast(best_action, tf.int32)), axis=1))
        targets = reward + not_done * self.gamma * target_Q_val
        targets = targets.numpy()
        Q_val = self.Q_model.predict_on_batch(obs).numpy()  # Q_value 테이블 생성
        idx = self.idx.numpy()
        Q_val[idx, action] = targets[idx]
        loss = self.Q_model.train_on_batch(obs, Q_val)
        return loss

    def Policy_gradient(self,obs,action,reward,policy_per):
        obs = self.batch_reshape(obs, self.P_nn)
        policy_per[self.idx.numpy(),action] = self.sigmoid(reward)
        loss = self.Q_model.train_on_batch(obs, policy_per)
        return loss

    def ActorCritic(self,obs,action,reward,next_obs,not_done,value_per,policy_per):
        Q_value_loss = self.Q_value(obs,action,reward,next_obs,not_done)
        obs = self.batch_reshape(obs, self.P_nn)
        policy_per[self.idx.numpy(),action] = self.sigmoid(value_per[self.idx.numpy(),action])
        policy_loss = self.P_model.train_on_batch(obs,policy_per)
        return Q_value_loss, policy_loss

    def A2C(self,obs,action,reward,next_obs,not_done,value_per,policy_per):
        Q_value_loss = self.Q_value(obs, action, reward, next_obs,not_done)
        obs = self.batch_reshape(obs, self.P_nn)
        adv = value_per[self.idx.numpy(), action] - value_per.mean(axis=1)
        policy_per[self.idx.numpy(), action] = self.sigmoid(adv)
        #print(policy_per)
        policy_loss = self.P_model.train_on_batch(obs, policy_per)
        return Q_value_loss, policy_loss


    def decide_quant(self, action, value_per, policy_per,init_cash,cu_price):
        # 매도 매수 주문 수량의 최대 크기 최소 크기를 정해 놓는 방법
        quant = init_cash // cu_price
        if policy_per is not None:
            quant = int(quant * policy_per[action])
        elif value_per is not None:
            quant = int(quant * self.sigmoid(value_per[action]))
        return quant

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def obs_reshape(self,x,nn):
        if nn == 'DNN':
            x = x.reshape(-1,self.input_shape)
        if nn == 'LSTM':
            x = x.reshape(-1,self.step_shape,self.input_shape)
        if nn == 'CNN':
            x = x.reshape(-1,self.step_shape,self.input_shape,1)
        return x

    def batch_reshape(self,x,nn):
        if nn == 'LSTM':
            x = x.reshape(x.shape[0],self.step_shape,x.shape[1])
        if nn == 'CNN':
            x = x.reshape(x.shape[0],self.step_shape,x.shape[1],1)
        return x
