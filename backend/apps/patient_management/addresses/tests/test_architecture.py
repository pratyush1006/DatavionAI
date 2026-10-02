"""Address architecture contract."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_layers():
    for name in (
        "models",
        "selectors",
        "services",
        "policies",
        "permissions",
        "events",
        "workflows",
        "api",
    ):
        assert (ROOT / name).exists()


def test_geography_boundary():
    model = (ROOT / "models" / "address.py").read_text(encoding="utf-8")
    adapter = (ROOT / "services" / "geography.py").read_text(encoding="utf-8")
    assert '"geography.Country"' in model
    assert '"geography.AdministrativeRegion"' in model
    assert '"geography.City"' in model
    assert "geopy" not in model.lower()
    assert "nominatim" not in model.lower()
    assert "apps.platform.geography" in adapter


def test_protected_family_dependency_not_referenced():
    forbidden = "family" + "_members"
    current_test = Path(__file__).resolve()
    for path in ROOT.rglob("*.py"):
        if path.resolve() == current_test:
            continue
        assert forbidden not in path.read_text(encoding="utf-8").lower()
