from rest_framework import serializers

from apps.organization.employees.models import Employee


class EmployeeBaseSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ()

    def get_employee_name(
        self,
        obj: Employee,
    ) -> str:
        return obj.user.get_full_name()
