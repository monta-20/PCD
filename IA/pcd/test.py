import pandas as pd
# df = pd.read_csv('../ilboursa data/BIAT_data.csv', header=None, encoding='ISO-8859-1', names=['date', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7'])

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
# for col in df.columns:
#     df[col] = df[col].apply(lambda x: int(''.join(x.split())) if (isinstance(x , str) and not any(c in x for c in '/%'))  else x)
#

#
# print("number of repeated data : ",df['date'].duplicated(keep=False).sum())
# start_date = pd.to_datetime(df['date'].iloc[-1], format='%d/%m/%Y')
# end_date = pd.to_datetime(df['date'].iloc[0], format='%d/%m/%Y')
#
# tunisia_business_days = pd.bdate_range(start_date, end_date, freq='b')
# num_business_days = len(tunisia_business_days)
#
# print("Number of business days:", num_business_days)

#***************************************
df2 = pd.read_csv('../BIAT_News.csv' )
df1 = pd.read_csv('../investing data/BIAT.csv' )
# df = df.rename(columns={'Date' : 'date','Price' : 'price','Open' : 'open','High' : 'high', 'Low' :'low','Vol.' : 'vol','Change %' : 'change'})
# df.drop(df.columns[0], axis=1 ,inplace=True)
# df = df.set_index('date')
# df.to_csv('../investing data/BIAT.csv')
# df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')

# df = df.sort_index(ascending=False)

# t = df.iloc[0:1,:]
# df = pd.concat([t, df], axis=0)

# df2['date'] = pd.to_datetime(df2['date'], format='%Y-%m-%d %H:%M:%s').dt.strftime('%Y-%m-%d')
# df2.drop(df2.columns[0], axis=1 ,inplace=True)
df1['date'] = pd.to_datetime(df1['date'])
df2['date'] = pd.to_datetime(df2['date'])
df1 = df1.set_index('date')
df2 = df2.set_index('date')
# df1['date'] = df1['date'].dt.date
# df2['date'] = df2['date'].dt.date
df2 = df2.groupby(df2.index).agg(lambda x: "***".join(list(x)))

df  = df1.merge(df2, how='outer', left_index=True, right_index=True)
df.sort_index( ascending=False , inplace=True)

# df2.to_csv('../BIAT_News.csv' , index=False)
print(df2)
print(df1)
dup = df[df.index.duplicated(keep=False)]
# print(df.groupby(df.index).apply(lambda x: pd.Series({
#     'news': '***'.join(x['news'].tolist())
# })  if pd.notna(x['news']).any() else x)
# )
print(df)
# print(df2.groupby(df2.index).agg(lambda x: list(x)))




