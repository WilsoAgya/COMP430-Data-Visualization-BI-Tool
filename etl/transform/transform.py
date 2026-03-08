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


def transform_time():

    #Array holds clean time data
    transformed_time_data = []
    seen_timestamps = set()
    index = 0
    for record in raw_data:
    #History is a dataframe with all the dates
        history = record['history']
    # Get each date and makes sure there's no duplicates
        for row in history.index:
            # If theres a duplicate add the date to the set
            if row in seen_timestamps:
                continue
            seen_timestamps.add(row)
            #Appending values to the list
            transformed_time_data.append({
                "time_key":index,
                "fulldate":row,
                "day":row.day,
                "month":row.month,
                "year":row.year
            })
            index+=1

    print(transformed_time_data)


'''def transform_industry():

def transform_profitability():'''

transform_time()
