import pandas as pd

df = pd.read_csv('.\\DB\\CSV\\daily\\DA000020.csv')
df.sort_values(by='date',inplace=True)
df_stock = df[['date','open','close','high','low','volume']].copy()
df_stock['prev_close'] = df_stock['close'].shift(1)
df_stock['prev_diff'] = df_stock['close'] - df_stock['prev_close']
df_stock['prev_volume'] = df_stock['volume'].shift(1)
df_stock['volume_diff'] = df_stock['volume'] - df_stock['prev_volume']
df_stock.dropna(inplace=True)
df_stock_ch = df_stock[['prev_close','close','prev_diff','open','high','low','volume','prev_volume','volume_diff']].copy()
df_stock_ch.reset_index(inplace=True)
df_stock_ch.drop(['index'],axis=1,inplace=True)
df_stock_ch.to_csv('.\\DB\\CSV\\daily\\DA000020_ch.csv',index=False)
print(df_stock_ch.head(5))