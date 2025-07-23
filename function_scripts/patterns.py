import numpy as np
from .helpers import make_grating

def generate_grating_pattern(size, spacing, orientation='horizontal'):
    """Generate a simple grating pattern."""
    if orientation == 'horizontal':
        grating = np.tile(np.linspace(0, 1, spacing), (size[0], size[1] // spacing + 1))
    else:
        grating = np.tile(np.linspace(0, 1, spacing), (size[1], size[0] // spacing + 1)).T
    return grating[:, :size[1]]

def make_phase_patterns(slm_shape, patch_size):
    """Create patch-based phase patterns."""
    rows = slm_shape[0] // patch_size
    cols = slm_shape[1] // patch_size
    patterns = []
    for i in range(rows):
        for j in range(cols):
            pattern = np.zeros(slm_shape)
            pattern[i * patch_size:(i + 1) * patch_size, j * patch_size:(j + 1) * patch_size] = 1
            patterns.append(pattern)
    return patterns
