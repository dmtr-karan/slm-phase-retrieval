# slm-phase-retrieval

![CI](https://github.com/dmtr-karan/slm-phase-retrieval/actions/workflows/python-install.yml/badge.svg)

Python-based phase and amplitude retrieval for LCOS-SLM characterization and calibration, adapted for Hamamatsu X15213 and related lab setups.

---

## ✨ Overview

This repository implements an optical wavefront retrieval algorithm based on interferometric grating patch methods. It enables correction of SLM-induced and optical aberrations for high-fidelity phase holography.

Adapted from:

- Phillip Zupancic (https://doi.org/10.1364/OE.24.013881)
- Schroff et al., *Scientific Reports* (https://doi.org/10.1038/s41598-023-30296-6)
- [Original `hologradpy` implementation](https://github.com/paul-schroff/hologradpy)

This version is fully adapted to a USB-connected LCOS SLM (Hamamatsu X15213) and integrates directly with a Hamamatsu ORCA camera and Thorlabs SC10 shutter.

---

## 📦 Repo Structure

```
slm-phase-retrieval/
├── main_phase_amplitude_retrieval.py        # Top-level phase retrieval routine

├── slm/
│   ├── slm_hamamatsu.py                     # Hamamatsu SLM USB control (X15213 LCOS)
│   ├── demo_slm_upload_grating_and_correction.py  # Phase upload demonstration
│   └── corr_patties/
│       └── CAL_LSH0803420_750nm.bmp         # Manufacturer correction pattern

├── orca/
│   └── orca_camera.py                       # ORCA Flash v3 USB interface

├── peripheral_instruments/
│   └── thorlabs_shutter.py                  # USB control for SC10 shutter

├── function_scripts/
│   ├── slmphase.py                          # Main retrieval class
│   ├── phase_gen.py                         # Phase pattern generation (gratings, corrections)
│   ├── fitting.py                           # Sine and Gaussian fitting routines
│   └── helpers.py                           # Normalization, meshgrid, utilities

├── tests/
│   ├── test_correction_by_lg.py             # Example LG-beam result viewer
│   ├── slm_speed_test.py                    # SLM phase upload benchmark
│   └── orca_speed_test_vs_cam_PrepMode.py   # Acquisition speed test

├── requirements.txt
├── LICENSE
└── README.md
```


---

## ⚙️ Hardware Requirements

- **SLM**: Hamamatsu X15213 (LCOS, USB interface)
- **Camera**: Hamamatsu ORCA Flash v3
- **Shutter**: Thorlabs SC10 (serial over USB)

---

## 🚀 Quick Demo

The script `slm/demo_slm_upload_grating_and_correction.py` demonstrates:

- Loading a correction phase pattern from a `.bmp`
- Generating a basic grating
- Uploading the combined phase to the SLM

This serves as a proof of working USB control and calibration-phase logic.

---

## 📐 Main Retrieval Logic

The core functionality is implemented in `function_scripts/slmphase.py` and:

1. Displays structured gratings on the SLM
2. Measures interferograms via a known patch structure
3. Computes relative phase across the SLM
4. Optionally fits amplitude (from arm interference)
5. Stores correction maps and Gaussian fits

Backgrounds are measured and removed either by shutter or by using a flat-phase mask with suppressed diffraction.

---

## 🔭 Future Work

Planned improvements include:

- Adding Python type annotations across the codebase
- Inlining phase generation logic into `slmphase.py`
- Including real LG donut test result in `tests/`
- Replacing placeholder phase_gen logic with full pattern generation code
- Adding unit tests and live examples
- Optional PyQt GUI interface (SLM/Camera control)

---

## 👤 Credits

Developed and maintained by **Dimitrios Karanikolopoulos**.

Calibration BMP and correction methodology originally based on manufacturer data and experimental wavefront flattening work.

SLM driver interface adapted from C++/DLL SDK using `cffi`.

Collaborative input on hardware abstraction by **John Balas** (International Center of Polaritonics, Westlake University, Hangzhou).