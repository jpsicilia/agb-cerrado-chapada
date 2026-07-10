# Aboveground Biomass (AGB) Estimation in the Cerrado — Chapada dos Veadeiros

Spatially explicit estimation of **aboveground biomass (AGB)** in the Chapada dos
Veadeiros National Park and its buffer zone (~11,935 km²), integrating
**GEDI L4A** as the response variable with **SAR/optical fusion** predictors
(Sentinel-1, Sentinel-2, ALOS-2 PALSAR-2, SRTM), modeled with a
**Quantile Regression Forest (QRF)** and **Conformalized Quantile Regression (CQR)**
for calibrated uncertainty.

**Key contribution:** the product is not just the AGB map, but the map paired with
calibrated uncertainty per physiognomy, honest spatial validation, and an explicit
**Area of Applicability (AOA)** — indicating where the model is actually valid.

> Undergraduate thesis (TCC) — Geography, UNILA.
> Author: Jose Pablo Perez Cicilia · ORCID 0009-0000-0519-8149

---

## How to reproduce (from scratch, in 5 steps)

```bash
# 1. Clone and create the environment
git clone <repo-url> && cd agb-cerrado-chapada
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Authenticate with Google Earth Engine (once)
earthengine authenticate

# 3. (Data) The study area and layers are accessed via GEE in the notebooks.
#    See scripts/01_define_aoi.js for the study-area definition.

# 4. Review config/config.yaml (all parameters live there)

# 5. Run the pipeline by phases (numbered notebooks)
jupyter lab notebooks/
#    01_area_masks       -> define AOI + land-cover mask
#    02_gedi_filter      -> download and filter GEDI L4A footprints
#    03_predictors       -> compose S1/S2/ALOS-2/SRTM on the common grid
#    04_matching         -> extract 3x3 window -> training table
#    05_model            -> QRF + CQR + spatial partitions + block CV
#    06_maps_aoa         -> AGB map + uncertainty + AOA + validation
```

All project-specific parameters (area, dates, thresholds, quantiles) live in
`config/config.yaml`. No path or parameter is hardcoded in the code.

---

## Project structure

```
agb-cerrado-chapada/
├── README.md
├── requirements.txt          # pinned versions
├── pyproject.toml            # metadata + ruff/black/pytest
├── config/
│   └── config.yaml           # ALL study parameters
├── src/agb_cerrado/
│   ├── data.py               # GEE access: GEDI, Sentinel, ALOS, SRTM
│   ├── preprocessing.py      # masks, GEDI filter, thinning, common grid
│   ├── models.py             # QRF, CQR, spatial partitions, AOA
│   └── utils.py              # CRS, reprojection, config loader, logging
├── notebooks/                # 01..06, exploratory and documented
├── tests/                    # unit tests (pytest)
├── scripts/                  # standalone scripts (GEE AOI definition, exports)
├── data/{raw,interim,processed}/   # not versioned (see .gitignore)
└── results/                  # final maps and models
```

---

## Methodological pipeline (7 phases)

| Phase | What | Output |
|-------|------|--------|
| 0 | Reproducible setup | repo, config, environment |
| 1 | Area + masks | AOI + native-vegetation mask |
| 2 | Response variable | filtered GEDI L4A footprints (7 layers) + thinning |
| 3 | Predictors | S1/S2/ALOS-2/SRTM on the common 30 m grid |
| 4 | Matching | 3×3 window → training table |
| 5 | Model | QRF + CQR, 3 spatial partitions, block CV |
| 6 | Maps + validation | AGB + uncertainty + AOA + external validation |

### Key methodological decisions (already consolidated)

- **GEDI L4A** provides AGBD directly (Mg/ha); RH metrics are not used as predictors (avoids circularity).
- **Land-cover mask** applied to both input AND output: native vegetation only (rocky outcrops / rocky grasslands are kept, as they are native low-AGB Cerrado).
- **Three spatially disjoint partitions** (train/calibration/test) separated by a minimum distance, preserving the exchangeability that conformal prediction requires.
- **Final map** produced by the model trained on the full dataset; cross-validation assesses performance, it does not produce the map.
- **Conformal correction** estimated on the held-out calibration block and transferred to the production model.
- **AOA (Meyer & Pebesma, 2021)** delimits where the map is statistically valid; performance metrics are reported over the WHOLE validation (no cropping), and the AOA only delimits the product.

---

## Data sources

| Data | Source | Access |
|------|--------|--------|
| Protected-area boundary | WDPA (WCMC/WDPA/current/polygons) | via GEE |
| Land cover | MapBiomas Collection 9 | via GEE |
| GEDI L4A v2.1 | ORNL DAAC (DOI 10.3334/ORNLDAAC/2056) | via GEE / earthaccess |
| Sentinel-2 L2A | Copernicus / GEE | `COPERNICUS/S2_SR_HARMONIZED` |
| Sentinel-1 GRD | Copernicus / GEE | `COPERNICUS/S1_GRD` |
| ALOS-2 PALSAR-2 | JAXA / GEE | ScanSAR asset |
| SRTM | USGS / GEE | `USGS/SRTMGL1_003` |

---

## Reproducibility

- Pinned versions in `requirements.txt`
- Fixed seed (`random_seed: 42` in the config)
- Parameters centralized in YAML
- Sources documented with access date
- Idempotent notebooks; logic in tested `.py` modules

## License

MIT.
