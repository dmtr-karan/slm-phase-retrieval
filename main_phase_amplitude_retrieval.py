"""
Main script for phase and amplitude retrieval using fringe interferometry
to calibrate a Hamamatsu LCOS-SLM. Requires a camera, shutter, and SLM driver.

Author: Dimitrios Karanikolopoulos
Co-author: John Balas (International Center of Polaritonics, Westlake University, Hangzhou)
"""

from function_scripts.phasamp_class import PhaseAmplitudeRetrieval
from orca.orca_camera import LiveHamamatsu
from slm.slm_hamamatsu import SlmHamamatsu
from peripheral_instruments.thorlabs_shutter import Shutter

# =============================
# User Configuration Flags
# =============================

measure_slm_phase = True           # Step 1: Measure SLM phase distortion
donut_check = False                # Step 2: Verify correction using LG-mode phase

# Optional control flags
flat_beam_prof = True              # Assume flat beam across SLM (skip intensity weighting)
default_profile = False            # Use synthetic Gaussian weighting
rm_fringe = True                   # Remove background by blank phase (no shutter)
use_previous_correction = False    # Apply previously saved correction
plot_in_loop = False               # Plot interferogram during iteration
save_loop_data = False             # Save all phase reconstruction data

# =============================
# Initialize Devices
# =============================

print("\n--- INITIALIZING INSTRUMENTS ---")
slm = SlmHamamatsu()
slm.connect()

cam = LiveHamamatsu(
    exposure=0.005,
    initCam=True,
    came_numb=0,
    trig_mODe=1
)

shut = Shutter()

# =============================
# Step 1: Measure SLM Phase Distortion
# =============================

if measure_slm_phase:
    print("\n--- MEASURING SLM PHASE ---")
    phaz = PhaseAmplitudeRetrieval(
        slm_disp_obj=slm,
        cam_obj=cam,
        shut_obj=shut,
        aperture_number=8,
        aperture_width=64,
        exp_time=0.005,
        num_frames=3,
        roi_min_x=256,
        roi_min_y=256,
        roi_n=512,
        plot_within=plot_in_loop,
        sv_data=save_loop_data,
        rm_fringes=rm_fringe,
        use_correction=use_previous_correction,
        flat_beam_prof=flat_beam_prof,
        default_profile=default_profile
    )
    phaz.measure_slm_wavefront()

# =============================
# Step 2: LG-Mode Donut Test (Optional)
# =============================

if donut_check:
    print("\n--- VALIDATING WITH DONUT PHASE ---")
    phaz.test_correction_by_lg_mode()

# =============================
# End
# =============================
print("\n Phase calibration sequence complete.")
