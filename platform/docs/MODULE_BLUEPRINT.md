# Datavion AI Module Blueprint

Every Django app in Datavion AI must follow this structure.

```
module/
│
├── admin.py
├── apps.py
├── models.py
├── selectors.py
├── serializers.py
├── services.py
├── permissions.py
├── urls.py
├── __init__.py
│
├── api/
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
│
├── migrations/
│   └── __init__.py
│
└── tests/
    ├── test_models.py
    ├── test_services.py
    ├── test_api.py
    └── __init__.py
```

---

## Responsibilities

### models.py

Contains only Django models.

No business logic.

---

### selectors.py

Contains read/query operations.

Examples:

- get_by_id()
- list_all()
- filter_by_status()

---

### services.py

Contains business logic.

Examples:

- create
- update
- delete
- workflows

Never query directly inside views.

---

### serializers.py

Validation

Serialization

Transformation

---

### permissions.py

Module-specific permissions.

---

### api/views.py

Contains only HTTP logic.

No business logic.

Calls Services and Selectors.

---

### urls.py

Module routing only.

---

### tests/

Every module contains:

- API tests
- Model tests
- Service tests

---

## Architecture Rules

Views → Services → Selectors → Models

Views must never contain business logic.

Services must never return HTTP responses.

Selectors must never modify data.

Models should contain only model-related behavior.

---

## API Standards

Every List API must support:

- Pagination
- Search
- Ordering
- Filtering

Every Create API must:

- Validate serializer
- Call service
- Return detail serializer

Every Update API must:

- Validate serializer
- Call service
- Return detail serializer

Every Delete API must:

- Call service
- Return HTTP 204

---

## Coding Standards

- Black formatting
- Ruff linting
- isort imports
- Type hints when appropriate
- Thin views
- Reusable services
