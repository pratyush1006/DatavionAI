"""
Organization onboarding workflow.

Provision organization defaults after creation.

Creates:

- Organization Profile
- Organization Branding
- Organization Settings
- Organization Modules
- Organization Features

Designed to be idempotent:
- Safe for retries
- Safe for Celery jobs
- Safe for failed provisioning recovery
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.platform.organizations.models import (
    Organization,
    OrganizationFeature,
    OrganizationModule,
    OrganizationProfile,
    OrganizationSettings,
)
from apps.platform.organizations.services.organization_branding import (
    create_branding,
)
from apps.platform.organizations.services.organization_feature import (
    create_feature,
)
from apps.platform.organizations.services.organization_module import (
    create_module,
)
from apps.platform.organizations.services.organization_settings import (
    create_settings,
)

logger = logging.getLogger(__name__)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationOnboardingRequest:
    """
    Organization onboarding input.
    """

    organization: dict[str, Any]

    settings: dict[str, Any] | None = None

    branding: dict[str, Any] | None = None

    modules: tuple[dict[str, Any], ...] = ()

    features: tuple[dict[str, Any], ...] = ()


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class OrganizationOnboardingData:
    """
    Workflow result.
    """

    organization_id: UUID

    profile_created: bool

    branding_created: bool

    settings_created: bool

    modules_created: int

    features_created: int


class OrganizationOnboardingWorkflow(
    BaseWorkflow[OrganizationOnboardingData],
):
    """
    Organization provisioning workflow.

    Idempotent provisioning workflow.
    """

    def __init__(
        self,
        *,
        request: OrganizationOnboardingRequest,
        logger_: logging.Logger | None = None,
    ) -> None:

        super().__init__(
            logger_=logger_,
        )

        self._request = request

    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[OrganizationOnboardingData]:

        organization = Organization.objects.get(
            id=self._request.organization["id"],
        )

        #
        # Profile
        #
        _, profile_created = OrganizationProfile.objects.get_or_create(
            organization=organization,
            defaults={
                "industry": "healthcare",
                "facility_type": (organization.organization_type),
                "description": (
                    self._request.organization.get(
                        "description",
                        "",
                    )
                ),
                "metadata": {},
            },
        )

        #
        # Settings
        #
        settings_created = False

        if self._request.settings:
            settings_exists = OrganizationSettings.objects.filter(
                organization=organization,
            ).exists()

            if not settings_exists:
                create_settings(
                    validated_data={
                        "organization": organization,
                        **self._request.settings,
                    },
                )

                settings_created = True

        #
        # Branding
        #
        branding_created = False

        if self._request.branding:
            branding_exists = hasattr(
                organization,
                "branding",
            )

            if not branding_exists:
                create_branding(
                    validated_data={
                        "organization": organization,
                        **self._request.branding,
                    },
                )

                branding_created = True

        #
        # Modules
        #
        modules_created = 0

        for module in self._request.modules:
            module_code = module["code"]

            module_exists = OrganizationModule.objects.filter(
                organization=organization,
                module_code=module_code,
            ).exists()

            if not module_exists:
                create_module(
                    validated_data={
                        "organization": organization,
                        "module_code": module_code,
                        "status": (
                            "enabled"
                            if module.get(
                                "enabled",
                                True,
                            )
                            else "disabled"
                        ),
                    },
                )

                modules_created += 1

        #
        # Features
        #
        features_created = 0

        for feature in self._request.features:
            feature_code = feature["code"]

            feature_exists = OrganizationFeature.objects.filter(
                organization=organization,
                feature_code=feature_code,
            ).exists()

            if not feature_exists:
                create_feature(
                    validated_data={
                        "organization": organization,
                        "feature_code": feature_code,
                        "status": (
                            "enabled"
                            if feature.get(
                                "enabled",
                                True,
                            )
                            else "disabled"
                        ),
                    },
                )

                features_created += 1

        data = OrganizationOnboardingData(
            organization_id=organization.id,
            profile_created=profile_created,
            branding_created=branding_created,
            settings_created=settings_created,
            modules_created=modules_created,
            features_created=features_created,
        )

        logger.info(
            "Organization onboarding completed.",
            extra={
                "organization_id": str(
                    organization.id,
                ),
                "tenant_id": str(
                    context.tenant_id,
                ),
            },
        )

        return WorkflowResult.ok(
            context=context,
            data=data,
            message="Organization onboarded successfully.",
            code="organization_onboarded",
        )


__all__: tuple[str, ...] = (
    "OrganizationOnboardingRequest",
    "OrganizationOnboardingData",
    "OrganizationOnboardingWorkflow",
)
