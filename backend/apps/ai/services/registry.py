"""AI application bootstrap and department registry."""

from __future__ import annotations

from apps.ai.constants import AIApplicationCode
from apps.ai.models import AIApplication
from apps.ai.services.scope import validate_scope

DEFAULT_APPLICATIONS = (
    (AIApplicationCode.CLINICAL_AI, "Clinical AI", "Clinical"),
    (AIApplicationCode.LABORATORY_AI, "Laboratory AI", "Laboratory"),
    (AIApplicationCode.PHARMACY_AI, "Pharmacy AI", "Pharmacy"),
    (AIApplicationCode.IMAGING_AI, "Imaging AI", "Imaging"),
    (AIApplicationCode.REVENUE_CYCLE_AI, "Revenue Cycle AI", "Revenue Cycle"),
)


def ensure_department_applications(*, tenant, organization):
    validate_scope(tenant=tenant, organization=organization)
    applications = []
    for code, name, department in DEFAULT_APPLICATIONS:
        app, _ = AIApplication.objects.get_or_create(
            organization=organization,
            code=code,
            defaults={"tenant": tenant, "name": name, "department": department},
        )
        if app.tenant_id != tenant.pk:
            raise ValueError("Existing AI application has an invalid tenant")
        applications.append(app)
    return applications
