from __future__ import annotations

import inspect
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from importlib import import_module
from typing import Any
from uuid import uuid4

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import TransactionTestCase

PREFIX = "E2E-RCM-V2"
TODAY = date.today() + timedelta(days=1)
NOW = datetime(2026, 9, 10, 12, 0, tzinfo=UTC)


def model_by_candidates(*labels: str):
    last_error = None
    for label in labels:
        try:
            model = apps.get_model(label)
            if model is not None:
                return model
        except (LookupError, ValueError) as exc:
            last_error = exc
    raise AssertionError(
        "Unable to resolve model from candidates: "
        + ", ".join(labels)
        + f". Last error: {last_error}"
    )


def model_fields(model):
    return {field.name: field for field in model._meta.fields}


def field_default(field):
    from django.db import models

    if field.default is models.NOT_PROVIDED:
        return None
    if callable(field.default):
        try:
            return field.default()
        except Exception:
            return None
    return field.default


def scalar_for_field(field, name: str):
    lowered = name.lower()

    if field.choices:
        first = next(iter(field.choices), None)
        if first is not None:
            return first[0]

    default = field_default(field)
    if default is not None:
        return default

    if field.is_relation:
        return None

    internal = field.get_internal_type()

    if "Boolean" in internal:
        return True
    if "Integer" in internal:
        return 1
    if "Decimal" in internal:
        return Decimal("1.00")
    if "DateTime" in internal:
        return NOW
    if internal == "DateField":
        return TODAY
    if internal == "JSONField":
        return {}
    if internal == "UUIDField":
        return uuid4()
    if "Email" in internal:
        return f"{PREFIX.lower()}@datavion.ai"
    if "Text" in internal or "Char" in internal:
        if "email" in lowered:
            return f"{PREFIX.lower()}@datavion.ai"
        if "phone" in lowered:
            return "+919876543210"
        if "mrn" in lowered:
            return f"{PREFIX}-MRN"
        if "code" in lowered:
            return f"{PREFIX}-CODE"
        if "number" in lowered:
            return f"{PREFIX}-NUM"
        if "name" in lowered:
            return f"{PREFIX} TEST"
        if "reference" in lowered:
            return f"{PREFIX}-REF"
        if "description" in lowered:
            return "Deterministic Revenue Cycle E2E fixture"
        if "reason" in lowered or "note" in lowered:
            return "Deterministic E2E test"
        return f"{PREFIX}-{name.upper()[:24]}"

    return None


def create_generic(model, overrides=None, *, depth=0):
    overrides = dict(overrides or {})
    fields = model_fields(model)
    values = {}

    for name, field in fields.items():
        if field.primary_key or getattr(field, "auto_created", False):
            continue

        if name in overrides:
            values[name] = overrides[name]
            continue

        if field.is_relation:
            if field.null or field.blank:
                continue

            remote = field.remote_field.model
            remote_label = remote._meta.label_lower

            if (
                remote_label
                in {
                    "organizations.organization",
                    "organization.organization",
                }
                and depth < 4
            ):
                values[name] = create_generic(remote, {}, depth=depth + 1)
                continue

            if remote_label.endswith(".tenant") and depth < 4:
                values[name] = create_generic(
                    remote,
                    {
                        "name": f"{PREFIX} Tenant",
                        "code": f"{PREFIX}-TEN",
                        "slug": f"{PREFIX.lower()}-tenant",
                    },
                    depth=depth + 1,
                )
                continue

            if remote is get_user_model():
                continue

            raise AssertionError(
                f"No deterministic fixture mapping for required relation "
                f"{model._meta.label_lower}.{name} -> {remote_label}"
            )

        value = scalar_for_field(field, name)
        from django.db import models

        if (
            value is None
            and field.default is models.NOT_PROVIDED
            and not field.null
            and not field.blank
        ):
            raise AssertionError(
                f"No deterministic fixture value for required field "
                f"{model._meta.label_lower}.{name}"
            )
        if value is not None:
            values[name] = value

    try:
        return model.objects.create(**values)
    except Exception as exc:
        raise AssertionError(
            f"Unable to create fixture {model._meta.label_lower}: {exc}. "
            f"Values={values!r}"
        ) from exc


