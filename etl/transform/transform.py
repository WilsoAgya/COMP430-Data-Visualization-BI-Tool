from typing import List, Dict, Any


# ---------- TICKER ----------
def transform_ticker(raw_data: List[Dict[str, Any]]) -> List[Dict]:
    result = []
    seen = set()

    for index, record in enumerate(raw_data):
        info = record.get("info", {})

        if not info.get("shortName") or not record.get("ticker"):
            continue

        symbol = info.get("symbol")
        if symbol in seen:
            continue
        seen.add(symbol)

        summary = info.get("longBusinessSummary", "")
        sentences = summary.split(". ")
        short_summary = (". ".join(sentences[:3]) + ".")[:500] if sentences else ""

        result.append({
            "ticker_id": index,
            "company_name": info.get("shortName"),
            "ticker_symbol": record.get("ticker"),
            "market": info.get("country"),
            "ticker_info": short_summary
        })

    return result


# ---------- TIME ----------
def transform_time(raw_data: List[Dict[str, Any]]) -> List[Dict]:
    result = []
    seen = set()
    idx = 0

    for record in raw_data:
        history = record.get("history")

        if history is None or history.empty:
            continue

        for ts in history.index:
            if ts in seen:
                continue

            seen.add(ts)

            result.append({
                "time_key": idx,
                "full_date": ts,
                "day": ts.day,
                "month": ts.month,
                "year": ts.year
            })

            idx += 1

    return result


# ---------- INDUSTRY ----------
def transform_industry(raw_data: List[Dict[str, Any]]) -> List[Dict]:
    result = []
    seen = set()
    idx = 0

    for record in raw_data:
        info = record.get("info", {})
        industry = info.get("industry")

        if not industry or industry in seen:
            continue

        seen.add(industry)

        result.append({
            "industry_id": idx,
            "industry_name": industry,
            "sector": info.get("sector"),
            "currency": info.get("currency")
        })

        idx += 1

    return result


# ---------- PROFITABILITY ----------
def transform_profitability(raw_data: List[Dict[str, Any]]) -> List[Dict]:

    def roa_tier(roa):
        if roa is None:
            return "Unknown"
        elif roa >= 0.20:
            return "Excellent"
        elif roa >= 0.10:
            return "Good"
        elif roa >= 0.05:
            return "Average"
        return "Poor"

    def roic_tier(roic):
        if roic is None:
            return "Unknown"
        elif roic >= 0.20:
            return "Excellent"
        elif roic >= 0.12:
            return "Good"
        elif roic >= 0.06:
            return "Average"
        return "Poor"

    result = []

    for idx, record in enumerate(raw_data):
        info = record.get("info", {})

        net_income = info.get("netIncomeToCommon")
        total_debt = info.get("totalDebt")
        book_value = info.get("bookValue")
        shares = info.get("sharesOutstanding")

        if None in (net_income, total_debt, book_value, shares) or (book_value * shares + total_debt) == 0:
            roic = None
        else:
            roic = net_income / (book_value * shares + total_debt)

        result.append({
            "tier_id": idx,
            "roa_tier": roa_tier(info.get("returnOnAssets")),
            "roic_tier": roic_tier(roic)
        })

    return result


# ---------- RISK ----------
def transform_risk(raw_data: List[Dict[str, Any]]) -> List[Dict]:
    result = []

    for idx, record in enumerate(raw_data):
        info = record.get("info", {})

        result.append({
            "risk_id": idx,
            "risk_category_name": "Overall Risk",
            "risk_rating_overall": info.get("overallRisk")
        })

    return result


# ---------- ANALYSIS ----------
def transform_analysis(raw_data: List[Dict[str, Any]]) -> List[Dict]:

    def trend(change):
        if change is None:
            return "Unknown"
        elif change > 0.10:
            return "Uptrend"
        elif change < -0.10:
            return "Downtrend"
        return "Sideways"

    result = []

    for idx, record in enumerate(raw_data):
        info = record.get("info", {})

        change = info.get("52WeekChange")

        result.append({
            "analysis_key": idx,
            "trend_direction": trend(change),
            "trend_value": change
        })

    return result