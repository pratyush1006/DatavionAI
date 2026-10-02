from django.contrib import admin

from apps.imaging.models import (
    ContrastAssessment,
    ImagingAppointmentLink,
    ImagingAuditEvent,
    ImagingChargeLink,
    ImagingDocumentLink,
    ImagingFinding,
    ImagingModality,
    ImagingOrder,
    ImagingProcedure,
    ImagingStudy,
    ImagingStudyReference,
    RadiologyReport,
    RadiologyReportVersion,
)

for model in (
    ImagingModality,
    ImagingOrder,
    ImagingProcedure,
    ImagingStudy,
    ContrastAssessment,
    ImagingFinding,
    RadiologyReport,
    RadiologyReportVersion,
    ImagingAppointmentLink,
    ImagingDocumentLink,
    ImagingChargeLink,
    ImagingStudyReference,
    ImagingAuditEvent,
):
    admin.site.register(model)
