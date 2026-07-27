"""
Jinja2 prompt engine backed by the ``PromptTemplate`` registry.
"""

from __future__ import annotations

from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from jinja2 import Template
from jinja2.exceptions import TemplateError

from apps.ai.models import PromptTemplate
from apps.datavionos.ai.exceptions import PromptEngineError
from apps.datavionos.ai.prompt import (
    PromptRequest,
    PromptResponse,
)
from apps.datavionos.ai.prompt import (
    PromptTemplate as PromptTemplateContract,
)


class JinjaPromptEngine:
    """
    Renders prompts from versioned ``PromptTemplate`` rows using Jinja2.
    """

    def __init__(
        self,
        *,
        organization_id: Any | None = None,
    ) -> None:
        self._organization_id = organization_id

    async def render(
        self,
        request: PromptRequest,
    ) -> PromptResponse:
        """Render a prompt from a template."""

        try:
            template = Template(request.template.template)
        except TemplateError as exc:
            raise PromptEngineError(str(exc)) from exc

        try:
            rendered = template.render(**request.variables)
        except TemplateError as exc:
            raise PromptEngineError(str(exc)) from exc

        return PromptResponse(
            prompt=rendered,
            metadata={"template": request.template.name},
        )

    async def validate(
        self,
        template: PromptTemplateContract,
    ) -> bool:
        """Validate a prompt template compiles."""

        try:
            Template(template.template)
            return True
        except TemplateError:
            return False

    async def resolve(
        self,
        name: str,
        version: str | None = None,
    ) -> PromptTemplateContract:
        """
        Resolve a registered template by name and optional version.
        """

        queryset = PromptTemplate.objects.filter(name=name)

        if self._organization_id is not None:
            queryset = queryset.filter(
                models_q(self._organization_id),
            )

        if version:
            queryset = queryset.filter(version=version)
        else:
            queryset = queryset.filter(is_active=True)

        try:
            instance = queryset.order_by("-version").first()
        except ObjectDoesNotExist:
            instance = None

        if instance is None:
            raise PromptEngineError(f"Prompt template not found: {name}")

        return PromptTemplateContract(
            name=instance.name,
            template=instance.template,
            version=instance.version,
        )


def models_q(organization_id: Any):
    """Build an organization-or-global lookup."""

    from django.db.models import Q

    from apps.platform.organizations.models import Organization

    org = Organization.objects.filter(pk=organization_id).first()
    return Q(organization__isnull=True) | Q(organization=org)


__all__ = [
    "JinjaPromptEngine",
]