def create_tenant():
    Tenant = model_by_candidates(
        "tenancy.tenant",
    )
    fields = model_fields(Tenant)
    overrides = {}
    if "name" in fields:
        overrides["name"] = f"{PREFIX} Tenant"
    if "code" in fields:
        overrides["code"] = f"{PREFIX}-TEN"
    if "slug" in fields:
        overrides["slug"] = f"{PREFIX.lower()}-tenant"
    return create_generic(Tenant, overrides)


def create_organization(tenant):
    Organization = model_by_candidates(
        "organizations.organization",
        "organization.organization",
    )
    fields = model_fields(Organization)
    overrides = {}
    if "tenant" in fields:
        overrides["tenant"] = tenant
    if "name" in fields:
        overrides["name"] = f"{PREFIX} Organization"
    if "code" in fields:
        overrides["code"] = f"{PREFIX}-ORG"
    if "slug" in fields:
        overrides["slug"] = f"{PREFIX.lower()}-org"
    return create_generic(Organization, overrides)


def create_actor(organization, tenant):
    User = get_user_model()
    fields = model_fields(User)
    email = f"{PREFIX.lower()}@datavion.ai"

    lookup = {"email": email} if "email" in fields else {}
    if lookup:
        existing = User.objects.filter(**lookup).first()
        if existing:
            return existing

    base = {}
    if "email" in fields:
        base["email"] = email
    if "username" in fields:
        base["username"] = f"{PREFIX.lower()}_user"
    if "first_name" in fields:
        base["first_name"] = "RCM"
    if "last_name" in fields:
        base["last_name"] = "E2E"
    if "is_active" in fields:
        base["is_active"] = True
    if "tenant" in fields:
        base["tenant"] = tenant
    if "organization" in fields:
        base["organization"] = organization

    try:
        manager = User.objects
        create_user = getattr(manager, "create_user", None)
        if create_user:
            return create_user(password="E2E-password-123!", **base)

        actor = manager.create(**base)
        if hasattr(actor, "set_password"):
            actor.set_password("E2E-password-123!")
            actor.save(update_fields=["password"])
        return actor
    except Exception as exc:
        raise AssertionError(f"Unable to create E2E actor: {exc}") from exc


def create_patient(organization):
    Patient = model_by_candidates("patient_core.patient", "patients.patient")
    fields = model_fields(Patient)
    overrides = {"organization": organization}

    if "mrn" in fields:
        overrides["mrn"] = f"{PREFIX}-MRN"
    if "first_name" in fields:
        overrides["first_name"] = "RCM"
    if "last_name" in fields:
        overrides["last_name"] = "E2E"
    if "date_of_birth" in fields:
        overrides["date_of_birth"] = date(1985, 1, 15)
    if "is_active" in fields:
        overrides["is_active"] = True
    if "status" in fields and fields["status"].choices:
        values = [value for value, _ in fields["status"].choices]
        for candidate in ("ACTIVE", "active"):
            if candidate in values:
                overrides["status"] = candidate
                break

    return create_generic(Patient, overrides)


def first_choice(model, field_name, preferred=()):
    field = model_fields(model).get(field_name)
    if not field or not field.choices:
        return preferred[0] if preferred else None
    values = [value for value, _ in field.choices]
    for item in preferred:
        if item in values:
            return item
    return values[0]


def call_with_contract(obj, method_name, candidates):
    method = getattr(obj, method_name, None)
    if not callable(method):
        raise AssertionError(f"Live callable missing: {obj}.{method_name}")

    sig = inspect.signature(method)
    kwargs = {}
    unresolved = []

    for name, parameter in sig.parameters.items():
        if parameter.kind in {
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        }:
            continue
        if name in candidates:
            kwargs[name] = candidates[name]
        elif parameter.default is inspect.Parameter.empty:
            unresolved.append(name)

    if unresolved:
        raise AssertionError(
            f"Unable to bind {obj.__name__}.{method_name}{sig}. "
            f"Missing required payload values: {unresolved}. "
            f"Available candidates: {sorted(candidates)}"
        )

    return method(**kwargs)


