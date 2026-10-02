from django.shortcuts import get_object_or_404

from apps.insurance.models import *


def queryset(model, organization_id):
    if (
        model is Payer
        or model is TPA
        or model is Subscriber
        or model is InsurancePlan
        or model is Enrollment
        or model is CoordinationOfBenefits
        or model is PayerTPARelationship
    ):
        return model.objects.filter(organization_id=organization_id)
    if model is PlanProduct:
        return model.objects.filter(plan__organization_id=organization_id)
    if model is Network or model is Benefit:
        return model.objects.filter(product__plan__organization_id=organization_id)
    if model is Dependent:
        return model.objects.filter(subscriber__organization_id=organization_id)
    if model is MemberIdentifier:
        return model.objects.filter(enrollment__organization_id=organization_id)
    return model.objects.none()


def get(model, object_id, organization_id):
    return get_object_or_404(queryset(model, organization_id), pk=object_id)
