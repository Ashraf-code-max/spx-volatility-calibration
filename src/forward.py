import numpy as np


def estimate_forward_and_discount(data, window=500):
    """Estimate F and D from C - P = D(F - K) using near-ATM strikes."""
    work = data.copy()
    work["call_put_diff"] = work["call_mid"] - work["put_mid"]

    center_index = work["call_put_diff"].abs().idxmin()
    center_strike = work.loc[center_index, "strike"]

    regression_data = work[
        (work["strike"] >= center_strike - window)
        & (work["strike"] <= center_strike + window)
    ].copy()

    strikes = regression_data["strike"].to_numpy()
    price_difference = regression_data["call_put_diff"].to_numpy()

    slope, intercept = np.polyfit(strikes, price_difference, 1)
    discount_factor = -slope
    forward_price = intercept / discount_factor

    fitted = slope * strikes + intercept
    residuals = price_difference - fitted
    rmse = np.sqrt(np.mean(residuals**2))
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((price_difference - np.mean(price_difference))**2)
    r_squared = 1 - ss_res / ss_tot

    return {
        "forward": forward_price,
        "discount_factor": discount_factor,
        "center_strike": center_strike,
        "r_squared": r_squared,
        "rmse": rmse,
        "regression_data": regression_data,
        "slope": slope,
        "intercept": intercept,
    }
