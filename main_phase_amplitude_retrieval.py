"""
main_phase_amplitude_retrieval.py

Main entry point for phase and amplitude retrieval using a spatial light modulator (SLM).
This script controls the sequence of measurements, including optional correction application,
and outputs correction maps.

Author: Dimitrios Karanikolopoulos
Co-author: John Balas (Institute of Polaritonics, Westlake University, Hangzhou)
"""

import os
from function_scripts.phasamp_class import PhaseAmplitudeRetrieval
from slm.slm_hamamatsu import SlmDisplay
from orca.orca_autonoma import LiveHamamatsu
from peripheral_instruments.thorlabs_shutter import Shutter

# === USER CONFIGURATION ===
measure_slm_phase = True
flat_beam_prof = True
donut_check = False
default_profile = False
rm_fringe = True
use_previous_correction = False
plot_in_lOOp = False
save_loop_data = False

# === HARDWARE SETUP ===
slm = SlmDisplay()
slm.connect()

cam = LiveHamamatsu(
    initCam=True,
    came_numb=0,
    trig_mODe=2,
    exposure=0.2  # seconds
)

shutter = Shutter()

# === RUN MEASUREMENT ===
phasamp = PhaseAmplitudeRetrieval(
    slm=slm,
    camera=cam,
    shutter=shutter,
    flat_beam_prof=flat_beam_prof,
    default_profile=default_profile,
    rm_fringe=rm_fringe,
    use_previous_correction=use_previous_correction,
    plot_in_loop=plot_in_lOOp,
    save_loop_data=save_loop_data
)

if measure_slm_phase:
    phasamp.measure_slm_wavefront()

if donut_check:
    phasamp.lg_donut_test()

print("✅ Main measurement script completed.")
