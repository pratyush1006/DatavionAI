"""
Patient Timeline API tests.
"""

from __future__ import annotations


def test_timeline_api_module_imports() -> None:
    """Ensure the API package is importable."""

    import apps.patient_management.timeline.api  # noqa: F401
