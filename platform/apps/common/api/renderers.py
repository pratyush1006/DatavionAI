"""
Reusable API renderers.

Datavion currently uses the default DRF JSON renderer.
Custom renderers should only be added when a genuine
cross-cutting requirement exists.
"""

from rest_framework.renderers import JSONRenderer

__all__ = [
    "JSONRenderer",
]
