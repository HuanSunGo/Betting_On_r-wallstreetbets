from utils.functions import *
import pandas as pd
import pickle

data_path='C:/Users/hs324/OneDrive/Desktop/Class_Files/GR5067_NLP/03_Group_Project/'
df = pd.read_csv(data_path + 'wallstreetbets_comments.csv')

#Read the data in and drop the irrevalent columns to reduce the size of data.
df.drop(columns=['author_created_utc','author','author_created_utc','author_fullname','controversiality','created_utc',
                'gilded','id','link_id','nest_level', 'parent_id','reply_delay','retrieved_on','subreddit','subreddit_id',
                'created_hour','created_day','timestamp','score'], inplace=True)
set(df['created_year'])
df = df[["created_year","created_month","body"]]
df.rename(columns={'created_year': 'year', 'created_month': 'month'}, inplace=True)

#Drop the rows with comments being null, and drop the apparent wrong record of year.
df = df[df['year']!=1970]
df.dropna(subset = ['body'], inplace = True) #13466012

df["body"] = df.body.apply(clean_text)

pickle.dump(df, open(data_path + "df_yearmonthbody.pkl", "wb"))

"""
Exploratory data viz code.
1.Load the merge_df, add the accumulated return for each stock from 2012-2020
"""
df_merge=pd.read_csv(data_path+'df_merge.csv')
df_plot=pd.DataFrame()
a=pd.DataFrame(df_merge['ticker'].value_counts()).reset_index()
a.rename(columns={'index':'ticker','ticker':'mention_counts'},inplace=True)

# Calculate the aggregate return
return_data = []

for ticker in df_merge['ticker'].unique():
    ticker_df = df_merge[df_merge['ticker']==ticker]
    prices = list(ticker_df['price'])
    start_price, end_price = prices[0], prices[-1]
    pct_return = (end_price - start_price) / start_price
    return_data.append({
        "ticker" : ticker,
        "return" : pct_return})

return_df = pd.DataFrame(return_data).round(2)
return_df.to_csv('cum_return.csv')

# Add one column of the accumulated mention times
# df_merge['count']=df_merge['count'].astype('int')
# return_df = pd.DataFrame(return_data).round(2)
# return_df['mention_sum']=pd.Series()
# for ticker in df_merge['ticker'].unique():
#     return_df['mention_sum'].append(
#         pd.Series(sum(df_merge[df_merge['ticker']==ticker].count())))

