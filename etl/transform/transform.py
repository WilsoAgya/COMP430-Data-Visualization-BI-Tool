
from etl.extract.extract import extract
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv


raw_data = extract()


def transform_ticker():


    transformed_ticker_data = []
    seen_symbols = set()
    index = 0
    for record in raw_data:
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
        index+=1

    print(transformed_ticker_data)
    return transformed_ticker_data


def transform_time():

    transformed_time_data = []
    seen_timestamps = set()
    index = 0
    for record in raw_data:
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
                "year": row.year,
                 "hour":row.hour,
                "minute":row.minute,
                "timezone": str(row.tzinfo)
            })


            index += 1

    return transformed_time_data


#Set up industry data
def transform_industry():
    transformed_industry_data = []
    seen_industries = set()
    index = 0

    #Checks each entry in raw_data and error checks the entries
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
    return transformed_industry_data


def transform_profitability():
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
    for record in raw_data:

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
        index+=1


    return profitability_data


#Setting up risk data
def transform_risk():
    transformed_risk_data = []
    index = 0
    for record in raw_data:
        info = record['info']
        if not info:
            continue

        transformed_risk_data.append({
            "risk_id": index,
            "risk_category_name": "Overall Risk",
            "risk_rating_overall": info.get("overallRisk")
        })
        index+=1

    return transformed_risk_data

#Analysis dimension
def transform_analysis():
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
        return "Sideways"

    for record in raw_data:

        info = record["info"]
        change = info.get("52WeekChange")

        transformed_analysis_data.append({
            "analysis_key": index,
            "trend_direction": get_trend_direction(change),
            "trend_value": change
        })
        index+=1
    return transformed_analysis_data


def get_industry_lookup():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE", "require")
    )
    cur = conn.cursor()
    cur.execute("SELECT industry_id, industry_name FROM dim_industry;")
    rows = cur.fetchall()
    # Returns a dict like {"Technology": 6, "Finance": 15}
    return {name: id for id, name in rows}


def transform_facts():
    global raw_data
    fact_data = []

    seen = set()
    def is_valid(record):
        info = record.get('info')
        if not info:
            return False
        if not info.get('shortName'):
            return False
        if not record.get('ticker'):
            return False
        symbol = info.get('symbol')
        if symbol in seen:
            return False
        seen.add(symbol)
        return True

    raw_data_clean = [r for r in raw_data if is_valid(r)]
    original_raw_data = raw_data
    raw_data = raw_data_clean

    ticker_data = transform_ticker()
    time_data  = transform_time()
    industry_data  = transform_industry()
    profitability_data = transform_profitability()
    risk_data  = transform_risk()
    analysis_data  = transform_analysis()
    industry_lookup = get_industry_lookup()

    raw_data = original_raw_data

    print(f"raw_data_clean: {len(raw_data_clean)}")
    print(f"ticker_data: {len(ticker_data)}")
    print(f"industry_data:   {len(industry_data)}")
    print(f"profitability_data: {len(profitability_data)}")
    print(f"risk_data:{len(risk_data)}")
    print(f"analysis_data: {len(analysis_data)}")

    #Check for no null values
    def safe_float(val):
        try:
            return float(val) if pd.notna(val) else None
        except Exception:
            return None
    #check if prices are valid
    def safe_price(history, date, col):
        try:
            if date not in history.index:
                return None
            val = history.loc[date, col]
            return float(val) if pd.notna(val) else None
        except Exception:
            return None

    for index, record in enumerate(raw_data_clean):
        info = record.get('info')
        history = record['history']

        industry_name = industry_data[index]['industry_name']
        actual_industry_id = industry_lookup.get(industry_name)

        net_income = info.get('netIncomeToCommon')
        total_debt = info.get('totalDebt')
        book_value = info.get('bookValue')
        shares  = info.get('sharesOutstanding')

        if None in (net_income, total_debt, book_value, shares):
            roic = None
        else:
            equity = book_value * shares
            roic   = net_income / (equity + total_debt) if (equity + total_debt) != 0 else None

        for time_record in time_data:
            date = time_record['full_date']

            fact_data.append({
                "ticker_id": ticker_data[index]['ticker_id'],
                "time_key": time_record['time_key'],
                "industry_id": actual_industry_id,
                "profitability_id": profitability_data[index]['tier_id'],
                "risk_id": risk_data[index]['risk_id'],
                "analysis_id": analysis_data[index]['analysis_key'],
                "close_price":  safe_price(history, date, 'Close'),
                "open_price":  safe_price(history, date, 'Open'),
                "high_price":  safe_price(history, date, 'High'),
                "low_price":  safe_price(history, date, 'Low'),
                "revenue":  safe_float(info.get('totalRevenue')),
                "return_on_asset":  safe_float(info.get('returnOnAssets')),
                "return_on_investment":   safe_float(roic)
            })

    print(fact_data)
    return fact_data



#transform_facts()
#transform_ticker()
#transform_profitability(raw_data)
#transform_industry()
#transform_time()
#transform_risk()