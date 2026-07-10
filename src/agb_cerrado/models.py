"""Modeling: QRF, conformal (CQR), spatial partitions, validation and AOA.

Implements the methodological core: Quantile Regression Forest with
Conformalized Quantile Regression for calibrated uncertainty, with spatially
disjoint partitioning and the Area of Applicability.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


def spatial_partition(table, cfg_val: dict[str, Any]):
    """Partition data into spatially disjoint train/calibration/test sets.

    The three blocks are separated by a minimum distance from one another,
    preserving the exchangeability that conformal prediction requires.

    Args:
        table: DataFrame with coordinates + predictors + AGBD.
        cfg_val: `validation` section of the config.

    Returns:
        Tuple (train, calibration, test) that are spatially separated.
    """
    raise NotImplementedError("Phase 5: implement spatial partition.")


def train_qrf(x_train: np.ndarray, y_train: np.ndarray, cfg_model: dict[str, Any]):
    """Train the Quantile Regression Forest.

    Args:
        x_train: Predictor matrix (n_samples, n_features).
        y_train: Observed AGBD vector (n_samples,).
        cfg_model: `model` section of the config (n_estimators, quantiles, etc.).

    Returns:
        Trained QRF model.
    """
    logger.info("Training QRF with %d samples", len(y_train))
    raise NotImplementedError("Phase 5: implement QRF training.")


def calibrate_conformal(model, x_calib: np.ndarray, y_calib: np.ndarray, alpha: float):
    """Calibrate the intervals via Conformalized Quantile Regression (CQR).

    Estimates the conformal correction factor on the held-out calibration block;
    this factor is then transferred to the production model (trained on all data).

    Args:
        model: QRF trained on the training block.
        x_calib: Predictors of the calibration block.
        y_calib: AGBD of the calibration block.
        alpha: Miscoverage level (0.10 = 90% nominal coverage).

    Returns:
        Conformal correction factor (to be applied to the intervals).
    """
    raise NotImplementedError("Phase 5: implement CQR calibration.")


def spatial_block_cv(table, cfg_val: dict[str, Any]):
    """Spatial block cross-validation (evaluates performance, does not produce the map).

    Args:
        table: Full DataFrame with coordinates + predictors + AGBD.
        cfg_val: `validation` section of the config.

    Returns:
        Dict of metrics (R2, RMSE, empirical coverage) per fold and aggregated.
    """
    raise NotImplementedError("Phase 5: implement spatial block CV.")


def compute_aoa(model, x_train: np.ndarray, x_map: np.ndarray):
    """Compute the Area of Applicability (Meyer & Pebesma, 2021).

    Delimits where predictor conditions fall within the training domain.
    Used ONLY to delimit the final product — never to crop metrics.

    Args:
        model: Trained QRF (for variable importance).
        x_train: Predictors of the training set.
        x_map: Predictors of all pixels in the wall-to-wall map.

    Returns:
        Binary applicability mask + dissimilarity index (DI).
    """
    raise NotImplementedError("Phase 6: implement AOA.")
