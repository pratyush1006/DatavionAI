"""
DatavionOS role/subscription runtime alignment tests.
"""

from apps.datavionos.services.effective_capability import (
    build_effective_capability_context,
)


def test_doctor_runtime_scope():
    context = build_effective_capability_context(
        user_id="doctor-1",
        organization_id="org-1",
        tenant_id="tenant-1",
        modules={
            "patients": True,
            "appointments": True,
            "clinical": True,
            "pharmacy": False,
            "laboratory": False,
            "radiology": False,
        },
        features={
            "patients.dashboard": True,
            "clinical.dashboard": True,
        },
        permissions={
            "patients.view",
            "appointments.view",
            "clinical.view",
        },
        roles={
            "doctor",
        },
        departments={
            "clinical",
        },
        ai_capabilities={
            "clinical_ai": True,
            "pharmacy_ai": False,
        },
    )

    assert context.module_enabled("patients")
    assert context.module_enabled("appointments")
    assert context.module_enabled("clinical")

    assert not context.module_enabled("pharmacy")
    assert not context.module_enabled("laboratory")
    assert not context.module_enabled("radiology")

    assert context.has_permission("patients.view")
    assert context.has_permission("clinical.view")

    assert not context.has_permission("pharmacy.view")

    assert "doctor" in context.roles
    assert "clinical" in context.departments

    assert context.ai_enabled("clinical_ai")
    assert not context.ai_enabled("pharmacy_ai")


def test_subscription_module_ceiling():
    context = build_effective_capability_context(
        user_id="doctor-2",
        organization_id="org-1",
        tenant_id="tenant-1",
        modules={
            "patients": True,
            "pharmacy": False,
        },
        permissions={
            "patients.view",
            "pharmacy.view",
        },
        roles={
            "doctor",
        },
        departments={
            "clinical",
        },
    )

    assert context.module_enabled("patients")
    assert not context.module_enabled("pharmacy")


def test_permission_does_not_override_missing_entitlement():
    context = build_effective_capability_context(
        user_id="doctor-3",
        organization_id="org-1",
        tenant_id="tenant-1",
        modules={
            "pharmacy": False,
        },
        permissions={
            "pharmacy.view",
        },
        roles={
            "doctor",
        },
        departments={
            "clinical",
        },
    )

    assert not context.module_enabled("pharmacy")
    assert context.has_permission("pharmacy.view")


def test_pharmacist_scope():
    context = build_effective_capability_context(
        user_id="pharmacist-1",
        organization_id="org-1",
        tenant_id="tenant-1",
        modules={
            "pharmacy": True,
        },
        permissions={
            "pharmacy.view",
        },
        roles={
            "pharmacist",
        },
        departments={
            "pharmacy",
        },
        ai_capabilities={
            "pharmacy_ai": True,
        },
    )

    assert context.module_enabled("pharmacy")
    assert context.has_permission("pharmacy.view")
    assert "pharmacist" in context.roles
    assert "pharmacy" in context.departments
    assert context.ai_enabled("pharmacy_ai")
