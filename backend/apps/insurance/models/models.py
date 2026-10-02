from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.insurance.constants import (
    BenefitCategory,
    CoordinationOrder,
    CoverageStatus,
    InsuranceType,
    RelationshipStatus,
    TPAType,
)
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


class Payer(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="insurance_payers"
    )
    legal_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    payer_code = models.CharField(max_length=100)
    electronic_payer_id = models.CharField(max_length=100, blank=True)
    payer_type = models.CharField(max_length=50, default="insurance")
    contact_information = models.JSONField(default=dict, blank=True)
    claims_configuration = models.JSONField(default=dict, blank=True)
    eligibility_configuration = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "insurance_payers"
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "payer_code"),
                name="insurance_payer_org_code_uniq",
            ),
        )

    def __str__(self):
        return self.display_name


class TPA(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="insurance_tpas"
    )
    legal_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    tpa_code = models.CharField(max_length=100)
    electronic_identifier = models.CharField(max_length=100, blank=True)
    tpa_type = models.CharField(
        max_length=40,
        choices=TPAType.choices,
        default=TPAType.THIRD_PARTY_ADMINISTRATOR,
    )
    contact_information = models.JSONField(default=dict, blank=True)
    service_capabilities = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "insurance_tpas"
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "tpa_code"), name="insurance_tpa_org_code_uniq"
            ),
        )

    def __str__(self):
        return self.display_name


class PayerTPARelationship(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="insurance_payer_tpa_relationships",
    )
    payer = models.ForeignKey(
        Payer, on_delete=models.PROTECT, related_name="tpa_relationships"
    )
    tpa = models.ForeignKey(
        TPA, on_delete=models.PROTECT, related_name="payer_relationships"
    )
    relationship_type = models.CharField(max_length=100, default="administration")
    external_identifier = models.CharField(max_length=100, blank=True)
    effective_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    eligibility_enabled = models.BooleanField(default=False)
    verification_enabled = models.BooleanField(default=False)
    authorization_enabled = models.BooleanField(default=False)
    claims_enabled = models.BooleanField(default=False)
    correspondence_enabled = models.BooleanField(default=False)
    routing_configuration = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        max_length=20,
        choices=RelationshipStatus.choices,
        default=RelationshipStatus.PENDING,
    )

    class Meta:
        db_table = "insurance_payer_tpa_relationships"
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "payer", "tpa", "effective_date"),
                name="ins_ptr_rel_uniq",
            ),
        )


class InsurancePlan(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="insurance_plans"
    )
    payer = models.ForeignKey(
        Payer, on_delete=models.PROTECT, related_name="insurance_plans"
    )
    name = models.CharField(max_length=200)
    plan_code = models.CharField(max_length=100)
    insurance_type = models.CharField(
        max_length=30, choices=InsuranceType.choices, default=InsuranceType.PRIVATE
    )
    policy_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "insurance_plans"
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "plan_code"),
                name="insurance_plan_org_code_uniq",
            ),
        )


class PlanProduct(BaseModel):
    objects = BaseManager()
    plan = models.ForeignKey(
        InsurancePlan, on_delete=models.PROTECT, related_name="products"
    )
    product_code = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "insurance_plan_products"
        constraints = (
            models.UniqueConstraint(
                fields=("plan", "product_code"), name="ins_product_plan_code_uniq"
            ),
        )


class Network(BaseModel):
    objects = BaseManager()
    product = models.ForeignKey(
        PlanProduct, on_delete=models.PROTECT, related_name="networks"
    )
    name = models.CharField(max_length=200)
    network_code = models.CharField(max_length=100)
    network_type = models.CharField(max_length=50, default="medical")
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "insurance_networks"
        constraints = (
            models.UniqueConstraint(
                fields=("product", "network_code"), name="ins_network_product_code_uniq"
            ),
        )


class Subscriber(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="insurance_subscribers"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="insurance_subscriber_records"
    )
    subscriber_identifier = models.CharField(max_length=100)
    relationship_to_patient = models.CharField(max_length=50, default="self")
    employer_name = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "insurance_subscribers"
        constraints = (
            models.UniqueConstraint(
                fields=("organization", "subscriber_identifier"),
                name="ins_sub_org_identifier_uniq",
            ),
        )


class Enrollment(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="insurance_enrollments"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="insurance_enrollments"
    )
    plan = models.ForeignKey(
        InsurancePlan, on_delete=models.PROTECT, related_name="enrollments"
    )
    product = models.ForeignKey(
        PlanProduct,
        on_delete=models.PROTECT,
        related_name="enrollments",
        null=True,
        blank=True,
    )
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.PROTECT,
        related_name="enrollments",
        null=True,
        blank=True,
    )
    member_id = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100, blank=True)
    group_number = models.CharField(max_length=100, blank=True)
    relationship_to_subscriber = models.CharField(max_length=50, default="self")
    effective_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    coverage_percentage = models.PositiveSmallIntegerField(default=100)
    status = models.CharField(
        max_length=20, choices=CoverageStatus.choices, default=CoverageStatus.PENDING
    )
    is_primary = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "insurance_enrollments"
        indexes = (
            models.Index(
                fields=("patient", "status"), name="ins_enroll_patient_status_idx"
            ),
        )


class Dependent(BaseModel):
    objects = BaseManager()
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.PROTECT, related_name="dependents"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="insurance_dependents"
    )
    relationship = models.CharField(max_length=50)
    effective_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "insurance_dependents"
        constraints = (
            models.UniqueConstraint(
                fields=("subscriber", "patient", "effective_date"),
                name="ins_dependent_rel_uniq",
            ),
        )


class MemberIdentifier(BaseModel):
    objects = BaseManager()
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.PROTECT, related_name="member_identifiers"
    )
    identifier_type = models.CharField(max_length=50)
    value = models.CharField(max_length=150)
    issuer = models.CharField(max_length=255, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "insurance_member_identifiers"
        constraints = (
            models.UniqueConstraint(
                fields=("enrollment", "identifier_type", "value"),
                name="ins_member_identifier_uniq",
            ),
        )


class Benefit(BaseModel):
    objects = BaseManager()
    product = models.ForeignKey(
        PlanProduct, on_delete=models.PROTECT, related_name="benefits"
    )
    category = models.CharField(
        max_length=40, choices=BenefitCategory.choices, default=BenefitCategory.MEDICAL
    )
    service_type = models.CharField(max_length=100)
    network_type = models.CharField(max_length=50, blank=True)
    coverage_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    copay_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    deductible_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    coinsurance_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    authorization_required = models.BooleanField(default=False)
    visit_limit = models.PositiveIntegerField(null=True, blank=True)
    monetary_limit = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    effective_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    rules = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "insurance_benefits"


class CoordinationOfBenefits(BaseModel):
    objects = BaseManager()
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="insurance_cob_records"
    )
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.PROTECT, related_name="coordination_records"
    )
    coordination_order = models.PositiveSmallIntegerField(
        choices=CoordinationOrder.choices
    )
    responsibility = models.CharField(max_length=100, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    verification_status = models.CharField(max_length=50, default="unknown")
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "insurance_coordination_of_benefits"
        constraints = (
            models.UniqueConstraint(
                fields=("enrollment", "coordination_order"),
                name="ins_cob_enroll_order_uniq",
            ),
        )
