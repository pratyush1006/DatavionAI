"""AI API routing and health tests."""

from __future__ import annotations

from django.urls import resolve


def test_health_route_resolves():
    match = resolve("/api/ai/health/")
    assert match.url_name == "ai-health"
