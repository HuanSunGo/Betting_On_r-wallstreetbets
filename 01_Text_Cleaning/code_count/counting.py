from utils.functions import *
import pickle
import numpy as np

df = pd.read_pickle(data_path + "df_yearmonthbody.pkl")

# Extract the ticker name from the full comment, had it shown in the ticker.csvx
df["symbol"] = [uppers_fun(v) for v in df.body] # ran for 7 hours or so.
df['tickers'] = df.symbol.apply(joiner)
df['tickers'].replace('', np.nan, inplace=True)

# Drop the comments that hadn't mention any ticker at all.
df.dropna(subset=['tickers'], inplace=True) # 1,571,183 rows (originally 13,466,012)
df["symbol"] = df.symbol.apply(set).apply(list)
df.drop(columns=['tickers'], inplace=True)
df["bodylen"]=df.body.apply(tokenizer).apply(len)
pickle.dump(df, open(data_path + "df_wsb.pkl", "wb"))

# aggregate by month
df = pd.read_pickle(data_path + "df_wsb.pkl")
df = df.groupby(['year','month']).agg({'symbol': 'sum'}).reset_index()
df['date'] = pd.to_datetime(df[['year', 'month']].assign(DAY=1))

dff = df.symbol.apply(counter)
dff["date"] = df.date
df = dff
del dff
cols = list(df.columns)
cols = [cols[-1]] + cols[:-1]
df = df[cols]
df = df.fillna(0)
df.columns = df.columns.get_level_values(0) # 101 by 3211
df = pd.melt(df,id_vars=['date'],var_name='ticker', value_name='count') # 324210 x 3
df['year'], df['month'] = df['date'].dt.year, df['date'].dt.month
df = df[["date","year","month","ticker","count"]]
pickle.dump(df, open(data_path + "df.pkl", "wb"))

































































