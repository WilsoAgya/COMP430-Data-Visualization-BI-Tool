import pandas as pd
import requests
import yfinance as yf
#from pandas.conftest import index_with_missing

from etl.extract import extract
import io

raw_data = extract.extract()
#Basic data extraction for the ticker dimension
def transform_ticker(data):


    transformed_ticker_data = []
    seen_symbols = set()

    #Handling messy data
    for index,record in enumerate(data):
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
    return transformed_ticker_data


def transform_time(data):

    #Array holds clean time data
    transformed_time_data = []
    seen_timestamps = set()
    index = 0
    for record in data:
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
    return transformed_time_data

#Set up industry data
def transform_industry(data):
    transformed_industry_data = []
    seen_industries = set()
    index = 0

    #Checks each entry in raw_data and error checks the entries
    for record in data:
        industry_info = record['info']

        if not['info']:
            continue
        if not industry_info['industry']:
            continue

        if record in transformed_industry_data:
            continue
        seen_industries.add(industry_info['industry'])

        transformed_industry_data.append({
            "industry_id": index,
            "industry_name": industry_info['industry'],
            "sector": industry_info['sector'],
            "currency": industry_info['currency']
        })
        index+=1

    print(transformed_industry_data)
    return transformed_industry_data


#Set up for profitability dimension
def transform_profitability(data):
    #returnOnAsset is in api so we made function that checks the value of the roa based on its value
    def get_roa_tier(roa):
        if roa is None:
            return "Unknown"
        elif roa >= 0.20:
            return "Excellent"
        elif roa >= 0.10:
            return "Good"
        elif roa >= 0.05:
            return "Average"
        else:
            return "Poor"

    #Roic will be calculated
    def get_roic_tier(roic):
        if roic is None:
            return "Unknown"
        elif roic >= 0.20:
            return "Excellent"
        elif roic >= 0.12:
            return "Good"
        elif roic >= 0.06:
            return "Average"
        else:
            return "Poor"

    profitability_data = []
    index = 0
    for record in data:

        #Get values necessary for calculation and compute the return on investment capital
        net_income = record['info'].get('netIncomeToCommon')
        total_debt = record['info'].get('totalDebt')
        book_value = record['info'].get('bookValue')
        shares = record['info'].get('sharesOutstanding')

        if None in (net_income, total_debt, book_value, shares) or (book_value * shares + total_debt) == 0:
            roic = None
        else:
            roic = net_income / (book_value * shares + total_debt)

        profitability_data.append({
            "tier_id": index,
            "roa_tier": get_roa_tier(record['info'].get('returnOnAssets')),
            "roic_tier": get_roic_tier(roic)
        })
        index += 1

    print(profitability_data)
    return profitability_data


#Setting up risk data
def transform_risk(data):
    transformed_risk_data = []
    index = 0
    for record in data:
        info = record['info']
        if not info:
            continue

        transformed_risk_data.append({
            "risk_id": index,
            "risk_category_name": "Overall Risk",
            "risk_rating_overall": info.get('overallRisk'),
        })
        index += 1

    return transformed_risk_data

#Analysis dimension
def transform_analysis(data):
    transformed_analysis_data = []
    index = 0

    #Gets the trend direction
    def get_trend_direction(change):
        if change is None:
            return "Unknown"
        elif change > 0.10:
            return "Uptrend"
        elif change < -0.10:
            return "Downtrend"
        else:
            return "Sideways"

    for record in data:
        info = record['info']

        transformed_analysis_data.append({
            "trend_id": index,
            "trend_direction": get_trend_direction(info['52WeekChange']),
            "trend_value": info['52WeekChange']

        })
        index+=1
    print(transformed_analysis_data)
    return transformed_analysis_data


def transform_facts():
    fact_data = []

    ticker_data = transform_ticker(raw_data)
    time_data = transform_time(raw_data)
    industry_data = transform_industry(raw_data)
    profitability_data = transform_profitability(raw_data)
    risk_data = transform_risk(raw_data)
    analysis_data = transform_analysis(raw_data)

    for index, record in enumerate(raw_data):
        info = record.get('info')
        if not info:
            continue

        history = record['history']

        net_income = info.get('netIncomeToCommon')
        total_debt = info.get('totalDebt')
        book_value = info.get('bookValue')
        shares = info.get('sharesOutstanding')

        # ROIC = Net Income / (Equity + Debt)
        equity = book_value * shares

        if None in (net_income, total_debt, book_value, shares) or (equity + total_debt) == 0:
            roic = None
        else:
            roic = net_income / (equity + total_debt)

        #The time of the exchange is the grain for the data warehouse. This will be observing data of 1h intervals in a span of 6months
        for time_record in time_data:
            date = time_record['fulldate']

            fact_data.append({
                # Dimension IDs
                "ticker_id": ticker_data[index]['ticker_id'],
                "time_key": time_record['time_key'],
                "industry_id": industry_data[index]['industry_id'],
                "tier_id": profitability_data[index]['tier_id'],
                "risk_id": risk_data[index]['risk_id'],
                "trend_id": analysis_data[index]['trend_id'],
                # Measured values
                "close_price": history.loc[date, 'Close'] if date in history.index else None,
                "open_price": history.loc[date, 'Open'] if date in history.index else None,
                "high_price": history.loc[date, 'High'] if date in history.index else None,
                "low_price": history.loc[date, 'Low'] if date in history.index else None,
                "revenue": info.get('totalRevenue'),
                'return_on_asset': info.get('returnOnAssets'),
                'return_on_investment': roic
            })

    print(fact_data)
    return fact_data

transform_facts()

#transform_profitability(raw_data)
#transform_industry()
#transform_time()
