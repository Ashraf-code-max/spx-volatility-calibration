import numpy as np
import pandas as pd

from src.implied_vol import implied_volatility


def build_volatility_smile(
    data,
    F,
    T,
    discount_factor,
    max_relative_spread=0.20,
    min_strike_ratio=0.70,
    max_strike_ratio=1.20,
):
    """Construct an OTM-option implied-volatility smile from an SPX chain."""
    results = []

    for _, row in data.iterrows():
        K = row["strike"]
        strike_ratio = K / F

        if strike_ratio < min_strike_ratio or strike_ratio > max_strike_ratio:
            continue

        if K < F:
            option_type = "put"
            bid, ask = row["put_bid"], row["put_ask"]
        else:
            option_type = "call"
            bid, ask = row["call_bid"], row["call_ask"]

        if bid <= 0:
            continue

        mid = (bid + ask) / 2
        relative_spread = (ask - bid) / mid

        if relative_spread > max_relative_spread:
            continue

        try:
            iv = implied_volatility(
                market_price=mid,
                F=F,
                K=K,
                T=T,
                discount_factor=discount_factor,
                option_type=option_type,
            )
        except ValueError:
            continue

        k = np.log(K / F)
        results.append({
            "strike": K,
            "option_type": option_type,
            "bid": bid,
            "ask": ask,
            "mid": mid,
            "relative_spread": relative_spread,
            "log_moneyness": k,
            "implied_vol": iv,
            "total_variance": iv**2 * T,
        })

    return pd.DataFrame(results)
