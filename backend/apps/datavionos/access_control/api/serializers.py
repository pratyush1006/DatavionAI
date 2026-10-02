"""Serializers for organization access-control mutations."""

from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from apps.platform.accounts.models import User
from apps.platform.rbac.constants import RoleScope, SystemRole
from apps.platform.rbac.models import Role


class OrganizationRoleAssignmentSerializer(serializers.Serializer):
    """Validate organization role assignment."""

    user_id = serializers.UUIDField()
    role_id = serializers.UUIDField()
    is_primary = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)

    def validate_role_id(self, value):
        if (
            not Role.objects.filter(
                pk=value,
                is_active=True,
                is_system=True,
                is_assignable=True,
                scope=RoleScope.ORGANIZATION,
            )
            .exclude(
                code__in=(
                    SystemRole.PLATFORM_ADMIN,
                    SystemRole.ORGANIZATION_OWNER,
                    SystemRole.ORGANIZATION_ADMIN,
                )
            )
            .exists()
        ):
            raise serializers.ValidationError(
                "Select an active organization role that can be assigned."
            )
        return value


class OrganizationMemberOnboardingSerializer(serializers.Serializer):
    """Validate creation of an organization user, employee record, and role."""

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    temporary_password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
    role_id = serializers.UUIDField()
    designation = serializers.CharField(max_length=150)
    employee_code = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )
    employment_type = serializers.CharField(
        max_length=30, required=False, default="FULL_TIME"
    )
    joining_date = serializers.DateField(required=False, default=timezone.localdate)
    department_id = serializers.UUIDField(required=False, allow_null=True)
    team_id = serializers.UUIDField(required=False, allow_null=True)
    supervisor_id = serializers.UUIDField(required=False, allow_null=True)

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def validate_role_id(self, value):
        if (
            not Role.objects.filter(
                pk=value,
                is_active=True,
                is_system=True,
                is_assignable=True,
                scope=RoleScope.ORGANIZATION,
            )
            .exclude(
                code__in=(
                    SystemRole.PLATFORM_ADMIN,
                    SystemRole.ORGANIZATION_OWNER,
                    SystemRole.ORGANIZATION_ADMIN,
                )
            )
            .exists()
        ):
            raise serializers.ValidationError(
                "Select an active, seeded organization role that can be assigned."
            )
        return value

    def validate(self, attrs):
        if attrs.get("team_id") and not attrs.get("department_id"):
            raise serializers.ValidationError(
                {"department_id": "Select a department before selecting a team."}
            )
        return attrs


class DepartmentMemberAssignmentSerializer(serializers.Serializer):
    """Validate department membership assignment."""

    department_id = serializers.UUIDField()
    employee_id = serializers.UUIDField()
    role_id = serializers.UUIDField(required=False, allow_null=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=255)
    is_primary = serializers.BooleanField(default=False)


class OrganizationDepartmentCreateSerializer(serializers.Serializer):
    """Create a department in the caller's active organization context."""

    name = serializers.CharField(max_length=255)
    code = serializers.RegexField(r"^[A-Z0-9_-]+$", max_length=30)
    department_type = serializers.CharField(max_length=50, required=False)


class OrganizationTeamCreateSerializer(serializers.Serializer):
    """Create an operational team and attach it to one department."""

    name = serializers.CharField(max_length=255)
    code = serializers.RegexField(r"^[A-Z0-9_-]+$", max_length=50)
    department_id = serializers.UUIDField()
    team_type = serializers.CharField(max_length=50, required=False, allow_blank=True)


class LifecycleSerializer(serializers.Serializer):
    """Validate lifecycle state."""

    is_active = serializers.BooleanField()
