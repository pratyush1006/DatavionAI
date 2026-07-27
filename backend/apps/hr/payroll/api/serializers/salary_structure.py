from rest_framework import serializers

from apps.hr.payroll.models import SalaryStructure

from .fields import (
    SALARY_STRUCTURE_DETAIL_FIELDS,
    SALARY_STRUCTURE_LIST_FIELDS,
    SALARY_STRUCTURE_WRITE_FIELDS,
)


class SalaryStructureBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    gross_salary = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = SalaryStructure
        fields = ()

    def get_employee_name(self, obj: SalaryStructure) -> str:
        return obj.employee.full_name


class SalaryStructureListSerializer(SalaryStructureBaseSerializer):
    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    class Meta(SalaryStructureBaseSerializer.Meta):
        fields = SALARY_STRUCTURE_LIST_FIELDS
        read_only_fields = SALARY_STRUCTURE_LIST_FIELDS


class SalaryStructureDetailSerializer(SalaryStructureBaseSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    organization_id = serializers.IntegerField(
        source="organization.id",
        read_only=True,
    )

    employee = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
    )

    employee_id = serializers.IntegerField(
        source="employee.id",
        read_only=True,
    )

    class Meta(SalaryStructureBaseSerializer.Meta):
        fields = SALARY_STRUCTURE_DETAIL_FIELDS
        read_only_fields = SALARY_STRUCTURE_DETAIL_FIELDS


class SalaryStructureCreateSerializer(SalaryStructureBaseSerializer):
    class Meta(SalaryStructureBaseSerializer.Meta):
        fields = SALARY_STRUCTURE_WRITE_FIELDS


class SalaryStructureUpdateSerializer(SalaryStructureBaseSerializer):
    class Meta(SalaryStructureBaseSerializer.Meta):
        fields = SALARY_STRUCTURE_WRITE_FIELDS
