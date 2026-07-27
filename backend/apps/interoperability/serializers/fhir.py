"""
FHIR R4 resource serializers.

Converts internal clinical models into FHIR-compliant resource
dictionaries. This is a pragmatic subset (Patient, Encounter,
Observation, Practitioner, Organization) sufficient for basic
interoperability without external dependencies.
"""

from __future__ import annotations

from apps.clinical.encounters.models import Encounter
from apps.clinical.patients.models import Patient
from apps.clinical.providers.models import Provider
from apps.platform.organizations.models import Organization


def patient_to_fhir(
    patient: Patient,
) -> dict:
    """Serialize a patient to a FHIR Patient resource."""

    return {
        "resourceType": "Patient",
        "id": str(patient.id),
        "active": patient.is_active,
        "name": [
            {
                "use": "official",
                "family": patient.last_name,
                "given": [patient.first_name],
            }
        ],
        "gender": (patient.gender or "unknown").lower(),
        "birthDate": (
            patient.date_of_birth.isoformat() if patient.date_of_birth else None
        ),
        "identifier": [
            {
                "system": "urn:datavion:mrn",
                "value": patient.mrn,
            }
        ],
    }


def encounter_to_fhir(
    encounter: Encounter,
) -> dict:
    """Serialize an encounter to a FHIR Encounter resource."""

    return {
        "resourceType": "Encounter",
        "id": str(encounter.id),
        "status": "finished" if encounter.ended_at else "in-progress",
        "class": {
            "system": ("http://terminology.hl7.org/CodeSystem/v3-ActCode"),
            "code": "AMB",
        },
        "subject": {
            "reference": f"Patient/{encounter.patient_id}",
        },
        "period": {
            "start": (
                encounter.started_at.isoformat() if encounter.started_at else None
            ),
            "end": (encounter.ended_at.isoformat() if encounter.ended_at else None),
        },
    }


def provider_to_fhir(
    provider: Provider,
) -> dict:
    """Serialize a provider to a FHIR Practitioner resource."""

    return {
        "resourceType": "Practitioner",
        "id": str(provider.id),
        "active": provider.is_active,
        "name": [
            {
                "use": "official",
                "text": getattr(provider, "full_name", str(provider)),
            }
        ],
        "identifier": [
            {
                "system": "urn:datavion:provider",
                "value": provider.provider_number,
            }
        ],
    }


def organization_to_fhir(
    organization: Organization,
) -> dict:
    """Serialize an organization to a FHIR Organization resource."""

    return {
        "resourceType": "Organization",
        "id": str(organization.id),
        "active": organization.is_active,
        "name": organization.name,
        "identifier": [
            {
                "system": "urn:datavion:org",
                "value": organization.code,
            }
        ],
    }


__all__ = [
    "encounter_to_fhir",
    "organization_to_fhir",
    "patient_to_fhir",
    "provider_to_fhir",
]