def _literal_string_values(node):
    values = []
    if isinstance(node, __import__("ast").Constant) and isinstance(node.value, str):
        values.append(node.value)
    elif isinstance(
        node, (__import__("ast").Tuple, __import__("ast").List, __import__("ast").Set)
    ):
        for item in node.elts:
            values.extend(_literal_string_values(item))
    elif isinstance(node, __import__("ast").Dict):
        for key in node.keys:
            if key is not None:
                values.extend(_literal_string_values(key))
        for value in node.values:
            values.extend(_literal_string_values(value))
    return values


def resolve_ar_transaction_types(ARService):
    """Discover accepted transaction types from the live service/model contract."""
    import ast
    import inspect

    discovered = []
    method = getattr(ARService, "post_transaction", None)
    if callable(method):
        try:
            source = inspect.getsource(method)
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Compare):
                    for comparator in node.comparators:
                        if isinstance(comparator, (ast.Set, ast.Tuple, ast.List)):
                            discovered.extend(_literal_string_values(comparator))
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr in {"get", "__getitem__"}
                ):
                    discovered.extend(_literal_string_values(node))
        except (OSError, TypeError, SyntaxError):
            pass

    try:
        ARTransaction = model_by_candidates("revenue_cycle.artransaction")
        field = model_fields(ARTransaction).get("transaction_type")
        if field and field.choices:
            discovered.extend(str(value) for value, _label in field.choices)
    except Exception:
        pass

    # Inspect likely module-level constants without assuming a particular name.
    try:
        module = import_module(ARService.__module__)
        for name, value in vars(module).items():
            if "TRANSACTION" not in name.upper():
                continue
            if isinstance(value, (set, tuple, list, frozenset)):
                discovered.extend(str(item) for item in value if isinstance(item, str))
    except Exception:
        pass

    result = []
    for value in discovered:
        value = str(value)
        if value and value not in result:
            result.append(value)
    return result


def post_ar_transaction(ARService, state):
    """Post one AR transaction using the live accepted transaction-type contract."""
    candidates = resolve_ar_transaction_types(ARService)
    if not candidates:
        candidates = [
            "DEBIT",
            "CREDIT",
            "PAYMENT",
            "ADJUSTMENT",
            "REFUND",
            "CHARGE",
            "DENIAL",
            "INSURANCE_PAYMENT",
            "WRITE_OFF",
            "debit",
            "credit",
            "payment",
            "adjustment",
            "refund",
            "denial",
            "insurance_payment",
            "write_off",
        ]

    errors = []
    for index, transaction_type in enumerate(candidates):
        try:
            with transaction.atomic():
                return ARService.post_transaction(
                    organization=state.organization,
                    account_id=state.ar_account.id,
                    transaction_type=transaction_type,
                    amount=Decimal("20.00"),
                    transaction_number=f"{PREFIX}-AR-TX-{index}",
                    transaction_date=NOW,
                    actor=state.actor,
                    source_type="denial",
                    source_id=state.denial.id,
                    external_reference=f"{PREFIX}-AR-REF",
                    note="Deterministic denial balance",
                )
        except ValueError as exc:
            if "Unsupported Accounts Receivable transaction type" in str(exc):
                errors.append(f"{transaction_type!r}: {exc}")
                continue
            raise

    raise AssertionError(
        "Unable to determine an accepted Accounts Receivable transaction type. "
        f"Discovered candidates={candidates!r}; errors={errors!r}"
    )


def resolve_analytics_period():
    """Resolve an accepted Revenue Analytics period from the live enum contract."""
    from importlib import import_module

    discovered = []
    try:
        constants = import_module("apps.revenue_cycle.revenue_analytics.constants")
        enum_cls = getattr(constants, "AnalyticsPeriod", None)
        if enum_cls is not None:
            values = getattr(enum_cls, "values", None)
            if values:
                discovered.extend(str(value) for value in values)
            members = getattr(enum_cls, "__members__", {})
            for member in members.values():
                value = getattr(member, "value", None)
                if isinstance(value, str):
                    discovered.append(value)
    except Exception:
        pass

    preferred = ("monthly", "MONTHLY", "month", "MONTH")
    ordered = []
    for candidate in preferred:
        if candidate in discovered and candidate not in ordered:
            ordered.append(candidate)
    for candidate in discovered:
        if candidate not in ordered:
            ordered.append(candidate)

    if ordered:
        return ordered[0]
    return "monthly"


