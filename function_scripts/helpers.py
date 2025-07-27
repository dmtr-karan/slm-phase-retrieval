"""
Utility functions for phase normalization, phase wrapping, and meshgrid creation.
"""

import numpy as np


def normalize(im):
    """
    Normalize an input image or array to the range [0, 1].

    Parameters:
        im (np.ndarray): Input array.

    Returns:
        np.ndarray: Normalized array.
    """
    im = im - np.min(im)
    return im / np.max(im)


def mod_1(arr):
    """
    Wrap values to the range [0, 1] by applying modulo 1.

    Parameters:
        arr (np.ndarray): Input array.

    Returns:
        np.ndarray: Modulo-wrapped array.
    """
    return np.mod(arr, 1)


def make_grid(im, scale=None):
    """
    Return a xy meshgrid based on the input array shape, ranging from
    -scale * width/2 to +scale * width/2.

    Parameters:
        im (np.ndarray): Input image (2D).
        scale (float): Optional spatial scale factor [m/pixel].

    Returns:
        (x, y): np.ndarray meshgrids
    """
    if scale is None:
        scale = 1
    h, w = im.shape
    y_lim, x_lim = h // 2, w // 2

    x, y = np.linspace(-x_lim * scale, x_lim * scale, w), np.linspace(-y_lim * scale, y_lim * scale, h)
    x, y = np.meshgrid(x, y)
    return x, y


def meshgrid_slm(slm_size, pitch):
    """
    Calculate X, Y meshgrid for SLM area using pixel pitch.

    Parameters:
        slm_size (tuple): Physical size (width, height) of the SLM in meters.
        pitch (float): Pixel pitch [m].

    Returns:
        tuple: (X, Y) meshgrid arrays in meters.
    """
    x = np.arange(-slm_size[0] / 2, slm_size[0] / 2, pitch)
    return np.meshgrid(x, x)


def closest_arr(arr, K):
    """
    Find the value in arr closest to K.

    Parameters:
        arr (np.ndarray): Array to search.
        K (float): Target value.

    Returns:
        tuple: (index, value)
    """
    diff = np.abs(arr - K)
    index = diff.argmin()
    return index, arr[index]
