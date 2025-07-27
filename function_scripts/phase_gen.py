"""
phase_gen.py

Stub module for SLM phase pattern generation.
Originally adapted from the 'phasamp' and 'hologradpy' repositories.

To be implemented in full later. Provides interface-compatible dummy behavior.

Author: Dimitrios Karanikolopoulos
"""

import numpy as np

# Internal storage
grating = None
patch = None
final_phase = None

# Control flags
grating_as_usual = True
correction_path = ""
which_phases = {
    "grating": False,
    "patch": False,
    "corr_patt": False,
    "corr_phase": False
}

def linear_grating(shape=(1024, 1272), period_px=40):
    """
    Create a horizontal grating pattern.

    Args:
        shape (tuple): (height, width) of the SLM.
        period_px (int): Pixel period of the grating.

    Returns:
        np.ndarray: Grating phase in [0, 1].
    """
    h, w = shape
    x = np.arange(w)
    grating_line = np.mod(x, period_px) / period_px
    gr = np.tile(grating_line, (h, 1))
    global grating
    grating = gr
    return gr

def make_full_slm_array():
    """
    Combines available phase components into a final SLM array.

    To be replaced with logic that loads correction files, applies patches, etc.

    Returns:
        np.ndarray: Final SLM phase pattern (normalized, float32).
    """
    global grating, patch, final_phase
    shape = grating.shape if grating is not None else (1024, 1272)

    # For now: simply return grating if available
    if grating is not None:
        final_phase = grating.copy()
    else:
        final_phase = np.zeros(shape)

    return final_phase
