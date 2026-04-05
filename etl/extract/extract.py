import pandas as pd
import requests
import yfinance as yf
import io
from typing import List, Dict, Any, Optional

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Optional: dynamic ticker list
def get_sp500_tickers() -> List[str]:
    response = requests.get(url, headers=headers)
    table = pd.read_html(io.StringIO(response.text))[0]
    return table["Symbol"].tolist()

# For now: fixed tickers
TICKERS = ['AMD','AAPL','MSFT','GOOG','TSLA','NVDA','JPM','HOOD','PEP','VST']


def extract(tickers: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    tickers = tickers or TICKERS
    raw_data: List[Dict[str, Any]] = []

    for ticker in tickers:
        try:
            finance_data = yf.Ticker(ticker)

            raw_data.append({
                "ticker": ticker,
                "info": finance_data.info or {},
                "financials": finance_data.financials,
                "history": finance_data.history(period="6mo", interval="1h")
            })

        except Exception as e:
            print(f"Failed for {ticker}: {e}")

    return raw_data