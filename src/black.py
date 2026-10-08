import numpy as np
from scipy.stats import norm


def black_call_price(F, K, T, sigma, discount_factor=1.0):
    """Black price of a European call written on a forward."""
    if T <= 0 or sigma <= 0:
        return discount_factor * max(F - K, 0.0)

    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return discount_factor * (F * norm.cdf(d1) - K * norm.cdf(d2))


def black_put_price(F, K, T, sigma, discount_factor=1.0):
    """Black price of a European put written on a forward."""
    if T <= 0 or sigma <= 0:
        return discount_factor * max(K - F, 0.0)

    d1 = (np.log(F / K) + 0.5 * sigma**2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return discount_factor * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
