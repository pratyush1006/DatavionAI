from __future__ import annotations

"""Architecture tests for Revenue Cycle Coding."""

from pathlib import Path


def test_coding_has_no_module_package_collisions():
    """Ensure the rebuilt Coding package has no file/package collisions."""

    app_path = Path(__file__).resolve().parents[1]

    pairs = (
        "events",
        "permissions",
        "policies",
        "selectors",
        "services",
        "workflows",
    )

    for name in pairs:
        assert not ((app_path / f"{name}.py").exists() and (app_path / name).is_dir())

    assert not (
        (app_path / "api" / "views.py").exists()
        and (app_path / "api" / "views").is_dir()
    )
    assert not (
        (app_path / "api" / "serializers.py").exists()
        and (app_path / "api" / "serializers").is_dir()
    )


def test_canonical_patient_import_is_used():
    """Ensure Coding references the canonical Patient model."""

    model_source = (
        Path(__file__).resolve().parents[1] / "models" / "coding_record.py"
    ).read_text(encoding="utf-8")

    assert "apps.patient_management.patients.models import Patient" in model_source


__all__ = (
    "test_canonical_patient_import_is_used",
    "test_coding_has_no_module_package_collisions",
)