def create_revenue_analytics_snapshot(RevenueAnalyticsService, state):
    """Create one analytics snapshot using the live accepted period contract."""
    candidates = []
    resolved = resolve_analytics_period()
    if resolved:
        candidates.append(resolved)

    for candidate in (
        "monthly",
        "MONTHLY",
        "month",
        "MONTH",
        "quarterly",
        "QUARTERLY",
        "quarter",
        "QUARTER",
        "yearly",
        "YEARLY",
        "year",
        "YEAR",
    ):
        if candidate not in candidates:
            candidates.append(candidate)

    errors = []
    for period in candidates:
        try:
            with transaction.atomic():
                return RevenueAnalyticsService.create_snapshot(
                    organization=state.organization,
                    period=period,
                    period_start=date(2026, 9, 1),
                    period_end=date(2026, 9, 30),
                    gross_charges=Decimal("100.00"),
                    payments=Decimal("80.00"),
                    adjustments=Decimal("20.00"),
                    denials=Decimal("20.00"),
                    write_offs=Decimal("0.00"),
                    outstanding_ar=Decimal("20.00"),
                    encounter_count=1,
                    claim_count=1,
                    denied_claim_count=1,
                    paid_claim_count=1,
                    actor=state.actor,
                )
        except ValueError as exc:
            if "Unsupported analytics period" in str(exc):
                errors.append(f"{period!r}: {exc}")
                continue
            raise

    raise AssertionError(
        "Unable to determine an accepted Revenue Analytics period. "
        f"Candidates={candidates!r}; errors={errors!r}"
    )


def assert_scope(organization, patient, obj):
    if hasattr(obj, "organization_id"):
        assert obj.organization_id == organization.id, (
            f"Organization mismatch for {obj!r}"
        )
    if patient is not None and hasattr(obj, "patient_id"):
        if obj.patient_id is not None:
            assert obj.patient_id == patient.id, f"Patient mismatch for {obj!r}"


@dataclass
class State:
    tenant: Any
    organization: Any
    actor: Any
    patient: Any
    payer: Any = None
    tpa: Any = None
    plan: Any = None
    product: Any = None
    subscriber: Any = None
    enrollment: Any = None
    benefit: Any = None
    cob: Any = None
    verification: Any = None
    eligibility: Any = None
    prior_authorization: Any = None
    charge: Any = None
    coding: Any = None
    scrub: Any = None
    submission: Any = None
    era: Any = None
    payment: Any = None
    denial: Any = None
    appeal: Any = None
    ar_account: Any = None
    ar_transaction: Any = None
    analytics: Any = None


