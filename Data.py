import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Combining 2 datasets into one to get more historical BTC price data
# Dataset one from: https://github.com/Yrzxiong/Bitcoin-Dataset/blob/master/Bit%20Coin.ipynb
# Dataset 2 from: https://uk.finance.yahoo.com/quote/BTC-USD/history/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAArt9m5lhYi3M9_oAhL_hrEij1nus0daSuTTxai-suC4qA-kjciMsPe1YdeTbJDEiMJhxcPKSr4KXbsMsqgtJxpHPc6ZGvZ7NwASNlr2F-4zFRgDKejNksy033I9CNiBHx4OvDNpajOmOMR37_pjTjZve9ie_EErJ93hyZRNlmu6&period1=1410912000&period2=1743608930
# Dataset 1
df = pd.read_csv('//Users//marcusmccourt//Documents//GitHub Projects//Personal.Projects//bitcoin_dataset.csv')
df = df[['Date', 'btc_market_price']]
df['Date'] = pd.to_datetime(df['Date'])
df.columns = df.columns.str.strip()
if 'btc_market_price' in df.columns:
    df.rename(columns={'btc_market_price': 'Price'}, inplace=True)
if 'Date' not in df.columns and 'date' in df.columns:
    df.rename(columns={'date': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df = df[['Date', 'Price']]

# Dataset 2
ticker = "BTC-USD"
start_date = "2014-12-17"
end_date = datetime.today().strftime('%Y-%m-%d')
data = yf.download(ticker, start=start_date, end=end_date)
data.reset_index(inplace=True)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
data = data[['Date', 'Close']]
data.rename(columns={'Close': 'Price'}, inplace=True)
data['Date'] = pd.to_datetime(data['Date'])

# Combine the two datasets 
combined_df = pd.concat([df, data], ignore_index=True)
combined_df = combined_df[['Date', 'Price']]
combined_df.sort_values(by='Date', inplace=True)
combined_df.drop_duplicates(subset='Date', keep='last', inplace=True)
combined_df.reset_index(drop=True, inplace=True)
combined_df['Date'] = pd.to_datetime(combined_df['Date'])
genesis_date = datetime(2009, 1, 3)
combined_df['days_from_genesis'] = (combined_df['Date'] - genesis_date).dt.days
combined_df = combined_df[combined_df['days_from_genesis'] > 0].copy()
