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


def transform_industry():
    transformed_industry_data = []
    seen_industries = set()
    index = 0

    for record in raw_data:
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



def transform_profitability():
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
    for record in raw_data:
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

def transform_risk():
    risk_data = []
    index = 0
    for record in raw_data:
        info = record['info']

        risk_data.append({
            "risk_id": index,
            "risk_category_name": "Overall Risk",
            "risk_rating_overall": info['overallRisk'],
        })
        index += 1

def transform_analysis():
    analysis_data = []
    index = 0

    def get_trend_direction(change):
        if change is None:
            return "Unknown"
        elif change > 0.10:
            return "Uptrend"
        elif change < -0.10:
            return "Downtrend"
        else:
            return "Sideways"

    for record in raw_data:
        info = record['info']

        analysis_data.append({
            "trend_id": index,
            "trend_direction": get_trend_direction(info['52WeekChange']),
            "trend_value": info['52WeekChange']

        })
        index+=1
    print(analysis_data)

#def transform_facts():


#transform_profitability()
#transform_industry()
#transform_time()
