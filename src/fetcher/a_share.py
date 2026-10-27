import akshare as ak
import pandas as pd


def _symbol_prefix(code: str) -> str:
    if code.startswith("6"):
        return f"sh{code}"
    return f"sz{code}"


def fetch_a_share_daily(code: str, start_date: str = "2020-01-01") -> pd.DataFrame:
    symbol = _symbol_prefix(code)
    df = ak.stock_zh_a_daily(symbol=symbol, start_date=start_date, adjust="qfq")
    df = df.reset_index() if "date" not in df.columns else df
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["code"] = code
    df["market"] = "A"
    df["adj_close"] = df["close"]
    cols = ["code", "market", "date", "open", "high", "low", "close", "volume", "adj_close"]
    return df[cols]
