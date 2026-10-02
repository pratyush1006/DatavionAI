from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hospital_operations.constants import CAPACITY_SETUP_CATALOG
from apps.hospital_operations.models import (
    Admission,
    Bed,
    BedReservation,
    Facility,
    OPDQueue,
    OperationalUnit,
    Room,
)
from apps.hospital_operations.permissions import HospitalOperationsPermission
from apps.hospital_operations.selectors import available_beds, opd_waiting_queue
from apps.hospital_operations.services import (
    assign_bed,
    complete_room_cleaning,
    discharge_patient,
    register_opd_visit,
    reserve_bed,
    transfer_patient,
)

from .serializers import (
    AdmissionCreateSerializer,
    BedAssignmentCreateSerializer,
    BedReservationCreateSerializer,
    BedSerializer,
    FacilitySerializer,
    OPDRegistrationSerializer,
    OPDVisitSerializer,
    OperationalUnitSerializer,
    RoomSerializer,
    TransferSerializer,
)


class _ScopedView(APIView):
    permission_classes = (IsAuthenticated, HospitalOperationsPermission)

    def scope(self, request):
        tenant = getattr(request, "current_tenant", None)
        organization = getattr(request, "current_organization", None)
        if not tenant or not organization:
            return (
                None,
                None,
                Response(
                    {"detail": "Tenant context required."},
                    status=status.HTTP_400_BAD_REQUEST,
                ),
            )
        return tenant, organization, None

    @staticmethod
    def error(exc):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class _ScopedSetupListCreateView(_ScopedView, ListCreateAPIView):
    """Organization-scoped capacity setup used before operational workflows."""

    rbac_permission = "manage"

    def get_queryset(self):
        tenant, organization, error = self.scope(self.request)
        if error:
            return self.queryset.none()
        return self.queryset.filter(tenant=tenant, organization=organization)

    def perform_create(self, serializer):
        tenant, organization, error = self.scope(self.request)
        if error:
            raise ValidationError("Tenant and organization context are required.")
        self.validate_scope(serializer.validated_data, tenant, organization)
        serializer.save(tenant=tenant, organization=organization)

    def validate_scope(self, data, tenant, organization):
        """Hook for descendants to verify every supplied parent is in scope."""


class CapacitySetupCatalogView(_ScopedView):
    """Governed dropdown values for facility-capacity setup."""

    rbac_permission = "manage"

    def get(self, request):
        _, _, error = self.scope(request)
        if error:
            return error
        return Response(CAPACITY_SETUP_CATALOG)


class FacilityListCreateView(_ScopedSetupListCreateView):
    queryset = Facility.objects.all().order_by("name")
    serializer_class = FacilitySerializer

    def create(self, request, *args, **kwargs):
        """Treat a repeated governed facility selection as an idempotent create.

        The setup UI intentionally offers catalog entries, so a retry must not
        fail merely because the selected facility code was already configured.
        """
        tenant, organization, error = self.scope(request)
        if error:
            return error
        code = str(request.data.get("code", "")).strip()
        if code:
            existing = (
                self.get_queryset()
                .filter(tenant=tenant, organization=organization, code=code)
                .first()
            )
            if existing is not None:
                return Response(
                    self.get_serializer(existing).data, status=status.HTTP_200_OK
                )
        return super().create(request, *args, **kwargs)


class OperationalUnitListCreateView(_ScopedSetupListCreateView):
    queryset = OperationalUnit.objects.select_related("facility").all().order_by("name")
    serializer_class = OperationalUnitSerializer

    def validate_scope(self, data, tenant, organization):
        facility = data["facility"]
        if (
            facility.tenant_id != tenant.id
            or facility.organization_id != organization.id
        ):
            raise ValidationError(
                {"facility": "Facility is outside the active organization."}
            )


class RoomListCreateView(_ScopedSetupListCreateView):
    queryset = Room.objects.select_related("facility", "unit").all().order_by("number")
    serializer_class = RoomSerializer

    def validate_scope(self, data, tenant, organization):
        facility = data["facility"]
        unit = data["unit"]
        if (
            facility.tenant_id != tenant.id
            or facility.organization_id != organization.id
        ):
            raise ValidationError(
                {"facility": "Facility is outside the active organization."}
            )
        if unit.tenant_id != tenant.id or unit.organization_id != organization.id:
            raise ValidationError({"unit": "Unit is outside the active organization."})
        if unit.facility_id != facility.uuid:
            raise ValidationError(
                {"unit": "Unit must belong to the selected facility."}
            )


