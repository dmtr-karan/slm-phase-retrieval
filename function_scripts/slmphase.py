"""
Phase and amplitude retrieval class adapted from:
- Phillip Zupancic (https://doi.org/10.1364/OE.24.013881)
- Schroff et al., Scientific Reports (https://doi.org/10.1038/s41598-023-30296-6)
- Refactored for LCOS-SLM calibration with custom camera and shutter integration.

Author: Dimitrios Karanikolopoulos
"""

import os
import time
import copy
import numpy as np
import matplotlib.pyplot as plt

import function_scripts.fitting as ft
from function_scripts.helpers import meshgrid_slm, closest_arr, make_grid

# Dummy phase generator placeholder (used until full logic is ported)
class DummyPhasor:
    """
    Stub class to emulate phase generation logic.
    To be replaced with complete routines from slm_hamamatsu.py.
    """
    def __init__(self):
        self.patch = None
        self.final_phase = None
        self.correction_path = None
        self.which_phases = {}

    def linear_grating(self):
        pass

    def make_full_slm_array(self):
        self.final_phase = np.zeros((1024, 1272), dtype=np.uint8)


phase_gen = DummyPhasor()


class PhaseAmplitudeRetriever:
    """
    The main class for retrieving the phase and intensity profile of the SLM wavefront.
    """

    def __init__(self, data_path, wavelength=752e-9):
        self.data_path = data_path
        self.wavelength = wavelength
        self.k = 2 * np.pi / self.wavelength
        self.the_path = data_path
        self.use_prev_dphi = False
        self.bckgrnd_full = None

    def measure_slm_wavefront(
        self,
        slm_disp_obj,
        cam_obj,
        shutter_obj,
        aperture_number=20,
        aperture_width=64,
        exposure_time=310 / 1000,
        num_frames=10,
        roi_min_x=4,
        roi_min_y=4,
        roi_n=12,
        plot_within=False,
        sv_data=False,
        rm_fringes=True,
        use_correction=False,
    ):
        """
        Main function to retrieve the SLM wavefront by projecting small aperture gratings
        and fitting the resulting interferograms.

        Saves:
            dphi: retrieved relative phase
            dphi_err: error from sine fitting
            i_fit: intensity from amplitude product of fits
        """

        self.use_prev_dphi = use_correction
        timestamp = time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())
        save_dir = os.path.join(self.data_path, f"{timestamp}_wavefront")
        os.makedirs(save_dir)

        # Setup
        res_y, res_x = slm_disp_obj.res
        npix = min(res_y, res_x)
        slm_pitch = slm_disp_obj.pitch
        k = self.k
        fl = 0.3  # Focal length (m)

        # Create phase mask for measurement
        phase_gen.correction_path = self.the_path
        phase_gen.which_phases = {
            "grating": True,
            "patch": False,
            "corr_patt": True,
            "corr_phase": use_correction,
        }
        phase_gen.linear_grating()
        phase_gen.make_full_slm_array()
        slm_phase = phase_gen.final_phase

        # Get aperture coordinates
        slm_idx = self._get_aperture_indices(
            aperture_number, aperture_number, 0, npix, 0, npix, aperture_width, aperture_width
        )
        roi_idxs = np.reshape(np.arange(aperture_number**2), (aperture_number, aperture_number))
        roi_idxs = roi_idxs[roi_min_x : roi_min_x + roi_n, roi_min_y : roi_min_y + roi_n].flatten()
        n_centre = aperture_number**2 // 2 + aperture_number // 2 - 1

        # Capture background image
        print("Recording background...")
        if rm_fringes:
            phase_gen.which_phases = {
                "grating": False,
                "patch": False,
                "corr_patt": True,
                "corr_phase": use_correction,
            }
            phase_gen.make_full_slm_array()
            slm_disp_obj.load_phase(phase_gen.final_phase)
            shutter_obj.shutter_enable()
        else:
            shutter_obj.shutter_enable(False)

        cam_obj.exposure = exposure_time
        cam_obj.num = num_frames
        cam_obj.prep_acq()
        cam_obj.take_average_image(num_frames)
        bckgr = copy.deepcopy(cam_obj.last_frame)

        # Activate shutter
        shutter_obj.shutter_enable(True)

        # Initialize image stack
        img_stack = np.zeros((300, 300, roi_n**2))
        ph_central = np.zeros((res_y, res_x))
        ph_central[slm_idx[0][n_centre]:slm_idx[1][n_centre],
                   slm_idx[2][n_centre]:slm_idx[3][n_centre]] = \
            slm_phase[slm_idx[0][n_centre]:slm_idx[1][n_centre],
                      slm_idx[2][n_centre]:slm_idx[3][n_centre]]

        # Loop over apertures
        print("Starting measurement loop...")
        for i, idx in enumerate(roi_idxs):
            masked_phase = np.copy(ph_central)
            masked_phase[slm_idx[0][idx]:slm_idx[1][idx],
                         slm_idx[2][idx]:slm_idx[3][idx]] = \
                slm_phase[slm_idx[0][idx]:slm_idx[1][idx],
                          slm_idx[2][idx]:slm_phase[3][idx]]

            phase_gen.patch = masked_phase
            phase_gen.make_full_slm_array()
            slm_disp_obj.load_phase(phase_gen.final_phase)

            cam_obj.take_average_image(num_frames)
            img_stack[..., i] = cam_obj.last_frame - bckgr

            if plot_within:
                plt.imshow(img_stack[..., i], cmap='inferno')
                plt.title(f"Patch {i}")
                plt.colorbar()
                plt.pause(0.3)
                plt.clf()

        # Fit retrieved phase
        print("Fitting phase data...")
        fit_sine = ft.FitSine(fl, k)
        popt_sv = []

        x, y = make_grid(img_stack[..., 0], scale=cam_obj.pitch)
        x_data = np.vstack((x.ravel(), y.ravel()))

        for i, idx in enumerate(roi_idxs):
            dx = (slm_idx[2][idx] - slm_idx[2][n_centre]) * slm_pitch
            dy = (slm_idx[0][idx] - slm_idx[0][n_centre]) * slm_pitch
            fit_sine.set_dx_dy(dx, dy)

            a_guess = np.sqrt(np.max(img_stack[..., i])) / 2
            p0 = [0, a_guess, a_guess]
            bounds = ([-np.pi, 0, 0], [np.pi, 2 * a_guess, 2 * a_guess])
            popt, _ = ft.safe_fit(fit_sine.fit_sine, x_data, img_stack[..., i].ravel(), p0, bounds)
            popt_sv.append(popt)

        popt_sv = np.array(popt_sv)
        dphi = -popt_sv[:, 0].reshape(roi_n, roi_n)
        amp = np.abs(popt_sv[:, 1] * popt_sv[:, 2]).reshape(roi_n, roi_n)

        # Save results
        np.save(os.path.join(save_dir, "dphi.npy"), dphi)
        np.save(os.path.join(save_dir, "amplitude.npy"), amp)

        plt.imshow(dphi, cmap='magma')
        plt.title("Retrieved Phase Map")
        plt.colorbar()
        plt.savefig(os.path.join(save_dir, "phase_map.png"))
        plt.close()

        plt.imshow(amp, cmap='inferno')
        plt.title("Retrieved Intensity (a*b)")
        plt.colorbar()
        plt.savefig(os.path.join(save_dir, "intensity_map.png"))
        plt.close()

    def _get_aperture_indices(self, n_ap_x, n_ap_y, x_min, x_max, y_min, y_max, dx, dy):
        """
        Computes ROI pixel bounds for a grid of patches.
        """
        patch_start_x = [int(x_min + i * dx) for i in range(n_ap_x)]
        patch_end_x = [x + dx for x in patch_start_x]
        patch_start_y = [int(y_min + i * dy) for i in range(n_ap_y)]
        patch_end_y = [y + dy for y in patch_start_y]

        patch_top = []
        patch_bot = []
        patch_left = []
        patch_right = []

        for i in patch_start_y:
            for j in patch_start_x:
                patch_top.append(i)
                patch_bot.append(i + dy)
                patch_left.append(j)
                patch_right.append(j + dx)

        return patch_top, patch_bot, patch_left, patch_right
