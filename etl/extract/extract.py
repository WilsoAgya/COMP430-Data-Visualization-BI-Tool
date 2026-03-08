import pandas as pd
import requests
import yfinance as yf
import io

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

response = requests.get(url, headers=headers)
sp500_table = pd.read_html(io.StringIO(response.text))[0]
'''tickers = sp500_table["Symbol"].tolist()'''
#Decided to stick with hardcoded companies for now just using 10 popular ones
tickers = ['AMD','AAPL','MSFT','GOOG','TSLA','NVDA','JPM','HOOD','PEP','VST']


raw_data = []

#Basic data extraction for the ticker dimension
def extract():

    raw_data.clear()

    for ticker in tickers:
        finance_data = yf.Ticker(ticker)
        #Extraction of useful data from the yfinance API
        try:
            raw_data.append({
                "ticker" : ticker,
                "info" : finance_data.info, 
                "financials" : finance_data.financials,
                "history": finance_data.history(period="6mo", interval="1h")
            })
        except Exception as e:
            print(f"Failed for {ticker}: {e}")



    return raw_data

