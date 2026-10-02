"""Patient Address lifecycle workflows."""

from __future__ import annotations

from apps.patient_management.addresses.services import AddressService


def create_address(**kwargs):
    return AddressService.create(**kwargs)


def update_address(address, **kwargs):
    return AddressService.update(address, **kwargs)


def delete_address(address):
    return AddressService.delete(address)


def verify_address(address, **kwargs):
    return AddressService.verify(address, **kwargs)
