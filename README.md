# slm-phase-retrieval: Phase & Amplitude Retrieval for SLM Correction

![CI](https://github.com/dmtr-karan/slm-phase-retrieval/actions/workflows/python-install.yml/badge.svg)

This repository implements a complete phase and amplitude correction pipeline for Spatial Light Modulators (SLMs), including device control, phase measurement, fringe analysis, and phase correction.

The workflow is based on adaptations of:

    Schroff et al., Scientific Reports, 2023
    Zurpaczik et al., Scientific Reports, 2021
    Source code adapted from https://github.com/paul-schroff/hologradpy

🧠 **Project Purpose**

The goal is to measure and correct intrinsic phase distortions introduced by LCOS-type SLMs by:

- Generating patch-based interferograms
- Fitting resulting fringe patterns to extract relative phase and intensity
- Constructing correction masks to apply during phase hologram generation
- Optionally validating phase recovery using LG-mode donut beams

📁 **Repository Structure**

slm-phase-retrieval/
├── main_phase_amplitude_retrieval.py         # Main script controlling phase correction process
├── slm/
│   ├── slm_hamamatsu.py                      # Hamamatsu SLM USB driver (X15213, LCOS)
│   ├── slm_upload_grating_and_correction.py  # Standalone demo: upload grating + correction to SLM
│   └── corr_patties/
│       └── CAL_LSH0803420_750nm.bmp          # Calibration correction pattern
├── orca/
│   └── orca_camera.py                        # Hamamatsu ORCA Flash v3 interface
├── peripheral_instruments/
│   └── thorlabs_shutter.py                   # SC10 shutter controller via USB
├── function_scripts/
│   ├── phasamp_class.py                      # Core logic for phase recovery
│   ├── helpers.py                            # Tools (normalization, meshgrids, unimod, etc.)
│   ├── patterns.py                           # Phase and intensity pattern generators
│   └── fitting.py                            # Curve fitting tools (e.g. Gaussian, cosine)
├── tests/
│   ├── test_correction_by_lg.py              # LG-mode donut validation (see example result)
│   ├── slm_speed_test.py                     # SLM phase upload timing benchmark
│   └── orca_speed_test_vs_cam_PrepMode.py    # Camera acquisition speed test
├── requirements.txt
├── LICENSE
└── README.md

🚀 **Quickstart: Measuring & Correcting SLM Phase**

The `main_phase_amplitude_retrieval.py` script handles full correction pipeline. Set the flags below as needed:

```python
measure_slm_phase = True           # Perform phase measurement using fringe analysis
flat_beam_prof = True              # Skip amplitude retrieval (assume flat beam profile)
donut_check = False                # Perform LG-mode donut test
default_profile = False            # Use Gaussian profile instead of measurement
rm_fringe = True                   # Blank phase used for fringe subtraction
use_previous_correction = False   # Reuse saved correction mask
plot_in_lOOp = False               # Enable live plotting during iterations
save_loop_data = False            # Save fringe data + plots during fitting
```

⚙️ **Equipment Supported**

| Device   | Model / Interface                |
|----------|----------------------------------|
| SLM      | Hamamatsu X15213 LCOS            |
| Camera   | Hamamatsu ORCA Flash v3          |
| Shutter  | Thorlabs SC10 (USB)              |

> Full control of each device is modularized in `slm/`, `orca/`, and `peripheral_instruments/`

📷 **SLM Upload Demo**

To demonstrate SLM usage and file-based correction phase:

```bash
python slm/slm_upload_grating_and_correction.py
```

It uploads a horizontal grating and calibration pattern from `slm/corr_patties/CAL_LSH0803420_750nm.bmp`.

📌 **Notes**

- All phases are normalized using `normalize(...)` then wrapped with `mod_1(...)`.
- Phase modulation depth is set to 198 (for 752 nm, as per manufacturer data).
- The unimod operation is handled via the `mod_1()` function in `helpers.py`.

🧑 **Author Information**

- Primary Author: Dimitrios Karanikolopoulos
- Co-Author (SLM driver): John Balas, Institute of Polaritonics, Westlake University, Hangzhou

---

## 🔧 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/dmtr-karan/slm-phase-retrieval.git
cd slm-phase-retrieval
pip install -r requirements.txt
```

Ensure camera drivers and SLM SDK are installed on your system (Hamamatsu ORCA, LCOS-SLM USB SDK).

---

## 🚀 Usage

To run a full phase + amplitude correction:

```bash
python main_phase_amplitude_retrieval.py
```

To upload a horizontal grating + correction to the SLM:

```bash
python slm/slm_upload_grating_and_correction.py
```

Use flags inside `main_phase_amplitude_retrieval.py` to:
- Enable/disable fringe measurement
- Toggle default beam profiles
- Skip or apply existing correction

Hardware modules:
- `SLM`: `slm/slm_hamamatsu.py`
- `Camera`: `orca/orca_camera.py`
- `Shutter`: `peripheral_instruments/thorlabs_shutter.py`

---

## 📄 License

This project is licensed under the terms of the MIT License. See `LICENSE` for details.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Please see `CONTRIBUTING.md`.

---

## 💬 Code of Conduct

By participating in this project, you agree to abide by the `CODE_OF_CONDUCT.md`.
