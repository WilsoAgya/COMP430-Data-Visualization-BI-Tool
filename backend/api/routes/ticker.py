from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from backend.api.db.connection import get_connection

router = APIRouter()
RANGE_DAYS = {
    "1M": 30,
    "3M": 90,
    "6M": 180,
    "1Y": 365,
}


# Endpoint to search for tickers based on query parameter
@router.get("/tickers")
def search_tickers(q: str = Query("", min_length=0), limit: int = Query(10, ge=1, le=25)):
    conn = get_connection()
    cur = conn.cursor()

    try:
        normalized_query = q.strip()
        like_query = f"%{normalized_query}%"
        prefix_query = f"{normalized_query}%"

        query = """
            SELECT
                ticker_symbol,
                company_name
            FROM dim_ticker
            WHERE
                %s = ''
                OR ticker_symbol ILIKE %s
                OR company_name ILIKE %s
            ORDER BY
                CASE
                    WHEN ticker_symbol ILIKE %s THEN 0
                    WHEN company_name ILIKE %s THEN 1
                    ELSE 2
                END,
                ticker_symbol ASC
            LIMIT %s;
        """
        cur.execute(
            query,
            (
                normalized_query,
                like_query,
                like_query,
                prefix_query,
                prefix_query,
                limit,
            ),
        )
        rows = cur.fetchall()

        return [{"symbol": row[0], "companyName": row[1]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


# Stocks data endpoint to fetch prices
# uses query param to determine the date range for the data in months
@router.get("/stocks/{symbol}")
def get_stock_data(
    symbol: str,
    range: Literal["1M", "3M", "6M", "1Y"] = Query("6M"),
):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=RANGE_DAYS[range])
        query = """
            SELECT
                t.ticker_symbol as symbol,
                f.high_price as high,
                f.low_price as low,
                f.closing_price as close,
                tm.full_date as date
            FROM facts_table f
            JOIN dim_ticker t ON f.ticker_id = t.ticker_id
            JOIN dim_time tm ON f.time_id = tm.time_key
            WHERE t.ticker_symbol = %s
              AND tm.full_date >= %s
            ORDER BY tm.full_date ASC;
        """
        cur.execute(query, (symbol.upper(), cutoff))
        rows = cur.fetchall()

        result = []
        for row in rows:
            result.append({
                "symbol": row[0],
                "high": float(row[1]),
                "low": float(row[2]),
                "close": float(row[3]),
                "date": str(row[4]),
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

    return result
