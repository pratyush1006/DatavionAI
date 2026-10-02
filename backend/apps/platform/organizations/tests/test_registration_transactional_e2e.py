import inspect
import json
from importlib import import_module

from django.test import TransactionTestCase

CANONICAL_MODULES = {
    "organization_creation": "apps.platform.organizations.workflows.organization_creation",
    "organization_onboarding": "apps.platform.organizations.workflows.organization_onboarding",
    "saas_provisioning": "apps.platform.organizations.services.saas_provisioning",
    "organization_module": "apps.platform.organizations.services.organization_module",
    "module_management": "apps.platform.organizations.workflows.module_management",
    "feature_management": "apps.platform.organizations.workflows.feature_management",
    "billing_registration": "apps.platform.saas_billing.workflows.registration",
    "subscription_service": "apps.platform.saas_billing.services.subscription_service",
    "entitlement_service": "apps.platform.saas_billing.services.entitlement_service",
    "entitlement_selector": "apps.platform.saas_billing.selectors.entitlement_selector",
    "tenant_service": "apps.platform.tenancy.services.tenant",
    "membership_service": "apps.platform.tenancy.services.membership",
    "tenant_context": "apps.platform.tenancy.context",
}
MODEL_MODULES = (
    "apps.platform.organizations.models.organization",
    "apps.platform.organizations.models.organization_module",
    "apps.platform.organizations.models.organization_feature",
    "apps.platform.saas_billing.models.plan",
    "apps.platform.saas_billing.models.subscription",
    "apps.platform.tenancy.models.tenant",
    "apps.platform.tenancy.models.membership",
)
TOKENS = (
    "register",
    "registration",
    "create",
    "onboard",
    "provision",
    "subscribe",
    "subscription",
    "entitlement",
    "tenant",
    "membership",
)


def public_callables(module):
    found = {}
    for name, value in vars(module).items():
        if name.startswith("_"):
            continue
        if inspect.isfunction(value) or inspect.isclass(value):
            try:
                signature = str(inspect.signature(value))
            except (TypeError, ValueError):
                signature = "<signature unavailable>"
            if any(token in name.lower() for token in TOKENS):
                found[name] = signature
    return found


class RegistrationTransactionalRuntimeProbe(TransactionTestCase):
    reset_sequences = False

    def test_canonical_runtime_contract(self):
        failures = []
        modules = {}
        models = {}

        for owner, module_name in CANONICAL_MODULES.items():
            try:
                module = import_module(module_name)
                modules[owner] = {
                    "module": module_name,
                    "callables": public_callables(module),
                }
            except Exception as exc:
                failures.append(
                    {
                        "owner": owner,
                        "module": module_name,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

        for module_name in MODEL_MODULES:
            try:
                module = import_module(module_name)
            except Exception as exc:
                failures.append(
                    {
                        "module": module_name,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
                continue

            for name, value in vars(module).items():
                meta = getattr(value, "_meta", None)
                if meta is None or not getattr(meta, "managed", False):
                    continue
                try:
                    models[f"{module_name}:{name}"] = {
                        "db_table": meta.db_table,
                        "fields": [
                            {
                                "name": field.name,
                                "type": field.__class__.__name__,
                                "null": getattr(field, "null", None),
                                "blank": getattr(field, "blank", None),
                                "has_default": getattr(
                                    field, "has_default", lambda: False
                                )(),
                            }
                            for field in meta.get_fields()
                            if not getattr(field, "auto_created", False)
                        ],
                    }
                except Exception as exc:
                    failures.append(
                        {
                            "model": f"{module_name}:{name}",
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )

        payload = {
            "modules": modules,
            "models": models,
            "failures": failures,
        }

        self.assertFalse(
            failures,
            msg=json.dumps(payload, indent=2, default=str),
        )
