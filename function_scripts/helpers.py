import numpy as np
from scipy.optimize import curve_fit


def normalize(array):
    """
    Normalize array to range [0, 1].

    Parameters:
        array (np.ndarray): Input array.

    Returns:
        np.ndarray: Normalized array.
    """
    array = array.astype(np.float32)
    min_val = np.min(array)
    max_val = np.max(array)
    return (array - min_val) / (max_val - min_val + 1e-12)


def mod_1(array):
    """
    Wrap phase values into the [0, 1] range.

    Parameters:
        array (np.ndarray): Input array.

    Returns:
        np.ndarray: Phase-wrapped array.
    """
    return np.mod(array, 1.0)


def two_d_gaussian(coords, amplitude, xo, yo, sigma_x, sigma_y, offset):
    """
    2D Gaussian function for fitting.

    Parameters:
        coords (tuple): (x, y) meshgrid.
        amplitude (float): Peak value.
        xo, yo (float): Center coordinates.
        sigma_x, sigma_y (float): Widths.
        offset (float): Baseline.

    Returns:
        np.ndarray: Flattened 2D Gaussian surface.
    """
    x, y = coords
    g = offset + amplitude * np.exp(
        -(((x - xo) ** 2) / (2 * sigma_x ** 2)
          + ((y - yo) ** 2) / (2 * sigma_y ** 2)))
    return g.ravel()


def fit_gaussian_2d(data):
    """
    Fit a 2D Gaussian to a given image array.

    Parameters:
        data (np.ndarray): Input image.

    Returns:
        popt (np.ndarray): Optimal fit parameters.
    """
    x = np.arange(data.shape[1])
    y = np.arange(data.shape[0])
    x, y = np.meshgrid(x, y)
    initial_guess = (np.max(data), data.shape[1]//2, data.shape[0]//2, 30, 30, np.min(data))
    popt, _ = curve_fit(two_d_gaussian, (x, y), data.ravel(), p0=initial_guess)
    return popt
