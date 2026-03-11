import pandas as pd
import requests
import yfinance as yf
from etl.extract.extract import extract
import io

raw_data = extract()


def transform_ticker():

    transformed_ticker_data = []
    seen_symbols = set()

    for index, record in enumerate(raw_data):
        info = record["info"]

        if not info:
            continue

        if not info.get("shortName"):
            continue

        if not record.get("ticker"):
            continue

        symbol = info.get("symbol")

        if symbol in seen_symbols:
            continue

        seen_symbols.add(symbol)

        full_summary = info.get("longBusinessSummary", "")
        sentences = full_summary.split(". ")
        short_summary = (". ".join(sentences[:3]) + ".")[:500] if sentences else ""

        transformed_ticker_data.append({
            "ticker_id": index,
            "company_name": info.get("shortName"),
            "ticker_symbol": record.get("ticker"),
            "market": info.get("country"),
            "ticker_info": short_summary,
        })

    print(transformed_ticker_data)
    return transformed_ticker_data


def transform_time(data):

    transformed_time_data = []
    seen_timestamps = set()
    index = 0
    for record in data:
    #History is a dataframe with all the dates
        history = record['history']
    # Get each date and makes sure there's no duplicates
        for row in history.index:

            if row in seen_timestamps:
                continue

            seen_timestamps.add(row)

            transformed_time_data.append({
                "time_key": index,
                "full_date": row,
                "day": row.day,
                "month": row.month,
                "year": row.year
            })

            index += 1

    return transformed_time_data


def transform_industry():

    transformed_industry_data = []
    seen_industries = set()
    index = 0

    for record in raw_data:
        info = record["info"]

        industry = info.get("industry")

        if not industry:
            continue

        if industry in seen_industries:
            continue

        seen_industries.add(industry)

        transformed_industry_data.append({
            "industry_id": index,
            "industry_name": industry,
            "sector": info.get("sector"),
            "currency": info.get("currency")
        })

        index += 1

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

    for index, record in enumerate(raw_data):

        info = record["info"]

        net_income = info.get("netIncomeToCommon")
        total_debt = info.get("totalDebt")
        book_value = info.get("bookValue")
        shares = info.get("sharesOutstanding")

        if None in (net_income, total_debt, book_value, shares) or (book_value * shares + total_debt) == 0:
            roic = None
        else:
            roic = net_income / (book_value * shares + total_debt)

        profitability_data.append({
            "tier_id": index,
            "roa_tier": get_roa_tier(info.get("returnOnAssets")),
            "roic_tier": get_roic_tier(roic)
        })

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
            "risk_rating_overall": info.get("overallRisk")
        })

    return risk_data


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

    for index, record in enumerate(raw_data):

        info = record["info"]
        change = info.get("52WeekChange")

        analysis_data.append({
            "analysis_key": index,
            "trend_direction": get_trend_direction(change),
            "trend_value": change
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
