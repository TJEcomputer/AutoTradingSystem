import numpy as np
import tensorflow as tf
from tensorflow.python.client import device_lib
from tensorflow import keras
import pandas as pd
df = pd.read_csv('.\\DB\\CSV\\daily\\DA000020_ch.csv')


#data = df.iloc[0].values.reshape(1,-1)
def add_feature(df):
    df_ = df.copy()
    windows = [5,10,20,60,120]
    for window in windows:
        df_[f'close_ma{window}'] = df_['close'].rolling(window).mean()
        df_[f'volume_ma{window}'] = df_['volume'].rolling(window).mean()
        df_[f'close_ma_latio{window}'] = (df_['close'] - df_[f'close_ma{window}']) / df_[f'close_ma{window}']
        df_[f'volume_ma_latio{window}'] = (df_['volume'] - df_[f'volume_ma{window}']) / df_[f'volume_ma{window}']
    data = df_.iloc[-1]

    return data.values


def get_obs(df_prev,obs):

    return obs, df_prev