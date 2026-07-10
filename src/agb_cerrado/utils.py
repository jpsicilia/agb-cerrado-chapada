"""General utilities: config loading, logging, and CRS transformations."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def load_config(config_path: Path | str = "config/config.yaml") -> dict[str, Any]:
    """Load the YAML configuration file.

    Args:
        config_path: Path to config.yaml.

    Returns:
        Dictionary with all project parameters.

    Example:
        >>> cfg = load_config()
        >>> cfg["study_area"]["buffer_m"]
        25000
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found at {config_path}")
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    logger.info("Config loaded from %s", config_path)
    return cfg


def set_global_seed(seed: int = 42) -> None:
    """Fix the global random seed for reproducibility.

    Args:
        seed: Seed value (default 42).
    """
    import random

    import numpy as np

    random.seed(seed)
    np.random.seed(seed)
    logger.info("Global seed set to %d", seed)


def reproject_geom_to_utm(geom, src_crs: str, utm_crs: str):
    """Reproject a geometry from a geographic CRS to UTM (meters).

    Needed because the 25 km buffer must be computed in meters, not degrees.

    Args:
        geom: Shapely geometry to reproject.
        src_crs: Source CRS (e.g. 'EPSG:4326').
        utm_crs: Target CRS in meters (e.g. 'EPSG:31983').

    Returns:
        Geometry reprojected to UTM.
    """
    from pyproj import Transformer
    from shapely.ops import transform

    transformer = Transformer.from_crs(src_crs, utm_crs, always_xy=True)
    logger.info("Reprojecting geometry: %s -> %s", src_crs, utm_crs)
    return transform(transformer.transform, geom)
