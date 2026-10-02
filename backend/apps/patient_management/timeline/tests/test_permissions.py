"""
Patient Timeline permission tests.
"""

from __future__ import annotations


def test_timeline_permission_module_imports() -> None:
    """Ensure the permission package is importable."""

    import apps.patient_management.timeline.permissions  # noqa: F401
