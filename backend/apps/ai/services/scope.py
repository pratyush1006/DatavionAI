from __future__ import annotations

from apps.ai.exceptions import AIAuthorizationError


def validate_scope(*, tenant, organization) -> None:
    if tenant is None or organization is None:
        raise AIAuthorizationError("Tenant and organization are required.")
    if getattr(organization, "tenant_id", None) != getattr(tenant, "pk", None):
        raise AIAuthorizationError("Organization does not belong to tenant.")


def validate_application_scope(application, *, tenant, organization) -> None:
    validate_scope(tenant=tenant, organization=organization)
    if (
        getattr(application, "tenant_id", None) != tenant.pk
        or getattr(application, "organization_id", None) != organization.pk
    ):
        raise AIAuthorizationError(
            "AI application is outside tenant/organization scope."
        )


def validate_module_reference_scope(module_reference, *, tenant, organization) -> None:
    validate_scope(tenant=tenant, organization=organization)
    if module_reference is None:
        raise AIAuthorizationError("AI module reference is required.")
    if (
        getattr(module_reference, "tenant_id", None) != tenant.pk
        or getattr(module_reference, "organization_id", None) != organization.pk
    ):
        raise AIAuthorizationError(
            "AI module reference is outside tenant/organization scope."
        )


def validate_knowledge_base_scope(knowledge_base, *, tenant, organization) -> None:
    validate_scope(tenant=tenant, organization=organization)
    if knowledge_base is None:
        raise AIAuthorizationError("Knowledge base is required.")
    if (
        getattr(knowledge_base, "tenant_id", None) != tenant.pk
        or getattr(knowledge_base, "organization_id", None) != organization.pk
    ):
        raise AIAuthorizationError(
            "Knowledge base is outside tenant/organization scope."
        )


def validate_document_scope(document, *, tenant, organization) -> None:
    validate_scope(tenant=tenant, organization=organization)
    if document is None:
        raise AIAuthorizationError("Knowledge document is required.")

    knowledge_base = getattr(document, "knowledge_base", None)
    if (
        getattr(document, "organization_id", None) != organization.pk
        or getattr(knowledge_base, "tenant_id", None) != tenant.pk
        or getattr(knowledge_base, "organization_id", None) != organization.pk
    ):
        raise AIAuthorizationError(
            "Knowledge document is outside tenant/organization scope."
        )


__all__ = (
    "validate_scope",
    "validate_application_scope",
    "validate_module_reference_scope",
    "validate_knowledge_base_scope",
    "validate_document_scope",
)