class BedListCreateView(_ScopedSetupListCreateView):
    queryset = Bed.objects.select_related("room", "room__unit").all().order_by("label")
    serializer_class = BedSerializer

    def validate_scope(self, data, tenant, organization):
        room = data["room"]
        if room.tenant_id != tenant.id or room.organization_id != organization.id:
            raise ValidationError({"room": "Room is outside the active organization."})


class BedListView(ListAPIView):
    permission_classes = (IsAuthenticated, HospitalOperationsPermission)
    rbac_permission = "view"
    serializer_class = BedSerializer

    def get_queryset(self):
        tenant = getattr(self.request, "current_tenant", None)
        organization = getattr(self.request, "current_organization", None)
        if not tenant or not organization:
            return Bed.objects.none()
        return available_beds(tenant=tenant, organization=organization)


class RoomListView(ListAPIView):
    permission_classes = (IsAuthenticated, HospitalOperationsPermission)
    rbac_permission = "view"
    serializer_class = RoomSerializer

    def get_queryset(self):
        tenant = getattr(self.request, "current_tenant", None)
        organization = getattr(self.request, "current_organization", None)
        if not tenant or not organization:
            return Room.objects.none()
        return Room.objects.filter(
            tenant=tenant, organization=organization
        ).select_related("facility", "unit")


class OPDQueueView(APIView):
    permission_classes = (IsAuthenticated, HospitalOperationsPermission)
    rbac_permission = "view"

    def get(self, request, queue_id):
        tenant = getattr(request, "current_tenant", None)
        organization = getattr(request, "current_organization", None)
        if not tenant or not organization:
            return Response({"detail": "Tenant context required."}, status=400)
        visits = opd_waiting_queue(
            tenant=tenant, organization=organization, queue_id=queue_id
        )
        return Response(OPDVisitSerializer(visits, many=True).data)


class OPDRegistrationView(_ScopedView):
    rbac_permission = "manage_opd"

    def post(self, request):
        tenant, organization, error = self.scope(request)
        if error:
            return error
        serializer = OPDRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = get_object_or_404(
            __import__("django.apps", fromlist=["apps"]).apps.get_model(
                "patient_core", "Patient"
            ),
            pk=serializer.validated_data["patient"],
        )
        queue = get_object_or_404(OPDQueue, pk=serializer.validated_data["queue"])
        try:
            visit = register_opd_visit(
                queue=queue,
                patient=patient,
                tenant=tenant,
                organization=organization,
                encounter_reference=serializer.validated_data.get(
                    "encounter_reference", ""
                ),
            )
        except ValidationError as exc:
            return self.error(exc)
        return Response(OPDVisitSerializer(visit).data, status=status.HTTP_201_CREATED)


class BedReservationCreateView(_ScopedView):
    rbac_permission = "manage"

    def post(self, request):
        tenant, organization, error = self.scope(request)
        if error:
            return error
        serializer = BedReservationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bed = get_object_or_404(Bed, pk=serializer.validated_data["bed"])
        patient = get_object_or_404(
            __import__("django.apps", fromlist=["apps"]).apps.get_model(
                "patient_core", "Patient"
            ),
            pk=serializer.validated_data["patient"],
        )
        try:
            reservation = reserve_bed(
                bed=bed,
                patient=patient,
                tenant=tenant,
                organization=organization,
                reserved_from=serializer.validated_data.get("reserved_from"),
                reserved_until=serializer.validated_data.get("reserved_until"),
                reference=serializer.validated_data.get("reference", ""),
                notes=serializer.validated_data.get("notes", ""),
            )
        except ValidationError as exc:
            return self.error(exc)
        return Response(
            {
                "uuid": str(reservation.uuid),
                "bed": str(reservation.bed_id),
                "patient": str(reservation.patient_id),
                "status": reservation.status,
            },
            status=201,
        )


