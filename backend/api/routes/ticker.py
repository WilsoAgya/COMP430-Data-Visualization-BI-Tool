from fastapi import APIRouter, HTTPException, Depends
from db.connection import get_connection

router = APIRouter()

@router.get("/stocks/{symbol}")
def get_stock_data(symbol: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
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
            ORDER BY tm.full_date DESC 
            LIMIT 100;
        """
        cur.execute(query, (symbol.upper(),))
        rows = cur.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "symbol": row[0],
                "high": float(row[1]),
                "low": float(row[2]),
                "close": float(row[3]),
                "date": str(row[4])
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

    return result
