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

    return transformed_ticker_data


def transform_time():

    transformed_time_data = []
    seen_timestamps = set()
    index = 0

    for record in raw_data:
        history = record["history"]

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

    return profitability_data


def transform_risk():

    risk_data = []

    for index, record in enumerate(raw_data):

        info = record["info"]

        risk_data.append({
            "risk_id": index,
            "risk_category_name": "Overall Risk",
            "risk_rating_overall": info.get("overallRisk")
        })

    return risk_data


def transform_analysis():

    analysis_data = []

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

    return analysis_data