from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from apps.platform.organizations.constants import (
    ORGANIZATION_CATEGORY_TYPES,
    OrganizationCategory,
    OrganizationSize,
    OrganizationType,
)


class OrganizationOnboardingValidationError(ValueError):
    """Raised when an onboarding organization profile is invalid."""


ORGANIZATION_TYPE_PLAN_SEGMENTS: dict[str, tuple[str, ...]] = {
    OrganizationType.HOSPITAL: ("HOSPITAL",),
    OrganizationType.CLINIC: ("CLINIC",),
    OrganizationType.DENTAL_CLINIC: ("DENTAL",),
    OrganizationType.EYE_CLINIC: ("CLINIC",),
    OrganizationType.ENT_CLINIC: ("CLINIC",),
    OrganizationType.CARDIOLOGY_CLINIC: ("CLINIC",),
    OrganizationType.NEUROLOGY_CLINIC: ("CLINIC",),
    OrganizationType.ORTHOPEDIC_CLINIC: ("CLINIC",),
    OrganizationType.PEDIATRIC_CLINIC: ("CLINIC",),
    OrganizationType.GYNECOLOGY_CLINIC: ("CLINIC",),
    OrganizationType.DERMATOLOGY_CLINIC: ("CLINIC",),
    OrganizationType.PSYCHIATRY_CLINIC: ("CLINIC",),
    OrganizationType.ONCOLOGY_CENTER: ("CLINIC",),
    OrganizationType.PHYSIOTHERAPY_CENTER: ("PHYSIOTHERAPY",),
    OrganizationType.REHABILITATION_CENTER: ("PHYSIOTHERAPY",),
    OrganizationType.DIALYSIS_CENTER: ("CLINIC",),
    OrganizationType.FERTILITY_CENTER: ("CLINIC",),
    OrganizationType.HOME_HEALTHCARE: ("NURSING_HOME",),
    OrganizationType.TELEMEDICINE: ("CLINIC",),
    OrganizationType.NURSING_HOME: ("NURSING_HOME",),
    OrganizationType.HOSPICE: ("NURSING_HOME",),
    OrganizationType.ASSISTED_LIVING: ("NURSING_HOME",),
    OrganizationType.WELLNESS_CENTER: ("CLINIC",),
    OrganizationType.LABORATORY: ("LABORATORY",),
    OrganizationType.DIAGNOSTIC_CENTER: ("LABORATORY", "IMAGING"),
    OrganizationType.RADIOLOGY_CENTER: ("IMAGING",),
    OrganizationType.IMAGING_CENTER: ("IMAGING",),
    OrganizationType.PATHOLOGY_LAB: ("LABORATORY",),
    OrganizationType.RETAIL_PHARMACY: ("PHARMACY",),
    OrganizationType.HOSPITAL_PHARMACY: ("PHARMACY",),
    OrganizationType.ONLINE_PHARMACY: ("PHARMACY",),
    OrganizationType.WHOLESALE_PHARMACY: ("PHARMACY",),
    OrganizationType.CORPORATE: ("ENTERPRISE",),
    OrganizationType.OCCUPATIONAL_HEALTH: ("ENTERPRISE",),
    OrganizationType.HEALTHCARE_NETWORK: ("ENTERPRISE",),
    OrganizationType.GOVERNMENT_HOSPITAL: ("HOSPITAL",),
}


def _normalize(value: Any) -> str:
    return str(value or "").strip().lower()


def plan_segments_for_organization_type(
    organization_type: str,
) -> tuple[str, ...]:
    return ORGANIZATION_TYPE_PLAN_SEGMENTS.get(
        _normalize(organization_type),
        (),
    )


def eligible_plan_segments(
    organization_type: str,
) -> Iterable[str]:
    return plan_segments_for_organization_type(organization_type)


def category_for_organization_type(
    organization_type: str,
) -> str:
    normalized_type = _normalize(organization_type)

    for category, members in ORGANIZATION_CATEGORY_TYPES.items():
        if any(_normalize(member.value) == normalized_type for member in members):
            return category.value

    return ""


def organization_type_matches_category(
    organization_type: str,
    category: str,
) -> bool:
    return category_for_organization_type(
        organization_type,
    ) == _normalize(category)


