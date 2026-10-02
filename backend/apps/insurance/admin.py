from django.contrib import admin

from apps.insurance.models import *

for model in (
    Payer,
    TPA,
    PayerTPARelationship,
    InsurancePlan,
    PlanProduct,
    Network,
    Subscriber,
    Enrollment,
    Dependent,
    MemberIdentifier,
    Benefit,
    CoordinationOfBenefits,
):
    admin.site.register(model)
