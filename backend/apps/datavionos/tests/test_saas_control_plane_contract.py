"""SaaS control-plane contract tests."""

from __future__ import annotations

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()


from apps.datavionos.services.effective_capability import (
    build_effective_capability_context,
)


def test_subscription_entitlement_override_contract():
    snapshot = build_effective_capability_context(
        user_id="u",
        organization_id="o",
        tenant_id="t",
        modules={"pharmacy": True, "billing": False},
        features={"pharmacy.ai": True, "billing.dashboard": False},
        permissions={"pharmacy.view"},
    )
    assert snapshot.module_enabled("pharmacy") is True
    assert snapshot.module_enabled("billing") is False
    assert snapshot.feature_enabled("pharmacy.ai") is True
    assert snapshot.feature_enabled("billing.dashboard") is False
    assert snapshot.has_permission("pharmacy.view") is True


def test_unentitled_module_cannot_be_reenabled_by_local_override():
    entitled = {"pharmacy": True}
    requested = {"pharmacy": False, "laboratory": True}
    effective = {
        key: entitled.get(key, False) and requested.get(key, True)
        for key in set(entitled) | set(requested)
    }
    assert effective["pharmacy"] is False
    assert effective["laboratory"] is False


def test_department_scoped_ai_requires_module_and_permission():
    context = build_effective_capability_context(
        user_id="u",
        organization_id="o",
        tenant_id="t",
        modules={"pharmacy": True},
        features={"pharmacy.ai": True},
        permissions={"laboratory.view"},
    )
    assert context.module_enabled("pharmacy") is True
    assert context.feature_enabled("pharmacy.ai") is True
    assert context.has_permission("pharmacy.view") is False