class InsuranceRevenueCycleTransactionalE2ETests(TransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        tenant = create_tenant()
        organization = create_organization(tenant)
        actor = create_actor(organization, tenant)
        patient = create_patient(organization)
        self.state = State(tenant, organization, actor, patient)

    def test_full_business_chain(self):
        s = self.state

        # Insurance master data: deterministic test fixtures only.
        Payer = model_by_candidates("insurance.payer")
        TPA = model_by_candidates("insurance.tpa")
        Plan = model_by_candidates("insurance.insuranceplan")
        Product = model_by_candidates("insurance.planproduct")
        Subscriber = model_by_candidates("insurance.subscriber")
        Enrollment = model_by_candidates("insurance.enrollment")
        Benefit = model_by_candidates("insurance.benefit")
        COB = model_by_candidates("insurance.coordinationofbenefits")
        Relationship = model_by_candidates("insurance.payerTPARelationship")

        s.payer = create_generic(
            Payer,
            {
                "organization": s.organization,
                "legal_name": "E2E Payer",
                "display_name": "E2E Payer",
                "payer_code": f"{PREFIX}-PAY",
                "electronic_payer_id": f"{PREFIX}PAYER",
                "payer_type": "private",
                "active": True,
            },
        )
        s.tpa = create_generic(
            TPA,
            {
                "organization": s.organization,
                "legal_name": "E2E TPA",
                "display_name": "E2E TPA",
                "tpa_code": f"{PREFIX}-TPA",
                "electronic_identifier": f"{PREFIX}TPA",
                "tpa_type": "tpa",
                "active": True,
            },
        )
        create_generic(
            Relationship,
            {
                "organization": s.organization,
                "payer": s.payer,
                "tpa": s.tpa,
                "status": "active",
            },
        )
        s.plan = create_generic(
            Plan,
            {
                "organization": s.organization,
                "payer": s.payer,
                "name": "E2E Commercial Plan",
                "plan_code": f"{PREFIX}-PLAN",
                "insurance_type": "private",
                "is_active": True,
            },
        )
        s.product = create_generic(
            Product,
            {
                "plan": s.plan,
                "name": "E2E Medical Product",
                "product_code": f"{PREFIX}-PROD",
                "is_active": True,
            },
        )
        s.subscriber = create_generic(
            Subscriber,
            {
                "organization": s.organization,
                "patient": s.patient,
                "member_id": f"{PREFIX}-MEM",
                "first_name": "RCM",
                "last_name": "E2E",
            },
        )
        s.enrollment = create_generic(
            Enrollment,
            {
                "organization": s.organization,
                "patient": s.patient,
                "plan": s.plan,
                "product": s.product,
                "subscriber": s.subscriber,
                "member_id": f"{PREFIX}-MEM",
                "policy_number": f"{PREFIX}-POLICY",
                "group_number": f"{PREFIX}-GROUP",
                "relationship_to_subscriber": "self",
                "effective_date": date(2026, 1, 1),
                "status": "active",
                "is_primary": True,
            },
        )
        s.benefit = create_generic(
            Benefit,
            {
                "product": s.product,
                "category": "medical",
                "service_type": "outpatient",
                "coverage_percent": Decimal("80.00"),
                "copay_amount": Decimal("20.00"),
                "deductible_amount": Decimal("500.00"),
                "authorization_required": True,
                "effective_date": date(2026, 1, 1),
            },
        )
        s.cob = create_generic(
            COB,
            {
                "organization": s.organization,
                "enrollment": s.enrollment,
                "coordination_order": 1,
                "responsibility": "primary",
            },
        )

        payer_id = str(s.payer.id)
        member_id = s.enrollment.member_id

        # Insurance Verification
        iv_module = import_module("apps.revenue_cycle.insurance_verification.services")
        iv = getattr(iv_module, "InsuranceVerificationService", None)
        if iv is None:
            raise AssertionError(
                "InsuranceVerificationService unavailable in live runtime."
            )
        s.verification = call_with_contract(
            iv,
            "create",
            {
                "organization_id": s.organization.id,
                "patient_id": s.patient.id,
                "request_reference": f"{PREFIX}-IV-REQ",
                "idempotency_key": f"{PREFIX}-IV-IDEM",
                "payer_id": payer_id,
                "member_id": member_id,
                "data": {
                    "payer_name": s.payer.display_name,
                    "policy_number": s.enrollment.policy_number,
                    "group_number": s.enrollment.group_number,
                    "subscriber_name": "RCM E2E",
                    "subscriber_relationship": "self",
                    "verification_method": "electronic",
                    "response_payload": {},
                },
            },
        )
        assert_scope(s.organization, s.patient, s.verification)

        # Eligibility
        from apps.revenue_cycle.eligibility.services import EligibilityService

        s.eligibility = EligibilityService.create(
            patient=s.patient,
            organization=s.organization,
            performed_by=s.actor,
            payer_id=payer_id,
            payer_name=s.payer.display_name,
            member_id=member_id,
            group_number=s.enrollment.group_number,
            subscriber_name="RCM E2E",
            subscriber_relationship="self",
            request_reference=f"{PREFIX}-ELIG-REQ",
            idempotency_key=f"{PREFIX}-ELIG-IDEM",
            response_payload={},
        )
        assert s.eligibility.status == "pending"

        # Prior Authorization — bind from the live signature.
        pa = None
        for module_name in (
            "apps.revenue_cycle.prior_authorization.services",
            "apps.revenue_cycle.prior_authorization.services.prior_authorization",
        ):
            try:
                module = import_module(module_name)
            except Exception:
                continue
            pa = getattr(module, "PriorAuthorizationService", None)
            if pa is not None:
                break

        if pa is None:
            raise AssertionError("PriorAuthorizationService unavailable.")

        s.prior_authorization = call_with_contract(
            pa,
            "create",
            {
                "organization_id": s.organization.id,
                "patient_id": s.patient.id,
                "payer_id": payer_id,
                "member_id": member_id,
                "procedure_code": "99213",
                "request_reference": f"{PREFIX}-PA-REQ",
                "idempotency_key": f"{PREFIX}-PA-IDEM",
                "data": {
                    "payer_name": s.payer.display_name,
                    "group_number": s.enrollment.group_number,
                    "requested_units": 1,
                    "requested_amount": Decimal("100.00"),
                    "requested_service_date": date.today() + timedelta(days=1),
                    "authorization_number": f"{PREFIX}-AUTH",
                },
            },
        )
        assert_scope(s.organization, s.patient, s.prior_authorization)

        # Charge
        from apps.revenue_cycle.charge_capture.services import ChargeCaptureService

        s.charge = ChargeCaptureService.create(
            actor=s.actor,
            tenant_id=s.tenant.id,
            organization=s.organization,
            patient=s.patient,
            service_code="99213",
            description="E2E outpatient evaluation",
            quantity=Decimal("1"),
            unit_price=Decimal("100.00"),
            idempotency_key=f"{PREFIX}-CHARGE-IDEM",
        )
        assert_scope(s.organization, s.patient, s.charge)

        # Coding
        from apps.revenue_cycle.coding.services import CodingService

        s.coding = CodingService.create(
            organization=s.organization,
            tenant_id=s.tenant.id,
            patient=s.patient,
            actor=s.actor,
            idempotency_key=f"{PREFIX}-CODING-IDEM",
            source_reference=str(s.charge.id),
            service_date=TODAY,
            coding_type="professional",
            encounter_type="outpatient",
            clinical_summary="Deterministic E2E clinical summary",
            documentation={"source": "transactional_e2e_v2"},
            coding_notes="E2E coding fixture",
        )
        assert_scope(s.organization, s.patient, s.coding)

        # Claim Scrubbing — consume current protected production surface.
        from apps.revenue_cycle.claim_scrubbing.services import create_scrub

        s.scrub, s.scrub_findings = create_scrub(
            organization=s.organization,
            patient=s.patient,
            claim_reference=f"{PREFIX}-CLAIM",
            idempotency_key=f"{PREFIX}-SCRUB-IDEM",
            input_snapshot={
                "charge_id": str(s.charge.id),
                "coding_id": str(s.coding.id),
                "payer_id": payer_id,
            },
            user=s.actor,
        )
        assert_scope(s.organization, s.patient, s.scrub)

        # Claim Submission
        from apps.revenue_cycle.claim_submission.services import create_submission

        s.submission, created = create_submission(
            organization=s.organization,
            patient=s.patient,
            user=s.actor,
            claim_reference=f"{PREFIX}-CLAIM",
            payer_id=payer_id,
            payer_name=s.payer.display_name,
            submission_method="edi",
            idempotency_key=f"{PREFIX}-SUBMISSION-IDEM",
            payload={
                "charge_id": str(s.charge.id),
                "coding_id": str(s.coding.id),
                "scrub_id": str(s.scrub.id),
            },
        )
        self.assertTrue(created)
        assert_scope(s.organization, s.patient, s.submission)

        # ERA
        from apps.core.workflows import WorkflowContext
        from apps.revenue_cycle.era.workflows import (
            CreateERAWorkflow,
            ERAWorkflowRequest,
        )

        era_request = ERAWorkflowRequest(
            actor=s.actor,
            organization_id=s.organization.id,
            tenant_id=s.tenant.id,
            data={
                "patient_id": s.patient.id,
                "payer_name": s.payer.display_name,
                "payer_identifier": payer_id,
                "trace_number": f"{PREFIX}-TRACE",
                "check_or_eft_number": f"{PREFIX}-EFT",
                "source": "edi_835",
                "payment_amount": Decimal("80.00"),
                "adjustment_amount": Decimal("20.00"),
                "received_at": NOW,
                "external_reference": f"{PREFIX}-ERA-REF",
                "idempotency_key": f"{PREFIX}-ERA-IDEM",
                "raw_payload": {"claim_reference": f"{PREFIX}-CLAIM"},
                "notes": "Deterministic E2E ERA",
            },
        )
        era_context = WorkflowContext.create(
            tenant_id=s.tenant.id,
            actor_id=s.actor.id,
            workflow_name="revenue_cycle.era.create",
        )
        era_result = CreateERAWorkflow(
            logger_=None,
            payload=era_request,
        ).execute(
            context=era_context,
        )
        s.era = era_result.data
        assert_scope(s.organization, s.patient, s.era)

        # Payment Posting
        from apps.revenue_cycle.payment_posting.services import (
            create_payment_posting,
        )

        s.payment = create_payment_posting(
            organization=s.organization,
            patient=s.patient,
            data={
                "payer_name": s.payer.display_name,
                "payer_claim_reference": f"{PREFIX}-CLAIM",
                "source": "era",
                "status": "pending",
                "amount": Decimal("80.00"),
                "adjustment_amount": Decimal("20.00"),
                "external_reference": f"{PREFIX}-EFT",
                "idempotency_key": f"{PREFIX}-PAYMENT-IDEM",
                "notes": "Deterministic E2E payment",
            },
            actor=s.actor,
        )
        assert_scope(s.organization, s.patient, s.payment)

        # Denial
        from apps.revenue_cycle.denials.services import create_denial

        s.denial = create_denial(
            organization=s.organization,
            patient=s.patient,
            actor=s.actor,
            data={
                "claim_submission_id": s.submission.id,
                "external_claim_id": str(s.submission.id),
                "payer_name": s.payer.display_name,
                "received_at": NOW,
                "denial_code": "CO-45",
                "denial_reason": "Test denial for E2E appeal path",
                "amount": Decimal("20.00"),
                "priority": "normal",
                "external_reference": f"{PREFIX}-DENIAL-REF",
                "idempotency_key": f"{PREFIX}-DENIAL-IDEM",
                "metadata": {"e2e": True},
            },
        )
        assert_scope(s.organization, s.patient, s.denial)

        # Appeal
        from apps.revenue_cycle.appeals.services import AppealService

        s.appeal = AppealService.create(
            actor=s.actor,
            tenant_id=s.tenant.id,
            organization_id=s.organization.id,
            patient_id=s.patient.id,
            data={
                "claim_reference": f"{PREFIX}-CLAIM",
                "payer_name": s.payer.display_name,
                "appeal_number": f"{PREFIX}-APPEAL",
                "denial_reference": str(s.denial.id),
                "status": "draft",
                "priority": "normal",
                "reason": "Deterministic E2E appeal",
                "clinical_summary": "E2E appeal clinical summary",
                "requested_amount": Decimal("20.00"),
                "approved_amount": Decimal("0.00"),
                "idempotency_key": f"{PREFIX}-APPEAL-IDEM",
                "metadata": {"e2e": True},
            },
        )
        assert_scope(s.organization, s.patient, s.appeal)

        # AR
        from apps.revenue_cycle.accounts_receivable.services import ARService

        s.ar_account = ARService.create_account(
            organization=s.organization,
            patient=s.patient,
            account_number=f"{PREFIX}-AR",
            currency="INR",
            actor=s.actor,
        )
        s.ar_transaction = post_ar_transaction(ARService, s)

        # Revenue Analytics
        from apps.revenue_cycle.revenue_analytics.services import (
            RevenueAnalyticsService,
        )

        s.analytics = create_revenue_analytics_snapshot(
            RevenueAnalyticsService,
            s,
        )

        # Final persistence + organization/patient scope gate.
        representative_pairs = (
            (Payer, s.payer),
            (TPA, s.tpa),
            (Plan, s.plan),
            (Product, s.product),
            (Subscriber, s.subscriber),
            (Enrollment, s.enrollment),
            (Benefit, s.benefit),
            (COB, s.cob),
        )
        for model_cls, obj in representative_pairs:
            self.assertIsNotNone(obj)
            self.assertTrue(
                model_cls.objects.filter(pk=obj.pk).exists(),
                f"{model_cls._meta.label_lower} was not persisted",
            )
            persisted = model_cls.objects.get(pk=obj.pk)
            if hasattr(persisted, "organization_id"):
                self.assertEqual(
                    persisted.organization_id,
                    s.organization.id,
                    f"{model_cls._meta.label_lower} organization scope mismatch",
                )
            if hasattr(persisted, "patient_id") and persisted.patient_id is not None:
                self.assertEqual(
                    persisted.patient_id,
                    s.patient.id,
                    f"{model_cls._meta.label_lower} patient scope mismatch",
                )

        # Verify the commit callback boundary independently of business payloads.
        callback_state = []
        with transaction.atomic():
            transaction.on_commit(lambda: callback_state.append("committed"))
            self.assertEqual(callback_state, [])
        self.assertEqual(callback_state, ["committed"])

        # Final business-chain assertions.
        rcm_objects = (
            s.verification,
            s.eligibility,
            s.prior_authorization,
            s.charge,
            s.coding,
            s.scrub,
            s.submission,
            s.era,
            s.payment,
            s.denial,
            s.appeal,
            s.ar_account,
            s.ar_transaction,
            s.analytics,
        )
        for obj in rcm_objects:
            self.assertIsNotNone(obj)
            self.assertTrue(
                obj.__class__.objects.filter(pk=obj.pk).exists(),
                f"{obj.__class__._meta.label_lower} was not persisted",
            )
            if hasattr(obj, "organization_id"):
                self.assertEqual(obj.organization_id, s.organization.id)
            if hasattr(obj, "patient_id") and obj.patient_id is not None:
                self.assertEqual(obj.patient_id, s.patient.id)

        for name in (
            "payer",
            "tpa",
            "plan",
            "enrollment",
            "verification",
            "eligibility",
            "prior_authorization",
            "charge",
            "coding",
            "scrub",
            "submission",
            "era",
            "payment",
            "denial",
            "appeal",
            "ar_account",
            "analytics",
        ):
            self.assertIsNotNone(getattr(s, name), name)

    def test_commit_boundary(self):
        Charge = model_by_candidates("revenue_cycle.charge")
        marker = f"{PREFIX}-COMMIT-IDEM"
        with transaction.atomic():
            charge = Charge.objects.create(
                organization=self.state.organization,
                patient=self.state.patient,
                tenant_id=self.state.tenant.id,
                service_code="TX-COMMIT",
                description="commit boundary",
                quantity=Decimal("1"),
                unit_price=Decimal("1.00"),
                total_amount=Decimal("1.00"),
                status=first_choice(Charge, "status", ("captured", "pending")),
                idempotency_key=marker,
            )
        self.assertTrue(Charge.objects.filter(pk=charge.pk).exists())

    def test_rollback_boundary(self):
        Charge = model_by_candidates("revenue_cycle.charge")
        marker = f"{PREFIX}-ROLLBACK-IDEM"

        try:
            with transaction.atomic():
                Charge.objects.create(
                    organization=self.state.organization,
                    patient=self.state.patient,
                    tenant_id=self.state.tenant.id,
                    service_code="TX-ROLLBACK",
                    description="rollback boundary",
                    quantity=Decimal("1"),
                    unit_price=Decimal("2.00"),
                    total_amount=Decimal("2.00"),
                    status=first_choice(Charge, "status", ("captured", "pending")),
                    idempotency_key=marker,
                )
                raise RuntimeError("intentional rollback")
        except RuntimeError:
            pass

        self.assertFalse(Charge.objects.filter(idempotency_key=marker).exists())
