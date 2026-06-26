from rest_framework import serializers

from apps.employees.models import Employee


class EmployeeListSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    department = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    team = serializers.CharField(
        source="team.name",
        read_only=True,
    )

    class Meta:
        model = Employee

        fields = (
            "id",
            "employee_code",
            "employee_name",
            "designation",
            "organization",
            "department",
            "team",
            "is_active",
        )

    def get_employee_name(
        self,
        obj,
    ):
        return obj.user.get_full_name()


class EmployeeDetailSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    department = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    department_id = serializers.IntegerField(
        source="department.id",
        read_only=True,
    )

    team = serializers.CharField(
        source="team.name",
        read_only=True,
    )

    team_id = serializers.IntegerField(
        source="team.id",
        read_only=True,
    )

    user_id = serializers.IntegerField(
        source="user.id",
        read_only=True,
    )

    manager = serializers.SerializerMethodField()

    manager_id = serializers.IntegerField(
        source="manager.id",
        read_only=True,
    )

    class Meta:
        model = Employee

        fields = (
            "id",
            "employee_code",
            "employee_name",
            "user_id",
            "organization",
            "organization_id",
            "department",
            "department_id",
            "team",
            "team_id",
            "designation",
            "manager",
            "manager_id",
            "hire_date",
            "is_active",
            "created_at",
            "updated_at",
        )

    def get_employee_name(
        self,
        obj,
    ):
        return obj.user.get_full_name()

    def get_manager(
        self,
        obj,
    ):
        if obj.manager:
            return obj.manager.user.get_full_name()

        return None


class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee

        fields = (
            "organization",
            "department",
            "team",
            "user",
            "employee_code",
            "designation",
            "manager",
            "hire_date",
            "is_active",
        )


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee

        fields = (
            "organization",
            "department",
            "team",
            "user",
            "employee_code",
            "designation",
            "manager",
            "hire_date",
            "is_active",
        )
