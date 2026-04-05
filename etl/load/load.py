import psycopg2
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()


def connect():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE", "require")
    )


# ---------- LOAD TICKER ----------
def load_dim_ticker(conn, rows: List[Dict]):
    cur = conn.cursor()

    for r in rows:
        cur.execute(
            """
            INSERT INTO dim_ticker
            (ticker_id, company_name, ticker_symbol, market, ticker_info)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (ticker_id) DO NOTHING
            """,
            (
                r["ticker_id"],
                r["company_name"],
                r["ticker_symbol"],
                r["market"],
                r["ticker_info"][:500] if r["ticker_info"] else None
            )
        )

    conn.commit()
    cur.close()


# ---------- RUN FULL ETL ----------
def run_etl():
    from etl.extract.extract import extract
    from etl.transform.transform import transform_ticker

    conn = connect()

    raw_data = extract()
    ticker_data = transform_ticker(raw_data)

    load_dim_ticker(conn, ticker_data)

    conn.close()

    print("ETL completed successfully")


if __name__ == "__main__":
    run_etl()