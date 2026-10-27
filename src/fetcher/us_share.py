import yfinance as yf
import pandas as pd


def fetch_us_share_daily(code: str, start: str = "2020-01-01") -> pd.DataFrame:
    df = yf.download(code, start=start, auto_adjust=False, progress=False)
    if df.empty:
        return pd.DataFrame()
    df = df.reset_index()
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    df = df.rename(columns={"adj_close": "adj_close"})
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["code"] = code
    df["market"] = "US"
    cols = ["code", "market", "date", "open", "high", "low", "close", "volume", "adj_close"]
    for c in cols:
        if c not in df.columns:
            df[c] = None
    return df[cols]
