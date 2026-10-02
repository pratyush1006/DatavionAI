# Operational AI is advisory. It cannot autonomously assign beds,
# admit, transfer, discharge, prescribe, or make clinical decisions.

# Explicit governance contract: this domain may request only advisory
# operational intelligence. It may never autonomously perform clinical
# or patient-flow actions.
AUTONOMOUS_CLINICAL_ACTION = False
autonomous_clinical_action = AUTONOMOUS_CLINICAL_ACTION

ALLOWED_CAPABILITIES = {
    "bed_capacity_forecast",
    "bed_utilization_summary",
    "room_utilization_summary",
    "opd_queue_summary",
    "patient_flow_summary",
    "operational_anomaly_detection",
}


def build_ai_context(*, tenant, organization, module_reference, unit_id=None):
    return {
        "tenant_id": str(tenant.pk),
        "organization_id": str(organization.pk),
        "module_reference": module_reference,
        "unit_id": str(unit_id) if unit_id else None,
    }


def validate_ai_capability(capability):
    if capability not in ALLOWED_CAPABILITIES:
        raise ValueError(f"Unsupported hospital operations AI capability: {capability}")
