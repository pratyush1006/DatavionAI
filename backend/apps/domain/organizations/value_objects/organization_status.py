"""
Organization status value object.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.domain.common import ValueObject
from apps.domain.organizations.enums.organization_status import (
    OrganizationStatus as OrganizationStatusEnum,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationStatus(
    ValueObject,
):
    """
    Organization lifecycle status.
    """

    value: OrganizationStatusEnum

    def _equality_components(
        self,
    ) -> tuple[object, ...]:
        return (self.value,)

    def __str__(
        self,
    ) -> str:
        return self.value.value

    @property
    def is_pending(
        self,
    ) -> bool:
        return self.value is OrganizationStatusEnum.PENDING

    @property
    def is_active(
        self,
    ) -> bool:
        return self.value is OrganizationStatusEnum.ACTIVE

    @property
    def is_suspended(
        self,
    ) -> bool:
        return self.value is OrganizationStatusEnum.SUSPENDED

    @property
    def is_inactive(
        self,
    ) -> bool:
        return self.value is OrganizationStatusEnum.INACTIVE

    @property
    def is_archived(
        self,
    ) -> bool:
        return self.value is OrganizationStatusEnum.ARCHIVED
