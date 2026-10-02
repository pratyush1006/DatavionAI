"""Read-only tenant-safe AI selectors."""

from __future__ import annotations

from apps.ai.models import AIApplication, AIConfiguration, AIConversation, KnowledgeBase


def applications_for(*, tenant, organization):
    return AIApplication.objects.filter(
        tenant=tenant, organization=organization, status="active"
    ).order_by("name")


def get_application(*, tenant, organization, code):
    return AIApplication.objects.get(
        tenant=tenant, organization=organization, code=code
    )


def conversations_for(*, tenant, organization, application=None):
    qs = AIConversation.objects.filter(tenant=tenant, organization=organization)
    return qs.filter(application=application) if application else qs


def knowledge_bases_for(*, tenant, organization):
    return KnowledgeBase.objects.filter(
        tenant=tenant, organization=organization, is_active=True
    )


def get_configuration(*, tenant, organization, application):
    return AIConfiguration.objects.select_related("provider", "model").get(
        tenant=tenant,
        organization=organization,
        application=application,
        is_active=True,
    )


__all__ = (
    "applications_for",
    "conversations_for",
    "get_application",
    "get_configuration",
    "knowledge_bases_for",
)
