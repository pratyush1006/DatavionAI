"""
Patient Timeline selector tests.
"""

from __future__ import annotations


def test_timeline_selector_module_imports() -> None:
    """Ensure the selector package is importable."""

    import apps.patient_management.timeline.selectors  # noqa: F401
