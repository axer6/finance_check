import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "stock.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS stock_daily (
    code TEXT NOT NULL,
    market TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    adj_close REAL,
    PRIMARY KEY (code, date)
);
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    return conn


def upsert(df: pd.DataFrame):
    if df.empty:
        return
    conn = get_conn()
    df.to_sql("stock_daily", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()


def query(code: str, start: str = None, end: str = None) -> pd.DataFrame:
    conn = get_conn()
    sql = "SELECT * FROM stock_daily WHERE code = ?"
    params = [code]
    if start:
        sql += " AND date >= ?"
        params.append(start)
    if end:
        sql += " AND date <= ?"
        params.append(end)
    sql += " ORDER BY date"
    df = pd.read_sql_query(sql, conn, params=params, parse_dates=["date"])
    conn.close()
    return df
