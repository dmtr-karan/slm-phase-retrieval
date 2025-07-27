import os
import numpy as np
from slm.slm_hamamatsu import SlmHamamatsu
from function_scripts.helpers import mod_1, normalize
from PIL import Image
import glob


def load_correction_phase(corr_path: str) -> np.ndarray:
    """
    Load and normalize the correction phase from BMP file.
    """
    if not os.path.exists(corr_path):
        raise FileNotFoundError(f"Correction BMP not found: {corr_path}")
    with Image.open(corr_path) as img:
        img_array = np.asarray(img, dtype=np.uint16)
    return normalize(img_array)


def generate_horizontal_grating(shape: tuple[int, int], period_px: int = 30) -> np.ndarray:
    """
    Create a simple horizontal phase grating pattern.
    """
    y, x = np.indices(shape)
    return normalize(np.mod(x, period_px).astype(np.float32))


def main():
    slm = SlmHamamatsu()
    slm.connect()

    # Load correction pattern from BMP
    corr_folder = os.path.join(os.path.dirname(__file__), "corr_patties")
    bmp_files = glob.glob(os.path.join(corr_folder, "*.bmp"))
    if not bmp_files:
        print("Correction pattern BMP not found in folder.")
        return
    correction = load_correction_phase(bmp_files[0])

    # Generate horizontal grating
    grating = generate_horizontal_grating(correction.shape)

    # Combine and wrap phase
    combined_phase = mod_1(grating + correction) * 198  # 198 is modDepth at 752nm
    slm.load_phase(combined_phase.astype(np.uint8))
    print("Phase loaded onto SLM.")

    input("Press Enter to close SLM connection...")
    slm.close_slm()


if __name__ == "__main__":
    main()
