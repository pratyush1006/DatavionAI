"""
Reusable API renderers.

This module provides a centralized import location for the
renderers used across the Datavion AI platform.

Datavion currently uses DRF's default JSON renderer.
Custom renderers should only be introduced when a genuine
cross-cutting requirement exists.
"""

from __future__ import annotations

from rest_framework.renderers import JSONRenderer

__all__ = [
    "JSONRenderer",
]
