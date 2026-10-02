from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("recruitment/", include("apps.hr.recruitment.urls")),
    path("attendance/", include("apps.hr.attendance.urls")),
    path("holidays/", include("apps.hr.holidays.urls")),
    path("leave/", include("apps.hr.leave.urls")),
    path("onboarding/", include("apps.hr.onboarding.urls")),
    path("payroll/", include("apps.hr.payroll.urls")),
    path("performance/", include("apps.hr.performance.urls")),
    path("shifts/", include("apps.hr.shifts.urls")),
    path("employees/", include("apps.organization.employees.urls")),
]

__all__ = ("urlpatterns",)
