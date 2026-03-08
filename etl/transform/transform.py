import pandas as pd
import requests
import yfinance as yf
from etl.extract import extract
import io

raw_data = extract.extract()
#Basic data extraction for the ticker dimension
def transform_ticker():


    transformed_ticker_data = []
    seen_symbols = set()

    #Handling messy data
    for index,record in enumerate(raw_data):
        info = record["info"]
        if not info:
            continue
        if not info['shortName']:
            continue
        if not record['ticker']:
            continue

        symbol = info ['symbol']
        if symbol in seen_symbols:
            continue
        seen_symbols.add(symbol)

        #Makes it only have 3 sentences for the overview

        full_summary = info.get("longBusinessSummary", "")
        sentences = full_summary.split(". ")
        short_summary = ". ".join(sentences[:3]) + "." if sentences else ""

        transformed_ticker_data.append({
            "ticker_id": index,
            "company_name": info["shortName"],
            "ticker_symbol": record['ticker'],
            "market": info["country"],
            "ticker_info": short_summary,
        })

    print(transformed_ticker_data)


'''def transform_time():
    


def transform_industry():

def transform_profitability():'''

transform_ticker()
