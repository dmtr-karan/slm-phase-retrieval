"""
Utility functions for phase normalization, phase wrapping, and meshgrid creation.
"""

import numpy as np


def normalize(arr):
    """
    Normalize input array to [0,1]
    """
    min_val, max_val = arr.min(), arr.max()
    return (arr - min_val) / (max_val - min_val) if max_val > min_val else arr


def mod_1(arr):
    """
    Wrap array phase values to [0,1)
    """
    return np.mod(arr, 1)


def centered_meshgrid(npx, npy):
    """
    Returns meshgrid centered at (0,0) in pixel coordinates.
    """
    x = np.arange(-npx // 2, npx // 2)
    y = np.arange(-npy // 2, npy // 2)
    return np.meshgrid(x, y)