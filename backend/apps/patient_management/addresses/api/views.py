"""Patient Address REST endpoints."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.addresses.api.serializers import AddressSerializer
from apps.patient_management.addresses.models import Address
from apps.patient_management.addresses.policies import AddressPolicy
from apps.patient_management.addresses.services import AddressService


def organization_for(request):
    organization = getattr(request.user, "organization", None)
    if organization is None and getattr(request.user, "organization_id", None):
        from apps.platform.organizations.models import Organization

        organization = get_object_or_404(Organization, pk=request.user.organization_id)
    if organization is None:
        raise ValidationError(
            "Authenticated user is not associated with an organization."
        )
    return organization


class AddressListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        organization = organization_for(request)
        qs = (
            Address.objects.with_relations()
            .filter(organization=organization)
            .exclude(status="inactive")
        )
        if request.query_params.get("patient"):
            qs = qs.filter(patient_id=request.query_params["patient"])
        return Response(AddressSerializer(qs, many=True).data)

    def post(self, request):
        organization = organization_for(request)
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        data.pop("tenant", None)
        data.pop("organization", None)
        patient = data.pop("patient", None)
        address = AddressService.create(
            tenant=organization.tenant,
            organization=organization,
            patient=patient,
            **data,
        )
        return Response(AddressSerializer(address).data, status=status.HTTP_201_CREATED)


class AddressDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def obj(self, request, address_id):
        address = get_object_or_404(Address.objects.with_relations(), pk=address_id)
        if not AddressPolicy.can_access(user=request.user, address=address):
            raise PermissionDenied
        return address

    def get(self, request, address_id):
        return Response(AddressSerializer(self.obj(request, address_id)).data)

    def patch(self, request, address_id):
        address = self.obj(request, address_id)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        data.pop("tenant", None)
        data.pop("organization", None)
        AddressService.update(
            address, tenant=address.tenant, organization=address.organization, **data
        )
        return Response(AddressSerializer(address).data)

    def delete(self, request, address_id):
        AddressService.delete(self.obj(request, address_id))
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressVerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, address_id):
        address = get_object_or_404(Address, pk=address_id)
        if not AddressPolicy.can_access(user=request.user, address=address):
            raise PermissionDenied
        return Response(
            AddressSerializer(
                AddressService.verify(
                    address, actor=request.user, notes=request.data.get("notes", "")
                )
            ).data
        )


class AddressReverseGeocodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, address_id):
        address = get_object_or_404(Address, pk=address_id)
        if not AddressPolicy.can_access(user=request.user, address=address):
            raise PermissionDenied
        return Response(AddressSerializer(AddressService.reverse_geocode(address)).data)
