"""Architecture tests for Charge Capture."""

from __future__ import annotations

from pathlib import Path

__all__ = ("test_root_urls_exists", "test_no_legacy_patient_imports")


ROOT = Path(__file__).resolve().parents[1]


def test_root_urls_exists() -> None:
    """Ensure the bounded context exposes its root URL configuration."""

    assert (ROOT / "urls.py").is_file()


def test_no_legacy_patient_imports() -> None:
    """Ensure Charge Capture references the canonical Patient model only."""

    for path in ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "apps.clinical.patients" not in text
