import os
import numpy as np
from sklearn.preprocessing import Normalizer
from tensorflow import keras

class Models:
    def __init__(self,code,step_num=1,input_num = 30,nn='DNN',activation='sigmoid',kernel_initializer='random_normal',trainable = True):
        self.code = code
        self.nn = nn
        self.input_num = input_num
        self.step_num = step_num
        self.model = self.build_model(trainable,activation,kernel_initializer)
        self.scaler = Normalizer()


    def build_model(self,trainable,activation,kernel_initializer):
        path = f'.\\model\\{self.nn}\\{self.code}.h5'
        if self.nn == 'DNN':
            if not os.path.isfile(path):
                Input = keras.layers.Input(shape=(self.input_num,))
                output = keras.layers.Dense(256, activation='sigmoid',kernel_initializer=kernel_initializer, trainable=trainable)(Input)
                for i in range(6):
                    output = keras.layers.Dense(128 // (2**i),activation='sigmoid',kernel_initializer=kernel_initializer,trainable=trainable)(output)
                    output = keras.layers.Dropout(0.01)(output)
                    output = keras.layers.BatchNormalization()(output)
                output =keras.layers.Dense(3, activation=activation,kernel_initializer=kernel_initializer, trainable=trainable)(output)
                model = keras.Model(inputs=[Input], outputs=[output])
                model.compile(loss='mean_squared_error',optimizer=keras.optimizers.SGD(lr=0.00001))
                model.save(path)
            else:
                model = keras.models.load_model(path)
            return model
        if self.nn =='LSTM':
            if not os.path.isfile(path):
                Input = keras.layers.Input(shape=(self.step_num,self.input_num))
                output = keras.layers.LSTM(256,dropout=0.1,stateful=False,return_sequences=True,  kernel_initializer='random_normal',trainable=trainable)(Input)
                output = keras.layers.BatchNormalization()(output)
                for i in range(4):
                    output = keras.layers.LSTM(128 // (2**i),dropout=0.1,stateful=False,return_sequences=True,kernel_initializer='random_normal',trainable=trainable)(output)
                    output = keras.layers.BatchNormalization()(output)
                output = keras.layers.LSTM(8, dropout=0.1,stateful=False,return_sequences=False,kernel_initializer='random_normal',trainable=trainable)(output)
                output = keras.layers.Dense(3 ,activation='linear',kernel_initializer='random_normal',trainable=trainable)(output)
                model = keras.Model(inputs=[Input],outputs=[output])
                model.compile(loss='mean_squared_error', optimizer=keras.optimizers.SGD(lr=0.01))
                model.save(path)
            else:
                model = keras.models.load_model(path)
            return model
        if self.nn =='CNN':
            if not os.path.isfile(path):
                Input = keras.layers.Input(shape=(self.step_num,self.input_num,1))
                output = keras.layers.Conv2D(256,kernel_size=(1,5),padding='same',activation='sigmoid',kernel_initializer='random_normal')(Input)
                output = keras.layers.BatchNormalization()(output)
                output = keras.layers.MaxPooling2D(pool_size=(1,2))(output)
                output = keras.layers.Dropout(0.5)(output)
                for i in range(3):
                    output = keras.layers.Conv2D(128 // (2**i),kernel_size=(1,5),padding='same',activation='sigmoid',kernel_initializer='random_normal')(output)
                    output = keras.layers.BatchNormalization()(output)
                    output = keras.layers.MaxPooling2D(pool_size=(1, 2))(output)
                    output = keras.layers.Dropout(0.5)(output)
                output = keras.layers.Flatten()(output)
                output = keras.layers.Dense(3,activation='sigmoid')(output)
                model = keras.Model(inputs=[Input],outputs=[output])
                model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=0.01))
                model.save(path)
            else:
                model = keras.models.load_model(path)
            return model

    def predict(self,x):
        """

        :param x:
        :return:
        예측값 2차원 배열
        """
        if self.nn == 'DNN':
            x = np.reshape(x, (1, self.input_num))
            pred = self.model.predict(x)
        if self.nn == 'LSTM':
            x = np.reshape(x, (1, 1,self.input_num))
            pred = self.model.predict(x)
            pred = pred.reshape(-1,3)
        if self.nn == 'CNN':

            x = np.reshape(x, (1, self.input_num))
            x = np.reshape(x, (1, 1, self.input_num,1))
            x.astype(float)

            pred = self.model.predict(x)
            pred = pred.reshape(1, 3)
        return pred

    def fit(self,x,y):
        if self.nn == 'DNN':
            x = np.array(x).reshape(-1, self.input_num)
        if self.nn == 'LSTM':
            x = np.array(x).reshape(-1, self.input_num)
            x = np.reshape(x,(x.shape[0],1,x.shape[1]))
        if self.nn == 'CNN':
            x = np.array(x).reshape(-1, self.input_num)

            x = np.reshape(x, (x.shape[0], 1, x.shape[1],1))
        return self.model.fit(x,y)

    def predict_on_batch(self,x):
        if self.nn == 'DNN':
            x = np.array(x).reshape(-1, self.input_num)
            x = x.astype(float)
            pred = self.model.predict_on_batch(x)
            pred = pred.numpy()
        if self.nn == 'LSTM':
            x = np.array(x).reshape(-1, self.input_num)
            x = x.astype(float)
            x = x.reshape(x.shape[0],1,x.shape[1])
            pred = self.model.predict_on_batch(x)
            pred = pred.numpy().reshape(pred.shape[0],3)
        if self.nn == 'CNN':
            x = np.array(x).reshape(-1, self.input_num)
            x = x.astype(float)
            x = x.reshape(x.shape[0], 1, x.shape[1],1)

            pred = self.model.predict_on_batch(x)
            pred = pred.numpy().reshape(pred.shape[0],1, 3)
            pred = pred.reshape(pred.shape[0], 3)
        return pred

    def train_on_batch(self,x,y):
        if self.nn == 'DNN':
            x = np.array(x).reshape(-1, self.input_num)
            x = x.astype(float)
        if self.nn == 'LSTM':
            x = np.array(x).reshape(-1, self.input_num)
            x = x.reshape(-1, 1, x.shape[1])
            x = x.astype(float)
        if self.nn == 'CNN':
            x = np.array(x).reshape(-1, self.input_num)
            x = x.reshape(-1, 1, x.shape[1],1)
            x = x.astype(float)
        return self.model.train_on_batch(x,y)

    def copy(self):
        return keras.models.clone_model(self.model)

    def save(self,path):
        return self.model.save(path)

    def save_weights(self,path):
        return self.model.save_weights(path)

    def load_weights(self,path):
        return self.model.load_weights(path)

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self,weights):
        return self.model.set_weights(weights)