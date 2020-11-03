import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras

env = gym.make('CartPole-v1')

n_inputs = 4
model = keras.models.Sequential(
    [keras.layers.Dense(5,activation='elu',input_shape=[n_inputs]),
     keras.layers.Dense(1,activation='sigmoid')]
)
obs = env.reset()
print(model(obs[np.newaxis]))

def basic_policy(obs):
    angle = obs[2]
    return 0 if angle < 0 else 1



total = []
for episode in range(500):
    episode_rewards = 0
    obs = env.reset()
    for step in range(200):
        action = basic_policy(obs)
        obs, reward, done, info = env.step(action)
        episode_rewards += reward
        if done:
            break
        env.render(mode='rgb_array')
    total.append(episode_rewards)

