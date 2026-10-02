from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.insurance.api.serializers import serializer_for
from apps.insurance.models import *
from apps.insurance.selectors import get, queryset
from apps.insurance.services import resolve_route
from apps.insurance.workflows import (
    InsuranceCreateWorkflow,
    InsuranceDeleteWorkflow,
    InsuranceUpdateWorkflow,
)
from apps.platform.organizations.models import Organization
from apps.platform.rbac.resolvers import resolve_permissions

MODELS = {
    "payers": Payer,
    "tpas": TPA,
    "payer-tpa-relationships": PayerTPARelationship,
    "plans": InsurancePlan,
    "products": PlanProduct,
    "networks": Network,
    "subscribers": Subscriber,
    "enrollments": Enrollment,
    "dependents": Dependent,
    "member-identifiers": MemberIdentifier,
    "benefits": Benefit,
    "cob": CoordinationOfBenefits,
}


def organization(request):
    org = getattr(request, "current_organization", None) or getattr(
        request, "organization", None
    )
    if org is not None:
        return org
    value = request.headers.get("X-Organization-ID")
    if value:
        return Organization.objects.filter(pk=value).first()
    return None


def allowed(request, org, permission):
    if org is None:
        return False
    perms = resolve_permissions(user=request.user, organization=org)
    return permission in perms


def context(request, org, name):
    return WorkflowContext.create(
        tenant_id=getattr(org, "tenant_id", org.id),
        actor_id=request.user.pk,
        workflow_name=name,
        metadata={"organization_id": str(org.id)},
    )


class CollectionAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    model = None

    def get(self, request):
        org = organization(request)
        if not allowed(request, org, "insurance.view") and not allowed(
            request, org, "insurance.manage"
        ):
            return Response({"detail": "Permission denied."}, status=403)
        return Response(
            serializer_for(self.model)(queryset(self.model, org.id), many=True).data
        )

    def post(self, request):
        org = organization(request)
        if not allowed(request, org, "insurance.manage"):
            return Response({"detail": "Permission denied."}, status=403)
        serializer = serializer_for(self.model)(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = InsuranceCreateWorkflow().execute(
            context=context(request, org, "insurance.create"),
            model=self.model,
            organization=org,
            data=serializer.validated_data,
        )
        return Response(serializer_for(self.model)(result.data).data, status=201)


class DetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    model = None

    def get(self, request, object_id):
        org = organization(request)
        if not allowed(request, org, "insurance.view") and not allowed(
            request, org, "insurance.manage"
        ):
            return Response({"detail": "Permission denied."}, status=403)
        return Response(
            serializer_for(self.model)(get(self.model, object_id, org.id)).data
        )

    def patch(self, request, object_id):
        org = organization(request)
        if not allowed(request, org, "insurance.manage"):
            return Response({"detail": "Permission denied."}, status=403)
        serializer = serializer_for(self.model)(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        result = InsuranceUpdateWorkflow().execute(
            context=context(request, org, "insurance.update"),
            model=self.model,
            organization=org,
            object_id=object_id,
            data=serializer.validated_data,
        )
        return Response(serializer_for(self.model)(result.data).data)

    def delete(self, request, object_id):
        org = organization(request)
        if not allowed(request, org, "insurance.delete") and not allowed(
            request, org, "insurance.manage"
        ):
            return Response({"detail": "Permission denied."}, status=403)
        InsuranceDeleteWorkflow().execute(
            context=context(request, org, "insurance.delete"),
            model=self.model,
            organization=org,
            object_id=object_id,
            actor=request.user,
        )
        return Response(status=204)


class RouteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, enrollment_id, service):
        org = organization(request)
        if not allowed(request, org, "insurance.view") and not allowed(
            request, org, "insurance.manage"
        ):
            return Response({"detail": "Permission denied."}, status=403)
        result = resolve_route(
            enrollment=get(Enrollment, enrollment_id, org.id), service=service
        )
        return Response(
            {
                "payer_id": str(result["payer"].id),
                "payer_name": result["payer"].display_name,
                "tpa_id": str(result["tpa"].id) if result["tpa"] else None,
                "tpa_name": result["tpa"].display_name if result["tpa"] else None,
                "service": service,
            }
        )
