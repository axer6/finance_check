import akshare as ak
import pandas as pd


def fetch_a_share_daily(code: str, start_date: str = "20200101", end_date: str = None) -> pd.DataFrame:
    df = ak.stock_zh_a_hist(
        symbol=code,
        period="daily",
        start_date=start_date,
        end_date=end_date or "",
        adjust="qfq",
    )
    df = df.rename(columns={
        "日期": "date",
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
    })
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["code"] = code
    df["market"] = "A"
    df["adj_close"] = df["close"]
    cols = ["code", "market", "date", "open", "high", "low", "close", "volume", "adj_close"]
    return df[cols]
