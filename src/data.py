from pathlib import Path
import re

import pandas as pd


COLUMN_NAMES = [
    "expiration",
    "call_symbol",
    "call_last",
    "call_net",
    "call_bid",
    "call_ask",
    "call_volume",
    "call_iv_cboe",
    "call_delta",
    "call_gamma",
    "call_open_interest",
    "strike",
    "put_symbol",
    "put_last",
    "put_net",
    "put_bid",
    "put_ask",
    "put_volume",
    "put_iv_cboe",
    "put_delta",
    "put_gamma",
    "put_open_interest",
]

NUMERIC_COLUMNS = [
    "call_last",
    "call_net",
    "call_bid",
    "call_ask",
    "call_volume",
    "call_iv_cboe",
    "call_delta",
    "call_gamma",
    "call_open_interest",
    "strike",
    "put_last",
    "put_net",
    "put_bid",
    "put_ask",
    "put_volume",
    "put_iv_cboe",
    "put_delta",
    "put_gamma",
    "put_open_interest",
]


def read_cboe_metadata(path):
    """Read the quote timestamp and displayed SPX level from a Cboe CSV."""
    path = Path(path)
    lines = path.read_text(encoding="utf-8-sig").splitlines()

    index_line = next(line for line in lines if line.startswith("S&P 500 INDEX,"))
    date_line = next(line for line in lines if line.startswith("Date:"))

    last_match = re.search(r"Last:\s*([0-9.]+)", index_line)
    date_text = date_line.split(",", 1)[0].replace("Date:", "").strip()
    date_text = date_text.split(" at ", 1)[0]

    return {
        "quote_date": pd.to_datetime(date_text),
        "spot_displayed": float(last_match.group(1)) if last_match else None,
    }


def load_cboe_csv(path):
    """Load the option table from a Cboe delayed-quote CSV."""
    path = Path(path)
    lines = path.read_text(encoding="utf-8-sig").splitlines()

    header_row = next(
        i for i, line in enumerate(lines)
        if line.startswith("Expiration Date,")
    )

    data = pd.read_csv(path, skiprows=header_row)
    data.columns = COLUMN_NAMES

    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data["expiration"] = pd.to_datetime(data["expiration"])
    return data


def clean_quotes(data):
    """Remove invalid quotes and add call/put mid-prices."""
    required = ["strike", "call_bid", "call_ask", "put_bid", "put_ask"]
    clean = data.dropna(subset=required).copy()

    clean = clean[
        (clean["call_bid"] >= 0)
        & (clean["call_ask"] >= clean["call_bid"])
        & (clean["put_bid"] >= 0)
        & (clean["put_ask"] >= clean["put_bid"])
    ].copy()

    clean["call_mid"] = (clean["call_bid"] + clean["call_ask"]) / 2
    clean["put_mid"] = (clean["put_bid"] + clean["put_ask"]) / 2
    return clean