class BedAssignmentCreateView(_ScopedView):
    rbac_permission = "manage"

    def post(self, request):
        tenant, organization, error = self.scope(request)
        if error:
            return error
        serializer = BedAssignmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bed = get_object_or_404(Bed, pk=serializer.validated_data["bed"])
        patient = get_object_or_404(
            __import__("django.apps", fromlist=["apps"]).apps.get_model(
                "patient_core", "Patient"
            ),
            pk=serializer.validated_data["patient"],
        )
        reservation = None
        if serializer.validated_data.get("reservation"):
            reservation = get_object_or_404(
                BedReservation, pk=serializer.validated_data["reservation"]
            )
        try:
            assignment = assign_bed(
                bed=bed,
                patient=patient,
                tenant=tenant,
                organization=organization,
                admission_reference=serializer.validated_data.get(
                    "admission_reference", ""
                ),
                reservation=reservation,
            )
        except ValidationError as exc:
            return self.error(exc)
        return Response(
            {
                "uuid": str(assignment.uuid),
                "bed": str(assignment.bed_id),
                "patient": str(assignment.patient_id),
                "active": assignment.active,
            },
            status=201,
        )


class AdmissionCreateView(_ScopedView):
    rbac_permission = "admit"

    @transaction.atomic
    def post(self, request):
        tenant, organization, error = self.scope(request)
        if error:
            return error
        serializer = AdmissionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = get_object_or_404(
            __import__("django.apps", fromlist=["apps"]).apps.get_model(
                "patient_core", "Patient"
            ),
            pk=serializer.validated_data["patient"],
        )
        unit = get_object_or_404(OperationalUnit, pk=serializer.validated_data["unit"])
        bed = get_object_or_404(Bed, pk=serializer.validated_data["bed"])
        try:
            admission = Admission.objects.create(
                tenant=tenant,
                organization=organization,
                patient=patient,
                unit=unit,
                admission_number=serializer.validated_data["admission_number"],
                admitted_at=timezone.now(),
                reason=serializer.validated_data.get("reason", ""),
            )
            assignment = assign_bed(
                bed=bed,
                patient=patient,
                tenant=tenant,
                organization=organization,
                admission_reference=admission.admission_number,
            )
            admission.bed_assignment = assignment
            admission.save(update_fields=("bed_assignment", "updated_at"))
        except ValidationError as exc:
            return self.error(exc)
        return Response(
            {
                "uuid": str(admission.uuid),
                "admission_number": admission.admission_number,
                "status": admission.status,
                "bed_assignment": str(assignment.uuid),
            },
            status=201,
        )


class AdmissionTransferView(_ScopedView):
    rbac_permission = "transfer"

    def post(self, request, admission_id):
        tenant, organization, error = self.scope(request)
        if error:
            return error
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admission = get_object_or_404(Admission, pk=admission_id)
        unit = get_object_or_404(OperationalUnit, pk=serializer.validated_data["unit"])
        bed = get_object_or_404(Bed, pk=serializer.validated_data["bed"])
        try:
            movement = transfer_patient(
                admission=admission,
                to_unit=unit,
                to_bed=bed,
                tenant=tenant,
                organization=organization,
                reason=serializer.validated_data.get("reason", ""),
                icu=serializer.validated_data.get("icu", False),
            )
        except ValidationError as exc:
            return self.error(exc)
        return Response(
            {
                "uuid": str(movement.uuid),
                "movement_type": movement.movement_type,
                "to_unit": str(movement.to_unit_id),
                "to_bed": str(movement.to_bed_id),
            },
            status=200,
        )


class AdmissionDischargeView(_ScopedView):
    rbac_permission = "discharge"

    def post(self, request, admission_id):
        tenant, organization, error = self.scope(request)
        if error:
            return error
        admission = get_object_or_404(Admission, pk=admission_id)
        try:
            admission = discharge_patient(
                admission=admission, tenant=tenant, organization=organization
            )
        except ValidationError as exc:
            return self.error(exc)
        return Response(
            {
                "uuid": str(admission.uuid),
                "status": admission.status,
                "discharged_at": admission.discharged_at,
            },
            status=200,
        )


class BedCleaningCompleteView(_ScopedView):
    rbac_permission = "manage"

    def post(self, request, bed_id):
        tenant, organization, error = self.scope(request)
        if error:
            return error
        bed = get_object_or_404(Bed, pk=bed_id)
        try:
            bed = complete_room_cleaning(
                bed=bed, tenant=tenant, organization=organization
            )
        except ValidationError as exc:
            return self.error(exc)
        return Response(BedSerializer(bed).data, status=200)
