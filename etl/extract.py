import pandas as pd
import requests
import yfinance as yf
import io

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

response = requests.get(url, headers=headers)
sp500_table = pd.read_html(io.StringIO(response.text))[0]
tickers = sp500_table["Symbol"].tolist()

ticker_load = []

#Basic data extraction for the ticker dimension
def extract():
    for index,ticker in enumerate(tickers[:200]):
        try:
            tick_info = yf.Ticker(ticker).info
            full_summary = tick_info.get("longBusinessSummary", "")
            sentences = full_summary.split(". ")
            short_summary = ". ".join(sentences[:3]) + "." if sentences else ""

            ticker_load.append({
            "ticker_id" : index,
            "company_name": tick_info['shortName'],
            "ticker_symbol" : ticker,
            "market" : tick_info['country'],
            'ticker_info' : short_summary
            })

            print(ticker_load)

        except Exception as e:
            print(f"Failed for {ticker}: {e}")

extract()
