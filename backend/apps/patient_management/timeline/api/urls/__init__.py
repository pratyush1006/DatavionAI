"""
Patient Timeline API URL package.
"""

from __future__ import annotations

from django.urls import URLPattern, URLResolver

__all__ = ()
# DatavionOS canonical URLConf cycle bridge.
# The nested URLConf already contains the canonical route definitions.
# Publish a placeholder before importing it because the nested module
# imports parent urlpatterns during module initialization.
urlpatterns: list[URLPattern | URLResolver] = []
from .timeline import urlpatterns as _canonical_urlpatterns

urlpatterns = _canonical_urlpatterns
del _canonical_urlpatterns
