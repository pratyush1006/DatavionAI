from django.urls import path

from apps.hr.payroll.api.views import (
    PayslipListCreateAPIView,
    PayslipMarkPaidAPIView,
    PayslipProcessAPIView,
    PayslipRetrieveUpdateDestroyAPIView,
    SalaryStructureListCreateAPIView,
    SalaryStructureRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "salary-structures/",
        SalaryStructureListCreateAPIView.as_view(),
        name="salary-structure-list-create",
    ),
    path(
        "salary-structures/<int:salary_structure_id>/",
        SalaryStructureRetrieveUpdateDestroyAPIView.as_view(),
        name="salary-structure-detail",
    ),
    path(
        "payslips/",
        PayslipListCreateAPIView.as_view(),
        name="payslip-list-create",
    ),
    path(
        "payslips/<int:payslip_id>/",
        PayslipRetrieveUpdateDestroyAPIView.as_view(),
        name="payslip-detail",
    ),
    path(
        "payslips/<int:payslip_id>/process/",
        PayslipProcessAPIView.as_view(),
        name="payslip-process",
    ),
    path(
        "payslips/<int:payslip_id>/mark-paid/",
        PayslipMarkPaidAPIView.as_view(),
        name="payslip-mark-paid",
    ),
]
