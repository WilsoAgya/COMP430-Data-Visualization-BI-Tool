from fastapi import APIRouter
from psycopg2.extras import RealDictCursor
from db.connection import get_connection

router = APIRouter()

@router.get("/risk")
def get_risk():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM dim_risk")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return data