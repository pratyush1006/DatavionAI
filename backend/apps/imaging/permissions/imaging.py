from apps.clinical.permissions import ClinicalAPIPermission


class ImagingAuthenticatedPermission(ClinicalAPIPermission):
    """Require organization-scoped imaging permissions at every API method."""

    domain = "imaging"
    action_aliases = {
        "ready": "update",
        "schedule": "update",
        "start": "update",
        "complete": "update",
        "arrive": "update",
        "acquire": "update",
        "interpret": "approve",
        "finalize": "approve",
    }
