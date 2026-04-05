from fastapi import APIRouter
from api.db.connection import get_connection

router = APIRouter()

@router.get("/tickers")
def get_tickers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM dim_ticker")
    rows = cur.fetchall()
    
    if not cur.description:
        return []

    columns = [col[0] for col in cur.description]

    result = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()

    return result