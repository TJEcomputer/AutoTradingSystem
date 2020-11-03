import pandas as pd
import numpy as np
import test
df = pd.read_csv('.\\DB\\CSV\\daily\\DA000020_ch.csv')
# 단계 시작
df_test = df.iloc[119:int(len(df)*0.6),:].copy()
prev_test = df.iloc[:119]
df_test = df_test.reset_index()
df_test = df_test.drop(['index'],axis =1)

data = df_test.iloc[0].values.reshape(1,-1)
data = pd.DataFrame(data,columns=df_test.columns)

prev_test = pd.concat([prev_test,data],ignore_index=True)
tt = test.add_feature(prev_test)

print(prev_test.tail(10))
print(prev_test.iloc[-1].values)
