"""Tenant-scoped Imaging operational API."""

from uuid import uuid4

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.imaging.models import (
    ImagingModality,
    ImagingOrder,
    ImagingProcedure,
    ImagingStudy,
    RadiologyReport,
)
from apps.imaging.permissions.imaging import ImagingAuthenticatedPermission
from apps.imaging.services.orders import create_imaging_order
from apps.imaging.services.studies import create_study
from apps.imaging.services.workflow import (
    complete_acquisition,
    complete_order,
    finalize_report,
    mark_order_ready,
    mark_study_arrived,
    mark_study_ready,
    move_to_interpretation,
    schedule_order,
    start_order,
    start_study,
)

from .serializers import (
    ImagingModalitySerializer,
    ImagingOrderSerializer,
    ImagingProcedureSerializer,
    ImagingStudySerializer,
    RadiologyReportSerializer,
)


def _scope(request):
    organization = getattr(request, "organization", None) or getattr(
        request.user, "organization", None
    )
    tenant_id = getattr(organization, "tenant_id", None) or getattr(
        request.user, "tenant_id", None
    )
    organization_id = getattr(organization, "id", None) or getattr(
        request.user, "organization_id", None
    )
    if tenant_id is None:
        raise ValueError("An active tenant is required.")
    requested = request.query_params.get("organization_id") or request.data.get(
        "organization_id"
    )
    if requested and organization_id and str(requested) != str(organization_id):
        raise PermissionError("Cross-organization access denied.")
    return tenant_id, organization_id


class TenantScopedViewSet(viewsets.ModelViewSet):
    permission_classes = (ImagingAuthenticatedPermission,)

    def get_queryset(self):
        tenant_id, organization_id = _scope(self.request)
        queryset = super().get_queryset().filter(tenant_id=tenant_id)
        return (
            queryset.filter(organization_id=organization_id)
            if organization_id
            else queryset
        )

    def perform_create(self, serializer):
        tenant_id, organization_id = _scope(self.request)
        serializer.save(tenant_id=tenant_id, organization_id=organization_id)


class ImagingModalityViewSet(TenantScopedViewSet):
    queryset = ImagingModality.objects.all().order_by("name")
    serializer_class = ImagingModalitySerializer


class ImagingProcedureViewSet(TenantScopedViewSet):
    queryset = (
        ImagingProcedure.objects.select_related("modality").all().order_by("name")
    )
    serializer_class = ImagingProcedureSerializer


class ImagingOrderViewSet(TenantScopedViewSet):
    queryset = ImagingOrder.objects.all().order_by("-created_at")
    serializer_class = ImagingOrderSerializer

    def create(self, request, *args, **kwargs):
        tenant_id, organization_id = _scope(request)
        order = create_imaging_order(
            tenant_id=tenant_id,
            patient_id=request.data.get("patient_id"),
            clinical_indication=request.data.get("clinical_indication", ""),
            order_number=request.data.get("order_number")
            or f"IMG-{uuid4().hex[:10].upper()}",
            ordering_provider_id=request.data.get("ordering_provider_id"),
            encounter_id=request.data.get("encounter_id"),
            priority=request.data.get("priority", "routine"),
            actor_id=getattr(request.user, "id", None),
        )
        if organization_id:
            order.organization_id = organization_id
            order.save(update_fields=["organization_id", "updated_at"])
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED)

    def transition(self, service):
        tenant_id, _ = _scope(self.request)
        state = service(
            order_id=self.get_object().id,
            tenant_id=tenant_id,
            actor_id=getattr(self.request.user, "id", None),
        )
        return Response({"status": state.current_state})

    @action(detail=True, methods=["post"])
    def ready(self, request, pk=None):
        return self.transition(mark_order_ready)

    @action(detail=True, methods=["post"])
    def schedule(self, request, pk=None):
        return self.transition(schedule_order)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        return self.transition(start_order)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        return self.transition(complete_order)


class ImagingStudyViewSet(TenantScopedViewSet):
    queryset = (
        ImagingStudy.objects.select_related("order", "procedure", "procedure__modality")
        .all()
        .order_by("-created_at")
    )
    serializer_class = ImagingStudySerializer

    def create(self, request, *args, **kwargs):
        tenant_id, organization_id = _scope(request)
        study = create_study(
            tenant_id=tenant_id,
            order_id=request.data.get("order"),
            procedure_id=request.data.get("procedure"),
            accession_number=request.data.get("accession_number")
            or f"ACC-{uuid4().hex[:10].upper()}",
            actor_id=getattr(request.user, "id", None),
        )
        if organization_id:
            study.organization_id = organization_id
            study.save(update_fields=["organization_id", "updated_at"])
        return Response(self.get_serializer(study).data, status=status.HTTP_201_CREATED)

    def transition(self, service, **extra):
        tenant_id, _ = _scope(self.request)
        state = service(
            study_id=self.get_object().id,
            tenant_id=tenant_id,
            actor_id=getattr(self.request.user, "id", None),
            **extra,
        )
        return Response({"status": state.current_state})

    @action(detail=True, methods=["post"])
    def arrive(self, request, pk=None):
        return self.transition(mark_study_arrived)

    @action(detail=True, methods=["post"])
    def ready(self, request, pk=None):
        return self.transition(mark_study_ready)

    @action(detail=True, methods=["post"])
    def acquire(self, request, pk=None):
        return self.transition(start_study)

    @action(detail=True, methods=["post"], url_path="complete-acquisition")
    def complete(self, request, pk=None):
        return self.transition(
            complete_acquisition, acquired_by_id=getattr(request.user, "id", None)
        )

    @action(detail=True, methods=["post"])
    def interpret(self, request, pk=None):
        return self.transition(move_to_interpretation)


class RadiologyReportViewSet(TenantScopedViewSet):
    queryset = (
        RadiologyReport.objects.select_related("study").all().order_by("-created_at")
    )
    serializer_class = RadiologyReportSerializer

    @action(detail=True, methods=["post"])
    def finalize(self, request, pk=None):
        tenant_id, _ = _scope(request)
        state = finalize_report(
            report_id=self.get_object().id,
            tenant_id=tenant_id,
            radiologist_id=getattr(request.user, "id", None),
        )
        return Response({"status": state.current_state})


class ImagingContractAPIView(APIView):
    permission_classes = (ImagingAuthenticatedPermission,)

    def get(self, request):
        return Response({"module": "imaging", "canonical": True, "resource": "imaging"})
