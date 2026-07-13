"""Data access: Earth Engine, GEDI L4A, Sentinel-1/2, ALOS-2, SRTM.

Each function is an isolated, testable block. None does heavy processing
inline — they only return GEE collections/objects to be composed downstream.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def init_gee(project: str) -> None:
    """Initialize Earth Engine with the user's project.

    Args:
        project: GEE project ID (e.g. 'alert-result-474012-g5').

    Note:
        Requires a prior `earthengine authenticate` (once per machine).
    """
    import ee

    ee.Initialize(project=project)
    logger.info("Earth Engine initialized (project=%s)", project)


def load_study_area(clip_bbox: list[float], filter_name: str, buffer_m: float):
    """Build the AOI from WDPA: clip to Goias and apply the buffer.

    Replicates scripts/01_define_aoi.js. The buffer is applied in meters.
    The result must be ~11,934.66 km2 (control number).

    Args:
        clip_bbox: Auxiliary clipping rectangle [W, S, E, N].
        filter_name: Value for the stringContains filter on NAME.
        buffer_m: Buffer radius in meters.

    Returns:
        ee.Geometry of the study area (polygon + buffer).
    """
    import ee

    wdpa = ee.FeatureCollection("WCMC/WDPA/current/polygons")
    region = ee.Geometry.Rectangle(clip_bbox)
    parks = (wdpa
             .filter(ee.Filter.stringContains("NAME", filter_name))
             .filterBounds(region))
    aoi = (parks.geometry()
           .intersection(region, 100)   # clip to Goias (maxError = 100 m)
           .buffer(buffer_m))
    logger.info("AOI built (buffer=%d m)", buffer_m)
    return aoi


def verify_area(aoi, expected_km2: float, tolerance: float = 0.05) -> float:
    """Verify the AOI area against the control number.

    Args:
        aoi: Study-area geometry.
        expected_km2: Expected area in km2 (control number, ~11934.66).
        tolerance: Allowed relative deviation (default 5%).

    Returns:
        The computed area in km2.

    Raises:
        ValueError: if the area deviates more than `tolerance` from expected.
    """
    area_km2 = aoi.area(100).divide(1e6).getInfo()
    deviation = abs(area_km2 - expected_km2) / expected_km2
    if deviation > tolerance:
        raise ValueError(
            f"AOI area {area_km2:.2f} km2 deviates {deviation:.1%} from "
            f"expected {expected_km2:.2f} km2. Check the definition."
        )
    logger.info("AOI area verified: %.2f km2", area_km2)
    return area_km2


def load_mapbiomas_mask(aoi, keep_classes: list[int], year: int = 2021):
    """Load the land-cover mask (MapBiomas), keeping only native vegetation.

    Args:
        aoi: Study-area geometry (ee.Geometry).
        keep_classes: MapBiomas classes to keep (native vegetation).
        year: MapBiomas collection year (default 2021, central year of the
            2020-2022 working period).

    Returns:
        Binary ee.Image (1 = native vegetation, 0 = drop), clipped to the AOI.
    """
    import ee

    asset = (
        "projects/mapbiomas-public/assets/brazil/lulc/"
        "collection9/mapbiomas_collection90_integration_v1"
    )
    band = f"classification_{year}"
    mask = (ee.Image(asset)
            .select(band)
            .remap(keep_classes, [1] * len(keep_classes), 0)
            .clip(aoi))
    logger.info("Native-vegetation mask built (MapBiomas %d)", year)
    return mask


def load_gedi_l4a(aoi, periods: list[list[str]]):
    """Load GEDI L4A footprints for the AOI over the valid periods (pre/post gap).

    Args:
        aoi: Study-area geometry (ee.Geometry).
        periods: List of [start, end] excluding the hibernation gap.

    Returns:
        ee.FeatureCollection of footprints with AGBD and quality flags.
    """
    raise NotImplementedError("Phase 2: implement GEDI L4A access.")


def load_predictors(aoi, cfg: dict[str, Any]):
    """Load and compose predictors (S1, S2, ALOS-2, SRTM) on the common grid.

    Args:
        aoi: Study-area geometry.
        cfg: Config with assets and the compositing time window.

    Returns:
        Multiband ee.Image with all predictors aligned at 30 m.
    """
    raise NotImplementedError("Phase 3: implement predictor compositing.")
