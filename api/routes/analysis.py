from fastapi import APIRouter
from psycopg2.extras import RealDictCursor
from api.db.connection import get_connection

router = APIRouter()

@router.get("/analysis")
def get_analysis():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM dim_analysis")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return data