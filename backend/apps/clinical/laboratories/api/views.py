from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.clinical.permissions import ClinicalAPIPermission

from ..models import (
    Laboratory,
    LaboratoryOrder,
    LaboratoryReport,
    LaboratoryResult,
    LaboratorySlot,
    LaboratorySpecimen,
    LaboratoryTest,
)
from ..policies import require_authenticated, require_organization
from ..services import allocate_slot_for_appointment, release_report, verify_result
from ..services.processing import (
    complete_processing,
    receive_specimen,
    start_processing,
)
from ..services.specimens import collect_specimen
from .serializers import (
    LaboratoryOrderSerializer,
    LaboratoryReportSerializer,
    LaboratoryResultSerializer,
    LaboratorySerializer,
    LaboratorySlotSerializer,
    LaboratorySpecimenSerializer,
    LaboratoryTestSerializer,
)


def organization(request):
    active_organization = getattr(request, "organization", None)
    value = (
        request.query_params.get("organization_id")
        or getattr(active_organization, "id", None)
        or getattr(request.user, "organization_id", None)
    )
    if not value:
        raise ValueError("organization_id is required.")
    require_organization(request, value)
    return value


class Scoped:
    organization_field = "organization_id"
    clinical_permission_domain = "laboratories"
    clinical_action_aliases = {}

    def get_permissions(self):
        action_by_method = {
            "GET": "view",
            "HEAD": "view",
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete",
        }
        action = action_by_method.get(self.request.method)
        if getattr(self, "action", None) not in {
            None,
            "list",
            "retrieve",
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            action = "transition"
        elif getattr(self, "action", None) in {"list", "retrieve"}:
            action = "view"
        elif getattr(self, "action", None) == "create":
            action = "create"
        elif getattr(self, "action", None) in {"update", "partial_update"}:
            action = "update"
        elif getattr(self, "action", None) == "destroy":
            action = "delete"
        return [
            IsAuthenticated(),
            ClinicalAPIPermission(
                action=action,
                domain=self.clinical_permission_domain,
                action_aliases=self.clinical_action_aliases,
            ),
        ]

    def get_queryset(self):
        require_authenticated(self.request)
        org = organization(self.request)
        return (
            super()
            .get_queryset()
            .filter(**{self.organization_field: org, "is_deleted": False})
        )

    def perform_create(self, serializer):
        serializer.save(organization_id=organization(self.request))


class LaboratoryViewSet(Scoped, viewsets.ModelViewSet):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    clinical_permission_domain = "laboratories"


class LaboratoryTestViewSet(Scoped, viewsets.ModelViewSet):
    queryset = LaboratoryTest.objects.all()
    serializer_class = LaboratoryTestSerializer
    clinical_permission_domain = "laboratories"


class LaboratorySlotViewSet(viewsets.ModelViewSet):
    queryset = LaboratorySlot.objects.all()
    serializer_class = LaboratorySlotSerializer
    clinical_permission_domain = "laboratories"
    clinical_action_aliases = {"allocate_appointment": "order"}

    def get_permissions(self):
        action = (
            "view"
            if self.action in {"list", "retrieve"}
            else (
                "create"
                if self.action == "create"
                else (
                    "update"
                    if self.action in {"update", "partial_update"}
                    else ("delete" if self.action == "destroy" else "transition")
                )
            )
        )
        return [
            IsAuthenticated(),
            ClinicalAPIPermission(
                action=action,
                domain=self.clinical_permission_domain,
                action_aliases=self.clinical_action_aliases,
            ),
        ]

    def get_queryset(self):
        require_authenticated(self.request)
        org = organization(self.request)
        lab = self.request.query_params.get("laboratory_id")
        qs = self.queryset.filter(laboratory__organization_id=org, is_deleted=False)
        return qs.filter(laboratory_id=lab) if lab else qs

    @action(detail=True, methods=["post"], url_path="allocate-appointment")
    def allocate_appointment(self, request, pk=None):
        org = organization(request)
        obj = allocate_slot_for_appointment(
            organization_id=org,
            laboratory_id=self.get_object().laboratory_id,
            slot_id=pk,
            appointment_id=request.data.get("appointment_id"),
            actor_id=getattr(request.user, "id", None),
        )
        return Response({"appointment_id": str(obj.id), "status": obj.status})


class LaboratoryOrderViewSet(Scoped, viewsets.ModelViewSet):
    queryset = LaboratoryOrder.objects.all()
    serializer_class = LaboratoryOrderSerializer
    clinical_permission_domain = "laboratories"
    clinical_action_aliases = {"create": "order", "collect": "specimen"}

    @action(detail=True, methods=["post"], url_path="collect-specimen")
    def collect(self, request, pk=None):
        specimen = collect_specimen(
            organization_id=organization(request),
            order_id=pk,
            specimen_type=request.data.get("specimen_type", "blood"),
            collector_user_id=getattr(request.user, "id", None),
            actor_id=getattr(request.user, "id", None),
        )
        return Response(LaboratorySpecimenSerializer(specimen).data, status=201)


class LaboratorySpecimenViewSet(Scoped, viewsets.ModelViewSet):
    queryset = LaboratorySpecimen.objects.all()
    serializer_class = LaboratorySpecimenSerializer
    clinical_permission_domain = "laboratories"
    clinical_action_aliases = {
        "receive": "specimen",
        "start": "specimen",
        "complete": "specimen",
    }

    def _transition(self, request, service):
        specimen = service(
            organization_id=organization(request),
            specimen_id=self.get_object().id,
            actor_id=getattr(request.user, "id", None),
        )
        return Response(self.get_serializer(specimen).data)

    @action(detail=True, methods=["post"])
    def receive(self, request, pk=None):
        return self._transition(request, receive_specimen)

    @action(detail=True, methods=["post"], url_path="start-processing")
    def start(self, request, pk=None):
        return self._transition(request, start_processing)

    @action(detail=True, methods=["post"], url_path="complete-processing")
    def complete(self, request, pk=None):
        return self._transition(request, complete_processing)


class LaboratoryResultViewSet(Scoped, viewsets.ModelViewSet):
    queryset = LaboratoryResult.objects.all()
    serializer_class = LaboratoryResultSerializer
    clinical_permission_domain = "laboratories"
    clinical_action_aliases = {"verify": "verify"}

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        obj = verify_result(
            organization_id=organization(request),
            result_id=pk,
            actor_id=getattr(request.user, "id", None),
        )
        return Response(self.get_serializer(obj).data)


class LaboratoryReportViewSet(Scoped, viewsets.ModelViewSet):
    queryset = LaboratoryReport.objects.all()
    serializer_class = LaboratoryReportSerializer
    clinical_permission_domain = "laboratories"
    clinical_action_aliases = {"release": "report_release"}

    @action(detail=True, methods=["post"])
    def release(self, request, pk=None):
        obj = release_report(
            organization_id=organization(request),
            order_id=self.get_object().order_id,
            actor_id=getattr(request.user, "id", None),
        )
        return Response(self.get_serializer(obj).data)
