from fastapi import APIRouter
from psycopg2.extras import RealDictCursor
from backend.api.db.connection import get_connection

router = APIRouter()

@router.get("/time")
def get_time():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM dim_time")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return data