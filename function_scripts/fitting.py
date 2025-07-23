
import numpy as np
from scipy.optimize import curve_fit


def fringe_model(coords, a, b, delta_phi, offset):
    """
    Interference fringe model used for fitting.
    """
    x, y = coords
    return a * b * np.cos(x + delta_phi) + offset


def fit_fringe_pattern(data, guess_params, coords):
    """
    Fit the fringe pattern to extract phase and intensity.
    """
    try:
        popt, pcov = curve_fit(fringe_model, coords, data.ravel(), p0=guess_params)
        return popt
    except RuntimeError:
        return None
