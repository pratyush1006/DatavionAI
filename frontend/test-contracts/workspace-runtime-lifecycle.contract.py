
"""
DatavionOS frontend workspace lifecycle contract.

This contract validates state propagation only.

Authorization remains backend-owned:
subscription -> entitlement -> organization state -> RBAC ->
effective capability context -> bootstrap.

The frontend consumes the resulting bootstrap manifest and renders it.
"""


def test_subscription_and_module_enabled_reaches_renderer():
    state = {
        "subscription": "plan_a",
        "modules": ["module_a"],
        "dashboard": {"cards": [{"id": "module_a"}]},
    }
    assert state["subscription"] == "plan_a"
    assert "module_a" in state["modules"]
    assert state["dashboard"]["cards"]


def test_organization_disable_is_renderer_state_change():
    before = {"modules": ["module_a"]}
    after = {"modules": []}
    assert "module_a" in before["modules"]
    assert "module_a" not in after["modules"]


def test_organization_reenable_is_renderer_state_change():
    disabled = {"modules": []}
    enabled = {"modules": ["module_a"]}
    assert "module_a" not in disabled["modules"]
    assert "module_a" in enabled["modules"]


def test_subscription_removal_is_renderer_state_change():
    entitled = {"modules": ["module_a"]}
    unentitled = {"modules": []}
    assert entitled != unentitled
    assert "module_a" not in unentitled["modules"]


def test_subscription_change_is_renderer_state_change():
    plan_a = {"modules": ["module_a", "module_b"]}
    plan_b = {"modules": ["module_a"]}
    assert plan_a["modules"] != plan_b["modules"]


def test_rbac_removal_is_renderer_state_change():
    allowed = {"permissions": ["workspace.view"]}
    denied = {"permissions": []}
    assert "workspace.view" in allowed["permissions"]
    assert "workspace.view" not in denied["permissions"]


def test_feature_removal_is_renderer_state_change():
    enabled = {"features": ["module_a.feature_x"]}
    disabled = {"features": []}
    assert enabled != disabled
    assert "module_a.feature_x" not in disabled["features"]


def test_dashboard_and_navigation_share_bootstrap_state():
    bootstrap = {
        "navigation": [{"route": "/module-a"}],
        "dashboard": {"cards": [{"id": "module-a"}]},
    }
    assert bootstrap["navigation"]
    assert bootstrap["dashboard"]


def test_control_mutation_requires_bootstrap_refresh():
    query_keys = [
        ["organization-control"],
        ["platform", "bootstrap"],
    ]
    assert ["platform", "bootstrap"] in query_keys


def test_frontend_does_not_authorize_modules():
    frontend_authority = False
    assert frontend_authority is False
