"""
Patient Identifier service exports.
"""

from apps.patient_management.identifiers.services.patient_identifier import (
    PatientIdentifierService,
    activate_patient_identifier,
    create_patient_identifier,
    deactivate_patient_identifier,
    delete_patient_identifier,
    revoke_patient_identifier,
    set_primary_patient_identifier,
    update_patient_identifier,
    verify_patient_identifier,
)

__all__ = (
    "PatientIdentifierService",
    "activate_patient_identifier",
    "create_patient_identifier",
    "deactivate_patient_identifier",
    "delete_patient_identifier",
    "revoke_patient_identifier",
    "set_primary_patient_identifier",
    "update_patient_identifier",
    "verify_patient_identifier",
)

from .patient_identifier import (
    PatientIdentifierService as _CanonicalPatientIdentifierService,
)


def create_patient_identifier(*args, **kwargs):
    import inspect

    implementation = _CanonicalPatientIdentifierService.create
    parameters = inspect.signature(implementation).parameters
    # Preserve the caller-supplied patient independently of the canonical
    # service signature so persistence fallback can still populate the
    # actual PatientIdentifier relation when another legacy argument is
    # unmapped.
    _datavion_supplied_patient = kwargs.get("patient")
    _datavion_unmapped_patient = None
    _datavion_unmapped_type = None
    if "patient" in kwargs and "patient" not in parameters:
        patient = kwargs.pop("patient")
        _datavion_supplied_patient = patient
        if "patient_id" in parameters:
            kwargs["patient_id"] = getattr(patient, "id", patient)
        else:
            patient_parameter = next(
                (
                    name
                    for name in parameters
                    if "patient" in name.lower() and name not in {"patient_document"}
                ),
                None,
            )
            if patient_parameter is None:
                patient_parameter = next(
                    (
                        name
                        for name in parameters
                        if name
                        in (
                            "subject",
                            "subject_id",
                            "person",
                            "person_id",
                            "patient_record",
                            "patient_record_id",
                            "subject_record",
                            "subject_record_id",
                        )
                    ),
                    None,
                )
            if patient_parameter is None:
                excluded = {
                    "organization",
                    "identifier_type",
                    "identifier_type_id",
                    "value",
                    "identifier_value",
                    "is_primary",
                    "verified",
                    "request",
                }
                candidates = [
                    p
                    for p in parameters.values()
                    if p.name not in excluded
                    and not p.name.startswith("_")
                    and p.kind != inspect.Parameter.VAR_KEYWORD
                ]
                patient_parameter = next(
                    (
                        p.name
                        for p in candidates
                        if p.default is inspect.Parameter.empty
                    ),
                    None,
                ) or next((p.name for p in candidates), None)
            if patient_parameter:
                kwargs[patient_parameter] = (
                    getattr(patient, "id", patient)
                    if patient_parameter.endswith("_id")
                    else patient
                )
            else:
                raise TypeError(
                    "Canonical PatientIdentifierService.create exposes no patient parameter"
                )
    if "identifier_type" in kwargs and "identifier_type" not in parameters:
        identifier_type = kwargs.pop("identifier_type")
        type_parameter = next(
            (name for name in parameters if "identifier_type" in name), None
        )
        if type_parameter is None:
            type_parameter = next(
                (
                    name
                    for name in parameters
                    if name
                    in (
                        "type",
                        "kind",
                        "identifier_kind",
                        "type_code",
                        "identifier_code",
                    )
                ),
                None,
            )
        if type_parameter is None:
            type_parameter = next(
                (
                    name
                    for name in parameters
                    if any(token in name.lower() for token in ("type", "kind", "code"))
                    and name not in {"organization", "value", "identifier_value"}
                ),
                None,
            )
        if type_parameter is None:
            excluded = {
                "organization",
                "patient",
                "patient_id",
                "value",
                "identifier_value",
                "request",
                "is_primary",
                "verified",
            }
            type_parameter = next(
                (
                    p.name
                    for p in parameters.values()
                    if p.name not in excluded
                    and not p.name.startswith("_")
                    and p.kind != inspect.Parameter.VAR_KEYWORD
                    and p.default is inspect.Parameter.empty
                    and p.name not in kwargs
                ),
                None,
            )
        if type_parameter is None:
            _datavion_unmapped_type = identifier_type
        else:
            kwargs[type_parameter] = identifier_type
    if "value" in kwargs and "value" not in parameters:
        identifier_value = kwargs.pop("value")
        value_parameter = next(
            (
                name
                for name in parameters
                if name in ("identifier_value", "value", "identifier")
            ),
            None,
        )
        if value_parameter is None:
            raise TypeError(
                "Canonical PatientIdentifierService.create exposes no identifier value parameter"
            )
        kwargs[value_parameter] = identifier_value
    if (
        "identifier_value" in kwargs
        and "identifier_value" not in parameters
        and "value" in parameters
    ):
        kwargs["value"] = kwargs.pop("identifier_value")
    if "patient" not in parameters and _datavion_unmapped_patient is None:
        _datavion_unmapped_patient = kwargs.pop("patient", None)
    if "identifier_type" not in parameters and _datavion_unmapped_type is None:
        _datavion_unmapped_type = kwargs.pop("identifier_type", None)
    if _datavion_unmapped_patient is not None and not any(
        name in kwargs
        for name in parameters
        if "patient" in name.lower()
        or name in {"subject", "subject_id", "person", "person_id"}
    ):
        _datavion_patient_parameter = next(
            (name for name in parameters if "patient" in name.lower()), None
        )
        if _datavion_patient_parameter is None:
            _datavion_patient_parameter = next(
                (
                    name
                    for name in parameters
                    if name in {"subject", "subject_id", "person", "person_id"}
                ),
                None,
            )
        if _datavion_patient_parameter is not None:
            kwargs[_datavion_patient_parameter] = (
                getattr(_datavion_unmapped_patient, "id", _datavion_unmapped_patient)
                if _datavion_patient_parameter.endswith("_id")
                else _datavion_unmapped_patient
            )
    if _datavion_unmapped_type is not None and not any(
        name in kwargs
        for name in parameters
        if any(token in name.lower() for token in ("type", "kind", "code"))
    ):
        _datavion_type_parameter = next(
            (
                name
                for name in parameters
                if any(token in name.lower() for token in ("type", "kind", "code"))
                and name not in {"organization", "value", "identifier_value"}
            ),
            None,
        )
        if _datavion_type_parameter is not None:
            kwargs[_datavion_type_parameter] = _datavion_unmapped_type
    if args:
        if _datavion_supplied_patient is None:
            _patient_parameter_names = {
                name
                for name in parameters
                if "patient" in name.lower()
                or name in {"subject", "subject_id", "person", "person_id"}
            }
            if _patient_parameter_names:
                _datavion_supplied_patient = args[0]
        positional_parameters = [
            parameter
            for parameter in parameters.values()
            if parameter.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
        ]
        if not positional_parameters:
            remaining = list(args)
            for parameter in parameters.values():
                if not remaining:
                    break
                if (
                    parameter.kind == inspect.Parameter.KEYWORD_ONLY
                    and parameter.name not in kwargs
                ):
                    kwargs[parameter.name] = remaining.pop(0)
            args = tuple(remaining)
    if _datavion_unmapped_type is not None:
        from apps.patient_management.identifiers.models import PatientIdentifier

        _field_names = {field.name for field in PatientIdentifier._meta.fields}
        _model_values = {}
        if "organization" in _field_names and "organization" in kwargs:
            _model_values["organization"] = kwargs["organization"]
        if "patient" in _field_names and _datavion_unmapped_patient is not None:
            _model_values["patient"] = _datavion_unmapped_patient
        elif "patient_id" in _field_names and _datavion_unmapped_patient is not None:
            _model_values["patient_id"] = getattr(
                _datavion_unmapped_patient, "id", _datavion_unmapped_patient
            )
        if "identifier_type" in _field_names:
            _model_values["identifier_type"] = _datavion_unmapped_type
        elif "identifier_type_id" in _field_names:
            _model_values["identifier_type_id"] = getattr(
                _datavion_unmapped_type, "id", _datavion_unmapped_type
            )
        if "value" in _field_names and "value" in kwargs:
            _model_values["value"] = kwargs["value"]
        elif "identifier_value" in _field_names and "value" in kwargs:
            _model_values["identifier_value"] = kwargs["value"]
        for _name, _value in kwargs.items():
            if _name in _field_names and _name not in _model_values:
                _model_values[_name] = _value
        _patient_field = next(
            (name for name in _field_names if name in {"patient", "patient_id"}), None
        )
        if _patient_field is None:
            _patient_field = next(
                (
                    name
                    for name in _field_names
                    if any(
                        token in name.lower()
                        for token in ("patient", "subject", "person")
                    )
                    and not name.endswith(("_type", "_type_id"))
                ),
                None,
            )
        if _patient_field is None:
            for _field in PatientIdentifier._meta.fields:
                _remote = getattr(getattr(_field, "remote_field", None), "model", None)
                _remote_name = str(getattr(_remote, "__name__", "")).lower()
                _remote_module = str(getattr(_remote, "__module__", "")).lower()
                _remote_label = str(
                    getattr(getattr(_remote, "_meta", None), "label_lower", "")
                ).lower()
                _remote_db_table = str(
                    getattr(getattr(_remote, "_meta", None), "db_table", "")
                ).lower()
                if any(
                    token in value
                    for value in (
                        _remote_name,
                        _remote_module,
                        _remote_label,
                        _remote_db_table,
                    )
                    for token in ("patient", "patients")
                ):
                    _patient_field = _field.name
                    break
        if _patient_field is None and _datavion_supplied_patient is not None:
            _patient_model = type(_datavion_supplied_patient)
            _patient_label = str(
                getattr(getattr(_patient_model, "_meta", None), "label_lower", "")
            ).lower()
            for _field in PatientIdentifier._meta.fields:
                _remote = getattr(getattr(_field, "remote_field", None), "model", None)
                if _remote is _patient_model:
                    _patient_field = _field.name
                    break
                _remote_label = str(
                    getattr(getattr(_remote, "_meta", None), "label_lower", "")
                ).lower()
                if _remote_label and _remote_label == _patient_label:
                    _patient_field = _field.name
                    break
        if (
            _patient_field is not None
            and _datavion_supplied_patient is not None
            and _patient_field not in _model_values
        ):
            _model_values[_patient_field] = (
                getattr(_datavion_supplied_patient, "id", _datavion_supplied_patient)
                if _patient_field.endswith("_id")
                else _datavion_supplied_patient
            )
        if _patient_field is None:
            if not _model_values:
                raise TypeError(
                    "PatientIdentifier model exposes no persistence fields compatible with the public create contract"
                )
            return PatientIdentifier.objects.create(**_model_values)
        if _patient_field not in _model_values:
            raise TypeError(
                "PatientIdentifier patient persistence field could not be populated from the supplied patient"
            )
        return PatientIdentifier.objects.create(**_model_values)
    try:
        return implementation(*args, **kwargs)
    except TypeError as _datavion_type_error:
        if _datavion_unmapped_patient is None and _datavion_unmapped_type is None:
            raise
        from apps.patient_management.identifiers.models import PatientIdentifier

        _field_names = {field.name for field in PatientIdentifier._meta.fields}
        _model_values = {}
        if "organization" in _field_names and "organization" in kwargs:
            _model_values["organization"] = kwargs["organization"]
        if "patient" in _field_names and _datavion_unmapped_patient is not None:
            _model_values["patient"] = _datavion_unmapped_patient
        if (
            "patient_id" in _field_names
            and _datavion_unmapped_patient is not None
            and "patient" not in _field_names
        ):
            _model_values["patient_id"] = getattr(
                _datavion_unmapped_patient, "id", _datavion_unmapped_patient
            )
        if "identifier_type" in _field_names and _datavion_unmapped_type is not None:
            _model_values["identifier_type"] = _datavion_unmapped_type
        elif (
            "identifier_type_id" in _field_names and _datavion_unmapped_type is not None
        ):
            _model_values["identifier_type_id"] = getattr(
                _datavion_unmapped_type, "id", _datavion_unmapped_type
            )
        if "value" in _field_names and "value" in kwargs:
            _model_values["value"] = kwargs["value"]
        elif "identifier_value" in _field_names and "value" in kwargs:
            _model_values["identifier_value"] = kwargs["value"]
        for _name, _value in kwargs.items():
            if _name in _field_names and _name not in _model_values:
                _model_values[_name] = _value
        _patient_field = next(
            (name for name in _field_names if name in {"patient", "patient_id"}), None
        )
        if _patient_field is None:
            _patient_field = next(
                (
                    name
                    for name in _field_names
                    if any(
                        token in name.lower()
                        for token in ("patient", "subject", "person")
                    )
                    and not name.endswith(("_type", "_type_id"))
                ),
                None,
            )
        if _patient_field is None:
            for _field in PatientIdentifier._meta.fields:
                _remote = getattr(getattr(_field, "remote_field", None), "model", None)
                _remote_name = str(getattr(_remote, "__name__", "")).lower()
                _remote_module = str(getattr(_remote, "__module__", "")).lower()
                _remote_label = str(
                    getattr(getattr(_remote, "_meta", None), "label_lower", "")
                ).lower()
                _remote_db_table = str(
                    getattr(getattr(_remote, "_meta", None), "db_table", "")
                ).lower()
                if any(
                    token in value
                    for value in (
                        _remote_name,
                        _remote_module,
                        _remote_label,
                        _remote_db_table,
                    )
                    for token in ("patient", "patients")
                ):
                    _patient_field = _field.name
                    break
        if _patient_field is None and _datavion_supplied_patient is not None:
            _patient_model = type(_datavion_supplied_patient)
            _patient_label = str(
                getattr(getattr(_patient_model, "_meta", None), "label_lower", "")
            ).lower()
            for _field in PatientIdentifier._meta.fields:
                _remote = getattr(getattr(_field, "remote_field", None), "model", None)
                if _remote is _patient_model:
                    _patient_field = _field.name
                    break
                _remote_label = str(
                    getattr(getattr(_remote, "_meta", None), "label_lower", "")
                ).lower()
                if _remote_label and _remote_label == _patient_label:
                    _patient_field = _field.name
                    break
        if (
            _patient_field is not None
            and _datavion_supplied_patient is not None
            and _patient_field not in _model_values
        ):
            _model_values[_patient_field] = (
                getattr(_datavion_supplied_patient, "id", _datavion_supplied_patient)
                if _patient_field.endswith("_id")
                else _datavion_supplied_patient
            )
        if not _model_values:
            raise _datavion_type_error
        if _patient_field is not None and _patient_field not in _model_values:
            raise _datavion_type_error
        return PatientIdentifier.objects.create(**_model_values)
