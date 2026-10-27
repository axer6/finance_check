import yaml
from pathlib import Path
from src.fetcher.a_share import fetch_a_share_daily
from src.fetcher.us_share import fetch_us_share_daily
from src.storage.db import upsert

CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "watchlist.yaml"


def load_watchlist() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def refresh_all():
    cfg = load_watchlist()
    for item in cfg.get("a_share", []):
        try:
            df = fetch_a_share_daily(item["code"])
            upsert(df)
            print(f"[OK] A {item['code']} {item['name']} rows={len(df)}")
        except Exception as e:
            print(f"[ERR] A {item['code']}: {e}")

    for item in cfg.get("us_share", []):
        try:
            df = fetch_us_share_daily(item["code"])
            upsert(df)
            print(f"[OK] US {item['code']} {item['name']} rows={len(df)}")
        except Exception as e:
            print(f"[ERR] US {item['code']}: {e}")


if __name__ == "__main__":
    refresh_all()
