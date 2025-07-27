# slm-phase-retrieval

![CI](https://github.com/dmtr-karan/slm-phase-retrieval/actions/workflows/python-install.yml/badge.svg)

This repository implements an optical phase and amplitude retrieval algorithm for **LCOS Spatial Light Modulators (SLMs)** using interferometric fringe analysis. It supports full system calibration using a **Hamamatsu SLM**, **Hamamatsu ORCA camera**, and **Thorlabs SC10 shutter**.

---

## 🧠 Purpose

The goal of this codebase is to retrieve the wavefront distortion across the SLM, including both:

- **Fixed distortions**: Residual manufacturing imperfections of the SLM (even after manufacturer’s correction mask)
- **Optical aberrations**: Introduced by the full experimental setup (lenses, alignment, beam quality)

The result is a spatially-resolved **phase correction map** that can be used in any downstream holography, beam shaping, or optical trapping application.

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

## 🧪 Hardware Used

| Device                | Model                        |
|----------------------|------------------------------|
| Spatial Light Modulator | Hamamatsu X15213 LCOS      |
| Camera               | Hamamatsu ORCA-Flash v3      |
| Shutter              | Thorlabs SC10                |

---

## 🚀 Quickstart: Retrieve Phase Map

```bash
python main_phase_amplitude_retrieval.py

All core parameters (grating configuration, region-of-interest size, exposure, etc.) are configured inside the script. Outputs include:

    dphi.npy – retrieved relative phase (can be used directly as a correction)

    amplitude.npy – intensity estimate from fringe amplitude

    PNG figures – phase + amplitude visualization

🧭 Demonstration: Load Grating + Correction

A standalone demonstration of uploading a horizontal grating and correction phase to the SLM is available here:

python slm/demo_slm_upload_grating_and_correction.py

This uses:

    Horizontal linear grating

    Correction phase from corr_patties/CAL_LSH0803420_750nm.bmp (manufacturer data)

    Modulation depth: 198 (optimized for 752 nm)

📖 Citations & Acknowledgments
Base Methodology

This work adapts algorithms and code originally published by:

    Phillip Zupancic et al. – Optics Express, 2016

    Schroff et al., Scientific Reports, 2023 – DOI: 10.1038/s41598-023-30296-6
    (see original repo: https://github.com/paul-schroff/hologradpy)

Code Authors

    Dimitrios Karanikolopoulos
    SLM integration, camera automation, phase logic

    John Balas (co-author, slm_hamamatsu.py)
    International Center of Polaritonics, Westlake University, Hangzhou

⚙️ Development

This repository is ready for GitHub Actions:

CI

Install dependencies:

pip install -r requirements.txt

📄 License

MIT License. See LICENSE.