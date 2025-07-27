import numpy as np
import scipy.optimize as opt

class FitSine:
    """
    2D Sine fitter for interferogram analysis.

    Fits fringe images to a cosine model of the form:
        f(x, y) = a * cos(kx * x + ky * y + phi) + c

    The gradient components kx, ky are determined from known dx, dy values
    and system wavelength/focal length parameters.

    Attributes:
        fl (float): Focal length [m].
        k (float): Wavenumber [rad/m].
    """

    def __init__(self, fl: float, k: float):
        self.fl = fl
        self.k = k
        self.kx = None
        self.ky = None

    def set_dx_dy(self, dx: float, dy: float):
        """
        Sets fringe spatial frequency based on patch offset dx, dy.

        Args:
            dx (float): Patch X-offset [m].
            dy (float): Patch Y-offset [m].
        """
        self.kx = self.k * dx / self.fl
        self.ky = self.k * dy / self.fl

    def fit_sine(self, XY, phi, a1, a2):
        """
        2D cosine model used for fitting interferograms.

        Args:
            XY (np.ndarray): Stacked X, Y grid vectors (2 x N).
            phi (float): Relative phase offset.
            a1 (float): Amplitude of beam 1.
            a2 (float): Amplitude of beam 2.

        Returns:
            np.ndarray: Flattened model image.
        """
        x, y = XY
        cos_term = np.cos(self.kx * x + self.ky * y + phi)
        return (a1 * a2 * cos_term).ravel()

def safe_fit(model_func, x_data, y_data, p0, bounds):
    """
    Wrapper for curve fitting with error handling.

    Args:
        model_func (callable): Model function to fit.
        x_data (np.ndarray): Input data for independent variable(s).
        y_data (np.ndarray): Measured values.
        p0 (list): Initial guess.
        bounds (tuple): Parameter bounds.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Fit parameters and covariance matrix.
    """
    try:
        popt, pcov = opt.curve_fit(model_func, x_data, y_data, p0=p0, bounds=bounds, maxfev=50000)
        return popt, pcov
    except RuntimeError:
        print("Fit failed — returning zeros.")
        return np.zeros(len(p0)), np.zeros((len(p0), len(p0)))
