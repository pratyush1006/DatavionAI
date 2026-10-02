"""Contracts for organization context and access-control orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class OrganizationAccessSnapshot:
    """Organization-scoped access-control snapshot."""

    organization: dict[str, Any]
    departments: list[dict[str, Any]]
    teams: list[dict[str, Any]]
    department_type_options: list[dict[str, str]]
    department_templates: list[dict[str, str]]
    team_type_options: list[dict[str, str]]
    team_templates: list[dict[str, str]]
    organization_roles: list[dict[str, Any]]
    available_roles: list[dict[str, Any]]
    employees: list[dict[str, Any]]
    department_memberships: list[dict[str, Any]]
    permissions: list[dict[str, Any]]
    ai_capabilities: dict[str, bool]
    can_manage_access: bool
    can_manage_departments: bool
