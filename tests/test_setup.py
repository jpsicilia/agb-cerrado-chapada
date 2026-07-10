"""Base tests: config, seed, structure. Run with `pytest tests/ -v`."""

from pathlib import Path

from agb_cerrado.utils import load_config, set_global_seed


def test_config_loads():
    """The config.yaml must load and contain the expected sections."""
    cfg = load_config("config/config.yaml")
    for section in ["project", "study_area", "data", "gedi_filter", "model", "validation"]:
        assert section in cfg, f"Missing config section: {section}"


def test_config_key_params():
    """Key parameters must hold the values consolidated in the methodology."""
    cfg = load_config("config/config.yaml")
    assert cfg["study_area"]["buffer_m"] == 25000
    assert cfg["study_area"]["crs_projected"] == "EPSG:31983"
    assert cfg["study_area"]["area_km2_expected"] == 11934.66
    assert cfg["model"]["cqr_alpha"] == 0.10
    assert cfg["gedi_filter"]["slope_max_deg"] == 15
    assert cfg["random_seed"] == 42


def test_landcover_classes_disjoint():
    """Keep and drop classes must not overlap."""
    cfg = load_config("config/config.yaml")
    keep = set(cfg["data"]["landcover_keep_classes"])
    drop = set(cfg["data"]["landcover_drop_classes"])
    assert keep.isdisjoint(drop), "keep/drop classes overlap!"


def test_seed_runs():
    """set_global_seed must not raise."""
    set_global_seed(42)


def test_project_structure():
    """Essential project folders must exist."""
    for d in ["src/agb_cerrado", "config", "notebooks", "tests", "data", "results"]:
        assert Path(d).exists(), f"Missing folder: {d}"
