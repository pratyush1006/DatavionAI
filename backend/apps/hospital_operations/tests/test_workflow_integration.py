from django.test import SimpleTestCase

from apps.hospital_operations.integrations import (
    INTEGRATIONS,
    validate_canonical_integrations,
)
from apps.hospital_operations.workflow import (
    EXTERNAL_BOUNDARIES,
    WORKFLOW_STAGES,
    validate_workflow_boundaries,
)


class HospitalWorkflowIntegrationTests(SimpleTestCase):
    def test_full_workflow_stage_contract(self):
        assert WORKFLOW_STAGES == (
            "patient",
            "opd",
            "encounter",
            "admission",
            "bed",
            "ward_icu",
            "laboratory",
            "imaging",
            "pharmacy",
            "rcm",
            "discharge",
            "notifications",
            "audit",
            "ai",
        )

    def test_external_boundaries_are_canonical(self):
        assert EXTERNAL_BOUNDARIES == {
            "encounter": "encounters",
            "laboratory": "laboratory",
            "imaging": "imaging",
            "pharmacy": "pharmacy",
            "rcm": "rcm",
            "notifications": "notifications",
            "audit": "audit",
            "ai": "ai",
        }

    def test_all_boundaries_resolve(self):
        validate_canonical_integrations()
        resolved = validate_workflow_boundaries()
        assert set(resolved) == set(EXTERNAL_BOUNDARIES)
        assert all(resolved.values())

    def test_registry_has_every_required_boundary(self):
        keys = {item.key for item in INTEGRATIONS}
        assert {
            "patient",
            "encounters",
            "laboratory",
            "pharmacy",
            "imaging",
            "rcm",
            "notifications",
            "audit",
            "ai",
        } <= keys

    def test_api_workflow_contract(self):
        from apps.hospital_operations.api.urls import urlpatterns

        names = {pattern.name for pattern in urlpatterns}
        assert {
            "beds",
            "bed-reservations",
            "bed-assignments",
            "bed-cleaning-complete",
            "rooms",
            "opd-queue",
            "opd-register",
            "admission-create",
            "admission-transfer",
            "admission-discharge",
        } <= names

    def test_api_rbac_contract(self):
        from apps.hospital_operations.api.views import (
            AdmissionCreateView,
            AdmissionDischargeView,
            AdmissionTransferView,
            BedAssignmentCreateView,
            BedCleaningCompleteView,
            BedReservationCreateView,
            OPDRegistrationView,
        )

        assert AdmissionCreateView.rbac_permission == "admit"
        assert AdmissionTransferView.rbac_permission == "transfer"
        assert AdmissionDischargeView.rbac_permission == "discharge"
        assert BedAssignmentCreateView.rbac_permission == "manage"
        assert BedReservationCreateView.rbac_permission == "manage"
        assert BedCleaningCompleteView.rbac_permission == "manage"
        assert OPDRegistrationView.rbac_permission == "manage_opd"
