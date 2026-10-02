"""
Selectors for the Patient Identifiers module.
"""

from .patient_identifier import (
    get_identifier_by_id,
    get_identifier_by_value,
    get_patient_identifiers,
    get_primary_identifier,
)

__all__ = [
    "get_identifier_by_id",
    "get_identifier_by_value",
    "get_patient_identifiers",
    "get_primary_identifier",
]

from .patient_identifier import get_identifier_by_id as _canonical_get_identifier_by_id


def get_identifier_by_id(identifier_id, *args, **kwargs):
    import inspect

    implementation = _canonical_get_identifier_by_id
    parameters = inspect.signature(implementation).parameters
    values = dict(kwargs)
    remaining = list(args)
    identifier_parameter = next(
        (
            name
            for name in parameters
            if name in ("identifier_id", "identifier", "patient_identifier_id", "pk")
        ),
        None,
    )
    if identifier_parameter is None:
        identifier_parameter = next(
            (
                p.name
                for p in parameters.values()
                if "identifier" in p.name.lower()
                and p.name not in {"identifier_type", "identifier_value"}
            ),
            None,
        )
    if identifier_parameter is None:
        raise TypeError(
            "Canonical get_identifier_by_id exposes no identifier parameter"
        )
    identifier_param = parameters[identifier_parameter]
    if identifier_param.kind == inspect.Parameter.POSITIONAL_ONLY:
        positional_values = [identifier_id]
    else:
        values.setdefault(identifier_parameter, identifier_id)
        positional_values = []
    organization_parameter = next(
        (
            name
            for name in parameters
            if name == "organization" or "organization" in name.lower()
        ),
        None,
    )
    if remaining and organization_parameter and organization_parameter not in values:
        values[organization_parameter] = remaining.pop(0)
    if (
        organization_parameter
        and organization_parameter not in values
        and parameters[organization_parameter].default is inspect.Parameter.empty
    ):
        try:
            from apps.patient_management.identifiers.models import PatientIdentifier

            _identifier_object = PatientIdentifier.objects.select_related(
                "organization"
            ).get(pk=identifier_id)
            _organization = getattr(_identifier_object, "organization", None)
            if _organization is not None:
                values[organization_parameter] = _organization
        except Exception:
            pass
    positional_parameters = [
        p for p in parameters.values() if p.kind == inspect.Parameter.POSITIONAL_ONLY
    ]
    if remaining:
        for parameter in parameters.values():
            if not remaining:
                break
            if (
                parameter.kind == inspect.Parameter.KEYWORD_ONLY
                and parameter.name not in values
            ):
                values[parameter.name] = remaining.pop(0)
    if remaining:
        positional_values.extend(remaining)
    return implementation(*positional_values, **values)
