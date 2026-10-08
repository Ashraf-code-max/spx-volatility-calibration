import numpy as np

from src.black import black_call_price
from src.svi import svi_total_variance


def svi_call_prices(strikes, F, T, discount_factor, svi_params):
    """Convert an SVI smile into European call prices."""
    strikes = np.asarray(strikes)
    a, b, rho, m, sigma_svi = svi_params
    k = np.log(strikes / F)
    total_variance = svi_total_variance(k, a, b, rho, m, sigma_svi)

    if np.any(total_variance <= 0):
        raise ValueError("SVI produced non-positive total variance on the grid")

    implied_vol = np.sqrt(total_variance / T)
    return np.array([
        black_call_price(F, K, T, vol, discount_factor)
        for K, vol in zip(strikes, implied_vol)
    ])


def check_call_monotonicity(call_prices, tolerance=1e-8):
    """Calls should be non-increasing in strike."""
    first_differences = np.diff(np.asarray(call_prices))
    violations = first_differences > tolerance
    return first_differences, violations


def check_butterfly_arbitrage(call_prices, tolerance=1e-8):
    """On an equally spaced grid, calls should be convex in strike."""
    prices = np.asarray(call_prices)
    second_differences = prices[:-2] - 2 * prices[1:-1] + prices[2:]
    violations = second_differences < -tolerance
    return second_differences, violations
