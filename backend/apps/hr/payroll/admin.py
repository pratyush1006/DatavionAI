from django.contrib import admin

from apps.hr.payroll.models import (
    Payslip,
    PayslipLineItem,
    SalaryStructure,
)


class PayslipLineItemInline(admin.TabularInline):
    model = PayslipLineItem
    extra = 0


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "basic_salary",
        "currency",
        "effective_from",
        "effective_to",
        "is_active",
    )

    list_filter = ("organization", "currency", "is_active")

    search_fields = ("employee__employee_code",)

    ordering = ("-effective_from",)


@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "pay_period_start",
        "pay_period_end",
        "net_pay",
        "currency",
        "status",
    )

    list_filter = ("organization", "status", "currency")

    search_fields = ("employee__employee_code",)

    ordering = ("-pay_period_start",)

    inlines = (PayslipLineItemInline,)
