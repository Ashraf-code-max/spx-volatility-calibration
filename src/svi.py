import numpy as np
from scipy.optimize import least_squares


def svi_total_variance(k, a, b, rho, m, sigma_svi):
    """Raw SVI total variance parameterization."""
    return a + b * (
        rho * (k - m)
        + np.sqrt((k - m)**2 + sigma_svi**2)
    )


def calibrate_svi(k, market_total_variance):
    """Calibrate one raw-SVI slice by nonlinear least squares."""
    k = np.asarray(k)
    market_total_variance = np.asarray(market_total_variance)

    def residuals(params):
        a, b, rho, m, sigma_svi = params
        model = svi_total_variance(k, a, b, rho, m, sigma_svi)
        return model - market_total_variance

    initial_guess = [0.01, 0.10, -0.30, 0.00, 0.10]
    lower_bounds = [-1.0, 0.0, -0.999, -1.0, 1e-4]
    upper_bounds = [1.0, 5.0, 0.999, 1.0, 5.0]

    return least_squares(
        residuals,
        initial_guess,
        bounds=(lower_bounds, upper_bounds),
    )
