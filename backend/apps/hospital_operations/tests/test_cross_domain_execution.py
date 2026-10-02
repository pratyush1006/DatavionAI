from __future__ import annotations

import inspect
from pathlib import Path

from django.test import SimpleTestCase


class HospitalOperationsCrossDomainExecutionTests(SimpleTestCase):
    """Certification of the concrete cross-domain execution boundary."""

    def test_cross_domain_adapter_module_exists(self):
        from apps.hospital_operations import cross_domain

        required = {
            "create_encounter",
            "create_laboratory_order",
            "create_imaging_order",
            "create_pharmacy_order",
            "create_rcm_charge",
            "execute_notification",
            "execute_audit",
            "execute_ai",
        }
        assert required <= set(dir(cross_domain))

    def test_cross_domain_adapters_have_explicit_contracts(self):
        from apps.hospital_operations import cross_domain

        expected = {
            "create_encounter": {"organization", "patient", "provider", "appointment"},
            "create_laboratory_order": {
                "organization",
                "patient",
                "provider",
                "encounter",
            },
            "create_imaging_order": {"tenant", "patient", "provider", "encounter"},
            "create_pharmacy_order": {
                "organization",
                "patient",
                "provider",
                "encounter",
            },
            "create_rcm_charge": {"actor", "tenant", "organization", "patient"},
            "execute_notification": {"patient"},
            "execute_audit": {"organization", "actor", "admission"},
            "execute_ai": {"tenant", "organization", "patient", "admission"},
        }
        for name, parameters in expected.items():
            signature = inspect.signature(getattr(cross_domain, name))
            assert parameters <= set(signature.parameters)

    def test_adapters_reference_canonical_domains_only(self):
        text = Path("apps/hospital_operations/cross_domain.py").read_text(
            encoding="utf-8"
        )
        for contract in (
            "apps.clinical.encounters",
            "apps.clinical.laboratories",
            "apps.imaging.services.orders",
            "apps.pharmacy.services.dispensing",
            "apps.revenue_cycle.charge_capture.services",
            "apps.common.notifications.channels",
            "apps.platform.audit.services.audit",
            "apps.ai.services.chat",
        ):
            assert contract in text
        assert "apps.datavionos" not in text

    def test_adapters_do_not_implement_autonomous_clinical_action(self):
        text = Path("apps/hospital_operations/ai.py").read_text(encoding="utf-8")
        assert "AUTONOMOUS_CLINICAL_ACTION = False" in text
        assert "autonomous_clinical_action = AUTONOMOUS_CLINICAL_ACTION" in text
