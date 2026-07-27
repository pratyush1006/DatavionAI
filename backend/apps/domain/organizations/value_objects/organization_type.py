"""
Organization type value object.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.domain.common import ValueObject
from apps.domain.organizations.enums.organization_type import (
    OrganizationType as OrganizationTypeEnum,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationType(
    ValueObject,
):
    """
    Organization type.
    """

    value: OrganizationTypeEnum

    def _equality_components(
        self,
    ) -> tuple[object, ...]:
        return (self.value,)

    def __str__(
        self,
    ) -> str:
        return self.value.value

    @property
    def is_hospital(
        self,
    ) -> bool:
        return self.value is OrganizationTypeEnum.HOSPITAL

    @property
    def is_clinic(
        self,
    ) -> bool:
        return self.value is OrganizationTypeEnum.CLINIC

    @property
    def is_laboratory(
        self,
    ) -> bool:
        return self.value is OrganizationTypeEnum.LABORATORY

    @property
    def is_pharmacy(
        self,
    ) -> bool:
        return self.value is OrganizationTypeEnum.PHARMACY