def validate_organization_profile(
    data: Mapping[str, Any],
) -> tuple[str, str, str]:
    organization_type = _normalize(
        data.get("organization_type"),
    )
    category = _normalize(
        data.get("category"),
    )
    if not category:
        category = _normalize(
            category_for_organization_type(organization_type),
        )
    size = _normalize(
        data.get("size"),
    )
    if not size:
        size = "small"

    valid_types = {item.value for item in OrganizationType}
    valid_categories = {item.value for item in OrganizationCategory}
    valid_sizes = {item.value for item in OrganizationSize}

    if not organization_type:
        raise OrganizationOnboardingValidationError(
            "organization_type is required.",
        )

    if organization_type not in valid_types:
        raise OrganizationOnboardingValidationError(
            "Invalid organization_type.",
        )

    if not category:
        raise OrganizationOnboardingValidationError(
            "category is required.",
        )

    if category not in valid_categories:
        raise OrganizationOnboardingValidationError(
            "Invalid category.",
        )

    if not organization_type_matches_category(
        organization_type,
        category,
    ):
        raise OrganizationOnboardingValidationError(
            "organization_type does not belong to the selected category.",
        )

    if not size:
        raise OrganizationOnboardingValidationError(
            "size is required.",
        )

    if size not in valid_sizes:
        raise OrganizationOnboardingValidationError(
            "Invalid organization size.",
        )

    return (
        category,
        organization_type,
        size,
    )


def _metadata_mapping(
    plan: Any,
) -> dict[str, Any]:
    value = getattr(
        plan,
        "metadata",
        {},
    )

    return dict(value) if isinstance(value, Mapping) else {}


def _metadata_values(
    metadata: Mapping[str, Any],
    *keys: str,
) -> set[str]:
    for key in keys:
        value = metadata.get(key)

        if isinstance(
            value,
            (list, tuple, set, frozenset),
        ):
            return {_normalize(item) for item in value if _normalize(item)}

    return set()


def _legacy_profile_catalog_matches(
    plan: Any,
    *,
    category: str,
    organization_type: str,
    size: str,
) -> bool:
    """Match plans from the deployed category-segmented catalog.

    The original public catalog stores the organization category in
    ``healthcare_segment`` and encodes the exact type and size in a code such
    as ``datavion-healthcare_provider-dental_clinic-solo-starter``. Newer
    plans use the dedicated healthcare segments above. Supporting both keeps
    plan selection backend-authoritative while allowing the existing catalog
    to be used without a data migration.
    """

    code = _normalize(getattr(plan, "code", ""))
    category = _normalize(category)
    organization_type = _normalize(organization_type)
    size = _normalize(size)

    if not code.startswith(f"datavion-{category}-"):
        # Non-catalog plans rely on their segment and optional metadata.
        return True

    return f"-{organization_type}-{size}-" in f"-{code}-"


def plan_is_eligible_for_onboarding(
    plan: Any,
    *,
    category: str,
    organization_type: str,
    size: str,
) -> bool:
    if plan is None:
        return False

    segment = _normalize(
        getattr(
            plan,
            "healthcare_segment",
            "",
        ),
    )

    allowed_segments = {
        _normalize(value)
        for value in plan_segments_for_organization_type(
            organization_type,
        )
    }

    # The deployed self-service catalog uses category values as segments;
    # retain dedicated type segments for the canonical Plan model.
    allowed_segments.add(_normalize(category))

    if segment not in allowed_segments:
        return False

    metadata = _metadata_mapping(plan)

    allowed_categories = _metadata_values(
        metadata,
        "organization_categories",
        "categories",
        "allowed_categories",
    )

    if allowed_categories and _normalize(category) not in allowed_categories:
        return False

    allowed_types = _metadata_values(
        metadata,
        "organization_types",
        "types",
        "allowed_organization_types",
    )

    if allowed_types and _normalize(organization_type) not in allowed_types:
        return False

    allowed_sizes = _metadata_values(
        metadata,
        "organization_sizes",
        "sizes",
        "allowed_sizes",
    )

    if allowed_sizes and _normalize(size) not in allowed_sizes:
        return False

    if segment == _normalize(category):
        return _legacy_profile_catalog_matches(
            plan,
            category=category,
            organization_type=organization_type,
            size=size,
        )

    return True


__all__ = [
    "ORGANIZATION_TYPE_PLAN_SEGMENTS",
    "OrganizationOnboardingValidationError",
    "category_for_organization_type",
    "eligible_plan_segments",
    "organization_type_matches_category",
    "plan_is_eligible_for_onboarding",
    "plan_segments_for_organization_type",
    "validate_organization_profile",
]
