# slm/slm_hamamatsu.py

import os
import time
import glob
import numpy as np
from PIL import Image
from cffi import FFI

from function_scripts.helpers import mod_1, normalize

__author__ = "Dimitrios Karanikolopoulos"
__coauthor__ = "John Balas (International Center of Polaritonics, Westlake University, Hangzhou)"


class SlmHamamatsu:
    """
    Python interface for controlling Hamamatsu X15213 LCOS-SLM via USB and DLL.

    Loads calibration phase (BMP) and generates custom gratings. Designed for
    phase mask generation and SLM correction in research-grade setups.
    """

    def __init__(self):
        # SLM characteristics
        self.slmX = 1272
        self.slmY = 1024
        self.res = [self.slmY, self.slmX]
        self.pitch = 12.5e-6
        self.slm_size = self.pitch * np.asarray(self.res)

        # Phase modulation depth (uint8 range, specific to wavelength)
        self.mod_depth = 198  # Value for 752 nm per manufacturer spec

        # Final phase image (uint8)
        self.final_phase = np.zeros((self.slmY, self.slmX), dtype=np.uint8)

        # SLM driver
        self.ffi = FFI()
        self.slmffi = None
        self.bID = []
        self._load_dll()

    def _load_dll(self):
        cur_path = os.getcwd()
        if "tests" in cur_path:
            cur_path = cur_path.replace("\\tests", "")
        slm_path = os.path.join(cur_path, "slm", "hpkSLMdaLV_stdcall_64bit")
        os.environ['PATH'] = slm_path + os.pathsep + os.environ.get('PATH', '')
        os.add_dll_directory(slm_path)

        dll_path = os.path.join(slm_path, "hpkSLMdaLV.dll")
        header_path = os.path.join(slm_path, "hpkSLMdaLVt.h")

        self.slmffi = self.ffi.dlopen(dll_path)
        with open(header_path, "r") as header_file:
            self.ffi.cdef(header_file.read())

    def connect(self) -> int:
        """
        Open communication with the SLM device.

        Returns:
            int: Board ID (bID) of the connected SLM.
        """
        bIDList = self.ffi.new('uint8_t[10]')
        self.slmffi.Open_Dev(bIDList, 10)
        self.bID = bIDList[0]
        print(f"SLM connected with bID: {self.bID}")
        return self.bID

    def check_temp(self) -> tuple[float, float]:
        """
        Read temperatures of SLM head and control board.

        Returns:
            tuple: (head_temp, control_board_temp)
        """
        bID = self.ffi.cast('uint8_t', self.bID)
        HeadTemp = self.ffi.new('double *')
        CBTemp = self.ffi.new('double *')
        self.slmffi.Check_Temp(bID, HeadTemp, CBTemp)
        return HeadTemp[0], CBTemp[0]

    def load_phase(self, image: np.ndarray) -> None:
        """
        Upload 2D phase pattern (uint8) to the SLM.

        Args:
            image (np.ndarray): Phase array, values in [0, 255].
        """
        image = image.astype(np.uint8).flatten().tolist()
        array_sz = self.ffi.cast('int32_t', self.slmX * self.slmY)
        array_in = self.ffi.new(f'uint8_t [{self.slmX * self.slmY}]', image)
        self.slmffi.Write_FMemArray(
            self.ffi.cast('uint8_t', self.bID),
            array_in,
            array_sz,
            self.ffi.cast('uint32_t', self.slmX),
            self.ffi.cast('uint32_t', self.slmY),
            self.ffi.cast('uint32_t', 0)
        )
        time.sleep(0.1)

    def close(self) -> None:
        """Close connection to SLM."""
        self.slmffi.Close_Dev(self.bID, 10)
        print("SLM connection closed.")

    def generate_horizontal_grating(self, diviX=16) -> np.ndarray:
        """
        Create a horizontal grating pattern by modulating over X.

        Args:
            diviX (int): Grating period (in pixels).

        Returns:
            np.ndarray: 2D normalized grating phase in [0,1].
        """
        x = np.linspace(0, self.slmX - 1, self.slmX)
        grating_line = np.mod(np.floor(x), diviX) / diviX
        grating = np.tile(grating_line, (self.slmY, 1))
        return normalize(grating)

    def load_correction_pattern(self) -> np.ndarray:
        """
        Load correction phase pattern from .bmp file.

        Returns:
            np.ndarray: Normalized correction phase pattern.
        """
        current_path = os.getcwd()
        if "tests" in current_path:
            current_path = current_path.replace("\\tests", "")
        search_path = os.path.join(current_path, "slm", "correction_patterns", "CAL_LSH0803420_750nm.bmp")
        bmp_files = glob.glob(search_path)

        if not bmp_files:
            print("Correction pattern BMP not found.")
            return np.zeros((self.slmY, self.slmX))

        with Image.open(bmp_files[0]) as img:
            correction = np.asarray(img, dtype=np.uint16)
        return normalize(correction)

    def combine_and_upload_phase(self):
        """
        Combine grating + correction pattern, mod 1, apply modulation depth, and upload to SLM.
        """
        grating = self.generate_horizontal_grating()
        correction = self.load_correction_pattern()
        phased = mod_1(grating + correction) * self.mod_depth
        self.final_phase = phased.astype(np.uint8)
        self.load_phase(self.final_phase)

    @property
    def meshgrid_slm(self):
        """
        Return meshgrid of SLM in meters.

        Returns:
            Tuple[np.ndarray, np.ndarray]: X and Y meshgrids
        """
        x = np.arange(-self.slm_size[0] / 2, self.slm_size[0] / 2, self.pitch)
        return np.meshgrid(x, x)
