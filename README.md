# slm-phase-retrieval

![CI](https://github.com/dmtr-karan/slm-phase-retrieval/actions/workflows/python-install.yml/badge.svg)


Python code for phase and amplitude retrieval on a Spatial Light Modulator (SLM), adapted and expanded from the methods in:

- Zupancic et al., *Optics Express*, 2016 — [https://doi.org/10.1364/OE.24.013881](https://doi.org/10.1364/OE.24.013881)
- Schroff et al., *Scientific Reports*, 2023 — [https://doi.org/10.1038/s41598-023-30296-6](https://doi.org/10.1038/s41598-023-30296-6)
- Based on code from [hologradpy](https://github.com/paul-schroff/hologradpy)

This repository calibrates the phase distortion of an SLM by displaying a sequence of local interferometric patches, analyzing the resulting interference patterns, and computing a correction mask for optical aberrations.

---

## 📌 Features

- Compatible with Hamamatsu X15213 LCOS-SLM (via USB DLL)
- Interfaced with Hamamatsu ORCA Flash v3 camera
- Uses manufacturer-supplied correction pattern + optionally retrieved wavefront correction
- Optional background removal via shutter or blank SLM phase
- 2D sinusoidal fringe fitting for high-resolution phase extraction
- Gaussian fitting for reconstructed intensity profiles

---

## 🧠 Method Overview

1. **SLM Patch Illumination**: small phase apertures are applied across the SLM surface.
2. **Interference Recording**: camera captures fringe patterns from signal + reference patches.
3. **Background Removal**: either using a shutter or applying a blank phase.
4. **Fringe Fitting**: cosine-based fits recover relative phase and amplitude.
5. **Correction Mask Construction**: recovered phase is used as a correction.

---

## 🧪 Structure
