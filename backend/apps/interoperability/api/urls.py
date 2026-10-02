"""Interoperability URL configuration."""

from django.urls import path

from apps.interoperability.api.views import (
    FHIREncounterDetailAPIView,
    FHIROrganizationDetailAPIView,
    FHIRPatientDetailAPIView,
    FHIRProviderDetailAPIView,
    HL7ADTAPIView,
    HL7ORUAPIView,
)

urlpatterns = [
    path(
        "fhir/Patient/<uuid:patient_id>/",
        FHIRPatientDetailAPIView.as_view(),
        name="fhir-patient-detail",
    ),
    path(
        "fhir/Encounter/<uuid:encounter_id>/",
        FHIREncounterDetailAPIView.as_view(),
        name="fhir-encounter-detail",
    ),
    path(
        "fhir/Practitioner/<uuid:provider_id>/",
        FHIRProviderDetailAPIView.as_view(),
        name="fhir-practitioner-detail",
    ),
    path(
        "fhir/Organization/",
        FHIROrganizationDetailAPIView.as_view(),
        name="fhir-organization-detail",
    ),
    path("hl7/adt-a01/", HL7ADTAPIView.as_view(), name="hl7-adt-a01"),
    path("hl7/oru-r01/", HL7ORUAPIView.as_view(), name="hl7-oru-r01"),
]
