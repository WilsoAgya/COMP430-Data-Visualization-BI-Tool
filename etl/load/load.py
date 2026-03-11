import psycopg2
from etl.transform.transform import transform_ticker

def connect():
    return psycopg2.connect(
        host="db.jakobupton.dev",
        database="comp430",
        user="comp430",
        password="COMP430group",
        port=5432,
        sslmode="require"  # safe default for remote Postgres; remove if it fails
    )

def load_dim_ticker(conn):
    rows = transform_ticker()
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
                r["ticker_info"]
            )
        )

    conn.commit()
    cur.close()

def run():
    conn = connect()
    load_dim_ticker(conn)
    conn.close()
    print("Loaded dim_ticker.")

if __name__ == "__main__":
    run()