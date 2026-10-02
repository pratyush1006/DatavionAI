"""Compatibility admin for canonical EmergencyContact."""

from __future__ import annotations

from django.contrib import admin

from apps.patient_management.emergency.models import (
    EmergencyContact,
)


def _field_names(model):
    return {
        field.name
        for field in model._meta.get_fields()
        if getattr(field, "concrete", False)
    }


def _relation_names(model):
    return {
        field.name
        for field in model._meta.get_fields()
        if (getattr(field, "concrete", False) and getattr(field, "is_relation", False))
    }


def _select_existing(
    model,
    candidates,
):
    fields = _field_names(model)

    return tuple(value for value in candidates if value in fields)


def _select_search_fields(
    model,
    candidates,
):
    fields = _field_names(model)

    return tuple(value for value in candidates if value.split("__", 1)[0] in fields)


def _select_relations(
    model,
    candidates,
):
    relations = _relation_names(model)

    return tuple(value for value in candidates if value in relations)


class EmergencyContactAdmin(admin.ModelAdmin):
    pass


DISPLAY_CANDIDATES = (
    "id",
    "patient",
    "name",
    "relationship",
    "phone",
    "alternate_phone",
    "email",
    "priority",
    "status",
    "is_deleted",
    "created_at",
    "updated_at",
)


SEARCH_CANDIDATES = (
    "name",
    "phone",
    "alternate_phone",
    "email",
    "patient__id",
)


FILTER_CANDIDATES = (
    "relationship",
    "priority",
    "status",
    "is_deleted",
    "created_at",
    "updated_at",
)


READONLY_CANDIDATES = (
    "id",
    "created_at",
    "updated_at",
    "deleted_at",
)


AUTOCOMPLETE_CANDIDATES = (
    "organization",
    "patient",
)


ORDERING_CANDIDATES = (
    "-priority",
    "name",
)


EmergencyContactAdmin.list_display = _select_existing(
    EmergencyContact, DISPLAY_CANDIDATES
)


EmergencyContactAdmin.search_fields = _select_search_fields(
    EmergencyContact,
    SEARCH_CANDIDATES,
)


EmergencyContactAdmin.list_filter = _select_existing(
    EmergencyContact,
    FILTER_CANDIDATES,
)


EmergencyContactAdmin.readonly_fields = _select_existing(
    EmergencyContact,
    READONLY_CANDIDATES,
)


EmergencyContactAdmin.autocomplete_fields = _select_relations(
    EmergencyContact,
    AUTOCOMPLETE_CANDIDATES,
)


existing_fields = _field_names(EmergencyContact)


EmergencyContactAdmin.ordering = tuple(
    value for value in ORDERING_CANDIDATES if value.lstrip("-") in existing_fields
)


if EmergencyContact not in admin.site._registry:
    admin.site.register(
        EmergencyContact,
        EmergencyContactAdmin,
    )
