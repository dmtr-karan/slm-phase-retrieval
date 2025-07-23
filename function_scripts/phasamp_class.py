import numpy as np
import os
import glob
from PIL import Image
from .helpers import normalize, mod_1

class PhaseAmplitudeRetriever:
    """Core class for SLM phase and amplitude retrieval."""

    def __init__(self, slm, camera, shutter, mod_depth=198):
        """
        Parameters:
            slm: SlmDisplay instance
            camera: Camera instance
            shutter: Shutter instance
            mod_depth: Modulation depth (0-255) for given wavelength
        """
        self.slm = slm
        self.camera = camera
        self.shutter = shutter
        self.mod_depth = mod_depth
        self.correction_phase = None
        self.final_phase_mask = None

    def load_correction_pattern(self, filename=None):
        """
        Loads a correction BMP pattern from the slm/corr_patties/ folder.
        Normalizes it and stores it internally.
        """
        current_path = os.getcwd()
        if "tests" in current_path:
            current_path = current_path.replace("\\tests", "")
        if filename is None:
            pattern_path = glob.glob(current_path + r"\\slm\\corr_patties\\CAL_LSH0803420_750nm.bmp")
        else:
            pattern_path = [filename]

        if not pattern_path or not os.path.exists(pattern_path[0]):
            print("Correction pattern BMP does not exist.")
            return

        print("Loading correction pattern from:\n{}".format(pattern_path[0]))
        with Image.open(pattern_path[0]) as img:
            image = np.asarray(img, dtype=np.uint16)
        self.correction_phase = normalize(image)

    def upload_test_grating_with_correction(self, frequency_px=40):
        """
        Builds a horizontal grating and adds correction phase.
        Uploads it to the SLM after proper normalization.
        """
        if self.correction_phase is None:
            raise ValueError("Correction pattern not loaded. Call load_correction_pattern() first.")

        y, x = np.indices((self.slm.slmY, self.slm.slmX))
        grating = np.mod(x, frequency_px) / frequency_px
        grating = normalize(grating)

        combo_phase = mod_1(grating + self.correction_phase) * self.mod_depth
        self.final_phase_mask = combo_phase.astype('uint8')

        self.slm.load_phase(self.final_phase_mask)
        print("Test grating with correction uploaded.")

