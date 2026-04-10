import psycopg2
import os
from dotenv import load_dotenv
from etl.transform.transform import transform_ticker, transform_time, transform_analysis, transform_industry, \
    transform_facts, transform_risk, transform_profitability
from psycopg2.extras import execute_values
from etl.transform.transform import transform_ticker

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

#Load time dimension
def load_dim_time(conn):
    rows = transform_time()
    cur = conn.cursor()

    for r in rows:
        cur.execute(

            '''INSERT INTO dim_time
            (time_key,full_date,year,month,day,hour,minute,timezone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (time_key) DO NOTHING'''
            ,
            (
                r['time_key'],
                r['full_date'],
                r['year'],
                r['month'],
                r['day'],
                r['hour'],
                r['minute'],
                r['timezone']
            )
        )

    #Updates time dimension with hour, minute, and time zone
        '''  cur.execute(

            UPDATE dim_time
                SET hour = %s,
                    minute = %s,
                    timezone = %s
                WHERE time_key = %s
                
                (
                    r['hour'],
                    r['minute'],
                    r['timezone'],
                    r['time_key']
                )

        ) '''

    conn.commit()
    cur.close()

def load_dim_analysis(conn):
    rows = transform_analysis()
    cur = conn.cursor()

    for r in rows:
        cur.execute(
            """
            INSERT INTO dim_analysis
            (analysis_key,trend_direction,change)
            VALUES (%s, %s, %s)
            ON CONFLICT (analysis_key) DO NOTHING
            """,
            (
                r["analysis_key"],
                r["trend_direction"],
                r["trend_value"]

            )
        )
    conn.commit()
    cur.close()

#load industry dimension
def load_dim_industry(conn):
    rows = transform_industry()
    cur = conn.cursor()

    for r in rows:
        cur.execute(
            """
            INSERT INTO dim_industry
            (industry_id, industry_name, sector_name, currency)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (industry_name) DO NOTHING
            """,
            (
                r["industry_id"],
                r["industry_name"],
                r["sector"],
                r["currency"]
            )
        )
    conn.commit()
    cur.close()
#load risk dimension
def load_dim_risk(conn):
    rows = transform_risk()
    cur = conn.cursor()

    for r in rows:
        cur.execute(
            """
            INSERT INTO dim_risk
            (risk_id, risk_category_name, riskratingoverall)
            VALUES (%s, %s, %s)
            ON CONFLICT (risk_id) DO NOTHING
            """,
            (
                r["risk_id"],
                r["risk_category_name"],
                r["risk_rating_overall"]
            )
        )

    conn.commit()
    cur.close()
#load profitability dimension
def load_dim_profitability(conn):
    rows = transform_profitability()
    cur = conn.cursor()

    for r in rows:
        cur.execute(
            """
            INSERT INTO dim_profitability
            (tier_id, roa_tier, roic_tier)
            VALUES (%s, %s, %s)
            ON CONFLICT (tier_id) DO NOTHING
            """,
            (
                r["tier_id"],
                r["roa_tier"],
                r["roic_tier"],

            )
        )

    conn.commit()
    cur.close()
#load ticker dimension

def load_dim_ticker(conn, rows):
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
                r["ticker_info"][:500] if r["ticker_info"] else None
            )
        )

    conn.commit()
    cur.close()




#load fact table
def load_fact_table(conn):
    rows = transform_facts()
    cur = conn.cursor()

    data = [
        (
            r["time_key"],
            r["ticker_id"],
            r["analysis_id"],
            r["profitability_id"],
            r["risk_id"],
            r["industry_id"],
            float(r["return_on_asset"] or 0.0),
            float(r["return_on_investment"]),
            float(r["revenue"]),
            float(r["high_price"] or 0),
            float(r["low_price"] or 0),
            float(r["open_price"] or 0),
            float(r["close_price"] or 0)
        )
        for r in rows
    ]

    execute_values(cur, """
        INSERT INTO facts_table
        (time_id, ticker_id, analysis_id, profitability_id, risk_id, industry_id,
         return_on_asset, return_on_investment, revenue_total_actual,
         high_price, low_price, open_price, closing_price)
        VALUES %s
        ON CONFLICT (time_id, ticker_id) DO NOTHING
    """, data, page_size=1000)

    conn.commit()
    cur.close()


def run():
    conn = connect()
    #load_dim_ticker(conn)
    #load_dim_time(conn)
    #load_dim_industry(conn)
    #load_dim_risk(conn)
    #load_dim_profitability(conn)
    #load_dim_analysis(conn)
    load_fact_table(conn)
    conn.close()
    print("Loaded fact_table")



run()
