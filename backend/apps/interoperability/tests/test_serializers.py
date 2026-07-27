"""
Smoke tests for the interoperability serializers.
"""

from __future__ import annotations

from apps.common.tests.base import BaseTestCase
from apps.interoperability.serializers.fhir import (
    encounter_to_fhir,
    patient_to_fhir,
    provider_to_fhir,
)
from apps.interoperability.serializers.hl7 import (
    build_adt_a01,
    build_oru_r01,
)


class FhirSerializerTestCase(BaseTestCase):
    """
    Verify FHIR serialization produces valid resource shapes.
    """

    def test_patient_to_fhir(self) -> None:
        patient = self.create_patient(
            first_name="Jane",
            last_name="Doe",
            gender="female",
            date_of_birth=__import__("datetime").date(1990, 1, 1),
        )

        resource = patient_to_fhir(patient)

        self.assertEqual(resource["resourceType"], "Patient")
        self.assertEqual(resource["name"][0]["family"], "Doe")
        self.assertEqual(resource["gender"], "female")

    def test_encounter_to_fhir(self) -> None:
        encounter = self.create_encounter()

        resource = encounter_to_fhir(encounter)

        self.assertEqual(resource["resourceType"], "Encounter")
        self.assertEqual(
            resource["subject"]["reference"],
            f"Patient/{encounter.patient_id}",
        )

    def test_provider_to_fhir(self) -> None:
        provider = self.create_provider()

        resource = provider_to_fhir(provider)

        self.assertEqual(resource["resourceType"], "Practitioner")


class Hl7SerializerTestCase(BaseTestCase):
    """
    Verify HL7 v2 message builders emit expected segments.
    """

    def test_build_adt_a01(self) -> None:
        message = build_adt_a01(
            sending_app="DATVION",
            sending_facility="ORG",
            patient_id="P1",
            patient_name="Doe^Jane",
            gender="F",
        )

        segments = message.split("\r")
        self.assertTrue(segments[0].startswith("MSH|"))
        self.assertTrue(any(s.startswith("PID|") for s in segments))

    def test_build_oru_r01(self) -> None:
        message = build_oru_r01(
            sending_app="DATVION",
            sending_facility="ORG",
            patient_id="P1",
            observation_id="HR",
            value="72",
        )

        segments = message.split("\r")
        self.assertTrue(any(s.startswith("OBX|") for s in segments))
