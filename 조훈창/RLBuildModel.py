import os
from tensorflow import keras
import log_recorder

class Models:

    def __init__(self):
        self.input_num = 31
        self.step_num = 1
        self.logging = log_recorder.Log().dir_recorder('RL','Buildmodel')
    def build_model(self,input_num=31,step_num=1,code = 'A000020',nn=None,path = f'.\\model\\DNN\\value\\',category='value',activation='sigmoid',kernel_initializer='random_normal',trainable = True,tick='d'):
        if not os.path.exists(path):
            os.makedirs(path)
        filename = f'{code}.h5'
        if tick == 'm':
            filename = f'{code}_m.h5'
        if nn == 'DNN':
            if not os.path.isfile(path + filename):
                Input = keras.layers.Input(shape=(input_num,))
                output = keras.layers.Dense(256, activation='sigmoid',kernel_initializer=kernel_initializer, trainable=trainable)(Input)
                output = keras.layers.Dropout(0.01)(output)
                for i in range(6):
                    output = keras.layers.Dense(128 // (2**i),activation='sigmoid',kernel_initializer=kernel_initializer,trainable=trainable)(output)
                    output = keras.layers.Dropout(0.01)(output)
                    output = keras.layers.BatchNormalization()(output)
                output =keras.layers.Dense(3, activation=activation,kernel_initializer=kernel_initializer, trainable=trainable)(output)
                model = keras.Model(inputs=[Input], outputs=[output])
                model.compile(loss='mean_squared_error',optimizer=keras.optimizers.SGD(lr=0.00001))
                model.save(path + filename)
                self.logging.info(path+filename +'모델을 저장합니다.')
            else:

                if tick == 'd':
                    model = keras.models.load_model(path + f'{code}.h5')

                    self.logging.info(path + f'{code}.h5 모델을 불러옵니다.')

                if tick == 'm':
                    model = keras.models.load_model(path + f'{code}_m.h5')

                    self.logging.info(path + f'{code}_m.h5 모델을 불러옵니다.')
            return model
        if nn =='LSTM':
            if not os.path.isfile(path + filename):
                Input = keras.layers.Input(shape=(step_num,input_num))
                output = keras.layers.LSTM(256,dropout=0.1,stateful=False,return_sequences=True,  kernel_initializer='random_normal',trainable=trainable)(Input)
                output = keras.layers.BatchNormalization()(output)
                for i in range(4):
                    output = keras.layers.LSTM(128 // (2**i),dropout=0.1,stateful=False,return_sequences=True,kernel_initializer='random_normal',trainable=trainable)(output)
                    output = keras.layers.BatchNormalization()(output)
                output = keras.layers.LSTM(8, dropout=0.1,stateful=False,return_sequences=False,kernel_initializer='random_normal',trainable=trainable)(output)
                output = keras.layers.Dense(3 ,activation=activation,kernel_initializer='random_normal',trainable=trainable)(output)
                model = keras.Model(inputs=[Input],outputs=[output])
                model.compile(loss='mean_squared_error', optimizer=keras.optimizers.SGD(lr=0.01))
                model.save(path + filename)

            else:

                if tick == 'd':
                    model = keras.models.load_model(path + f'{code}.h5')

                    self.logging.info(path + f'{code}.h5 모델을 불러옵니다.')

                if tick == 'm':
                    model = keras.models.load_model(path + f'{code}_m.h5')

                    self.logging.info(path + f'{code}_m.h5 모델을 불러옵니다.')
            return model
        if nn =='CNN':
            if not os.path.isfile(path + filename):
                Input = keras.layers.Input(shape=(step_num,input_num,1))
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
                output = keras.layers.Dense(3,activation=activation)(output)
                model = keras.Model(inputs=[Input],outputs=[output])
                model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=0.01))
                model.save(path + filename)


            else:
                if tick =='d':

                    model = keras.models.load_model(path + f'{code}.h5')

                    self.logging.info(path + f'{code}.h5 모델을 불러옵니다.')

                if tick == 'm':
                    model = keras.models.load_model(path + f'{code}_m.h5')

                    self.logging.info(path + f'{code}_m.h5 모델을 불러옵니다.')
            return model

