from utils.functions import *
import numpy as np

## cleaning crsp
crsp = pd.read_csv(data_path + 'crsp.csv')
crsp['date'] = crsp['date'].astype(str)
crsp['date'] = pd.to_datetime(crsp['date'])
crsp['date'] = crsp.date.apply(lambda dt: dt.replace(day=1))
crsp['lag_vwretd'] = (crsp.groupby(["ticker"]))['vwretd'].shift(1) # my poor math! 
crsp = crsp.dropna(subset=['lag_vwretd']) # value weighted return 
crsp = crsp[crsp['ticker'].isin(ticker)] # keep only tickers in CRSP/NASDAQ/AMEX dictionary
crsp = crsp.sort_values(["ticker","date"], ascending = (True, True))
crsp = crsp[(crsp.date >= "2012-04-01") & (crsp.date <= "2020-08-01")]

## merging crsp with reddit count data_count
df = pd.read_pickle(data_path + 'df.pkl')
df = crsp.merge(df, on=['date','ticker'], how='left').reset_index(drop=True)
# df = pd.merge(df, crsp, on=['date','ticker']).reset_index(drop=True)
df['year'], df['month'] = df['date'].dt.year, df['date'].dt.month
df['count'] = df['count'].fillna(0)
df.to_csv(data_path + "df_merge.csv", sep=',', index=False)

## top x percentiles
df_sum = pd.DataFrame((df.groupby(["ticker"]))['count'].sum())
p1 = percentile(df_sum['count'],99)
p5 = percentile(df_sum['count'],95)
df_sum['top1'] = np.where(df_sum['count']>= p1, 1, 0)
df_sum['top5'] = np.where(df_sum['count']>= p5, 1, 0)
df_sum['notzero'] = np.where(df_sum['count']>= 9, 1, 0)
df_sum.to_csv(data_path + "df_sum.csv", sep=',', index=False)

df = pd.merge(df, df_sum[['top1','top5','notzero']], on=['ticker']).reset_index(drop=True)
df.to_csv(data_path + "df_merge2.csv", sep=',', index=False)

# df_sumyear = pd.DataFrame((df.groupby(["ticker","year"]))['count'].sum())
# df_sumyear.to_csv(data_path + "df_sumyear.csv", sep=',')


























