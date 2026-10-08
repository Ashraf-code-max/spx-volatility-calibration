from scipy.optimize import brentq

from src.black import black_call_price, black_put_price


def implied_volatility(
    market_price,
    F,
    K,
    T,
    discount_factor,
    option_type,
):
    """Invert Black's formula to obtain implied volatility."""
    if option_type == "call":
        pricing_function = black_call_price
        lower_bound = discount_factor * max(F - K, 0.0)
        upper_bound = discount_factor * F
    elif option_type == "put":
        pricing_function = black_put_price
        lower_bound = discount_factor * max(K - F, 0.0)
        upper_bound = discount_factor * K
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    if not (lower_bound < market_price < upper_bound):
        raise ValueError("Market price violates Black no-arbitrage bounds")

    def objective(sigma):
        return pricing_function(
            F=F,
            K=K,
            T=T,
            sigma=sigma,
            discount_factor=discount_factor,
        ) - market_price

    return brentq(objective, 1e-6, 5.0)
