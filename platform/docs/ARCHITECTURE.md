# Datavion AI Architecture

## Overview

Datavion AI follows a layered architecture to separate concerns and improve maintainability.

```
HTTP Request
      │
      ▼
API View
      │
      ▼
Service Layer
      │
      ▼
Selector Layer
      │
      ▼
Database Models
      │
      ▼
PostgreSQL
```

---

# Folder Structure

```
platform/
│
├── apps/
│   ├── accounts/
│   ├── organizations/
│   ├── departments/
│   ├── rbac/
│   ├── common/
│   └── core/
│
├── config/
├── docs/
├── requirements/
├── static/
├── templates/
└── tests/
```

---

# Layer Responsibilities

## Models

Responsible for:

- Database schema
- Relationships
- Model methods

Should NOT contain business workflows.

---

## Selectors

Responsible for reading data.

Examples:

- get_by_id()
- list_all()
- search()
- filtering()

Selectors never modify data.

---

## Services

Responsible for business logic.

Examples:

- create
- update
- delete
- workflows
- validation beyond serializers

Services never return HTTP responses.

---

## Serializers

Responsible for:

- Validation
- Serialization
- Deserialization

---

## API Views

Responsible only for:

- Receiving requests
- Calling services
- Returning responses

Views should never contain business logic.

---

## Permissions

Each module defines its own permission classes.

Authentication is handled using JWT.

Authorization is handled using RBAC.

---

# Shared Framework

Common reusable components live in:

```
apps/common/
```

Current shared modules:

- constants.py
- validators.py
- utils.py
- pagination.py
- exceptions.py

API framework:

```
apps/common/api/
```

Contains:

- base_generics.py
- base_permissions.py
- base_views.py
- mixins.py

---

# API Standards

Every List endpoint supports:

- Pagination
- Search
- Ordering
- Filtering

Every Create endpoint:

- Validates serializer
- Calls service
- Returns detail serializer

Every Update endpoint:

- Validates serializer
- Calls service

Every Delete endpoint:

- Calls service
- Returns HTTP 204

---

# Coding Standards

- Black
- Ruff
- isort
- Thin Views
- Service Layer
- Selector Layer

---

# Future Roadmap

Core Modules:

- Teams
- Employees
- Patients
- Providers
- Claims
- Appointments
- Billing
- Insurance

Infrastructure:

- Docker
- Celery
- Redis
- CI/CD
- Monitoring
- Audit Logs
- Multi-tenancy
