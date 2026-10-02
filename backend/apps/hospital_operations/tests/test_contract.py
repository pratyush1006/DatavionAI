from pathlib import Path

from django.test import SimpleTestCase


class HospitalOperationsContractTests(SimpleTestCase):
    def test_models_and_ai_contract(self):
        from apps.hospital_operations.ai import ALLOWED_CAPABILITIES
        from apps.hospital_operations.models import (
            Admission,
            Bed,
            BedAssignment,
            BedReservation,
            Facility,
            OPDQueue,
            OPDVisit,
            OperationalEvent,
            OperationalUnit,
            PatientMovement,
            Room,
        )

        assert all(
            (
                Admission,
                Bed,
                BedAssignment,
                BedReservation,
                Facility,
                OPDQueue,
                OPDVisit,
                OperationalEvent,
                OperationalUnit,
                PatientMovement,
                Room,
            )
        )
        assert "bed_capacity_forecast" in ALLOWED_CAPABILITIES
        assert "opd_queue_summary" in ALLOWED_CAPABILITIES

    def test_ai_is_advisory(self):
        text = Path("apps/hospital_operations/ai.py").read_text(encoding="utf-8")
        assert "cannot autonomously assign beds" in text
        assert "autonomous_clinical_action" in text

    def test_transactional_hardening_is_present(self):
        text = Path("apps/hospital_operations/services.py").read_text(encoding="utf-8")
        assert "select_for_update" in text
        assert "@transaction.atomic" in text
        assert "register_opd_visit" in text
        assert "reserve_bed" in text
        assert "transfer_patient" in text
        assert "discharge_patient" in text

    def test_rbac_contract_is_canonical(self):
        from apps.hospital_operations.constants import RBAC_PERMISSIONS

        assert RBAC_PERMISSIONS["view"] == "hospital_operations.view"
        assert RBAC_PERMISSIONS["manage"] == "hospital_operations.manage"
        assert RBAC_PERMISSIONS["admit"] == "hospital_operations.admit"
        assert RBAC_PERMISSIONS["transfer"] == "hospital_operations.transfer"
        assert RBAC_PERMISSIONS["discharge"] == "hospital_operations.discharge"
        assert RBAC_PERMISSIONS["manage_opd"] == "hospital_operations.manage_opd"

    def test_cross_scope_guards_are_present(self):
        text = Path("apps/hospital_operations/services.py").read_text(encoding="utf-8")
        assert "outside the active scope" in text
        assert "tenant_id != tenant.id" in text
        assert "organization_id != organization.id" in text

    def test_canonical_integration_registry(self):
        from apps.hospital_operations.integrations import INTEGRATIONS

        assert {item.key for item in INTEGRATIONS} == {
            "patient",
            "encounters",
            "laboratory",
            "pharmacy",
            "imaging",
            "rcm",
            "notifications",
            "audit",
            "ai",
        }

    def test_canonical_patient_boundary(self):
        from django.apps import apps

        model = apps.get_model("patient_core", "Patient")
        assert model._meta.label == "patient_core.Patient"
        assert model.__module__ == "apps.patient_management.patients.models.patient"

    def test_family_members_is_not_targeted(self):
        installer = Path("installer_hospital_operations_end_to_end.py").read_text(
            encoding="utf-8"
        )
        assert "family_members" in installer.lower()
        assert "FAMILY MEMBERS: UNTOUCHED" in installer
