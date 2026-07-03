# Contributing to Datavion AI

First of all, thank you for contributing to **Datavion AI**.

Our goal is to build an enterprise-grade Healthcare Revenue Cycle Management (RCM) platform using modern software engineering practices, clean architecture, and AI-first development.

This document defines the engineering standards that every contributor must follow.

---

# Table of Contents

- Code of Conduct
- Development Philosophy
- Repository Structure
- Architecture Principles
- Getting Started
- Development Workflow
- Branch Strategy
- Commit Message Convention
- Coding Standards
- API Development Standards
- Database Standards
- Testing Standards
- Code Review Checklist
- Pull Request Process
- Documentation Standards
- Security Guidelines
- Release Process

---

# Code of Conduct

Be respectful.

Be professional.

Be collaborative.

Focus on technical discussions rather than personal opinions.

---

# Development Philosophy

Datavion AI follows these principles:

- Clean Architecture
- SOLID Principles
- DRY
- KISS
- YAGNI
- API First
- Security First
- Test Driven Mindset
- AI Ready
- Enterprise Grade

---

# Repository Structure

```
platform/

apps/
config/
docs/
requirements/
scripts/
templates/

manage.py
pyproject.toml
```

Every business module follows the same structure.

```
module/

api/
tests/
migrations/

models.py
selectors.py
services.py
serializers.py
permissions.py
urls.py
admin.py
apps.py
```

---

# Architecture Principles

## Models

Responsible only for persistence.

Business logic should not live in models.

---

## Selectors

Responsible only for reading data.

Selectors must never modify the database.

---

## Services

Responsible for business logic.

All create, update and delete operations belong here.

---

## Serializers

Responsible for:

- validation
- serialization
- deserialization

Do not place business logic inside serializers.

---

## Views

Views should only orchestrate HTTP requests.

Views must not contain business logic.

---

## Permissions

Authorization must be handled through permission classes.

Never hardcode permissions inside views.

---

# Getting Started

Clone the repository.

```bash
git clone <repository-url>

cd platform
```

Create a virtual environment.

Windows

```powershell
python -m venv venv

venv\Scripts\activate
```

Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements/dev.txt
```

Install pre-commit hooks.

```bash
pre-commit install
```

Run Django checks.

```bash
python manage.py check
```

---

# Development Workflow

```
Issue

↓

Create Feature Branch

↓

Implementation

↓

Unit Tests

↓

Run Pre-Commit

↓

Open Pull Request

↓

Code Review

↓

Merge
```

---

# Branch Strategy

```
main

develop

feature/<feature-name>

bugfix/<issue-name>

hotfix/<issue-name>

release/<version>
```

Examples

```
feature/patient-module

feature/rbac-api

bugfix/login-api

hotfix/jwt-expiry
```

---

# Commit Message Convention

We follow the Conventional Commits specification.

Examples

```
feat(accounts): add user management API

fix(auth): resolve JWT refresh issue

refactor(employees): move validation into service layer

docs(readme): update installation guide

test(teams): add service layer tests

perf(selectors): optimize employee queries

chore(ci): configure GitHub Actions
```

---

# Coding Standards

## Python

- Python 3.12
- PEP 8
- Black formatting
- Ruff linting
- MyPy type checking

---

## Naming

Classes

```
PascalCase
```

Functions

```
snake_case
```

Variables

```
snake_case
```

Constants

```
UPPER_CASE
```

Private methods

```
_method_name()
```

---

## Type Hints

Always use type hints.

Example

```python
def create_user(
    *,
    validated_data: dict,
) -> User:
```

---

## Docstrings

Public functions must contain docstrings.

Example

```python
"""
Create a new employee.
"""
```

---

# API Development Standards

Every endpoint must have:

- Serializer
- Selector
- Service
- Permission
- Tests
- OpenAPI documentation

Views should remain thin.

Business logic belongs in services.

---

# Database Standards

Use PostgreSQL.

Never execute raw SQL unless necessary.

Optimize queries using:

- select_related
- prefetch_related

Keep migrations small and atomic.

Never edit an applied migration.

---

# Testing Standards

Every feature should include tests.

Test types

- Unit Tests
- API Tests
- Permission Tests
- Service Tests
- Selector Tests

Run tests

```bash
pytest
```

Coverage

```bash
coverage run -m pytest

coverage report
```

Minimum coverage target:

```
95%
```

---

# Code Review Checklist

Before requesting a review, ensure:

- Code builds successfully
- Django system check passes
- Ruff passes
- Black passes
- MyPy passes
- Tests pass
- Coverage meets target
- Documentation updated

---

# Pull Request Process

Every Pull Request should include:

## Summary

Describe the purpose of the change.

## Changes

List major implementation details.

## Testing

Describe how the change was tested.

## Checklist

- [ ] Tests added or updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Code reviewed
- [ ] Pre-commit passed

---

# Documentation Standards

Documentation is part of the codebase.

Update documentation whenever you change:

- APIs
- Architecture
- Database
- Configuration
- Environment Variables

---

# Security Guidelines

Never commit:

- API Keys
- JWT Secrets
- Database Passwords
- Cloud Credentials
- `.env` files

Use environment variables for all secrets.

Run Bandit before merging security-sensitive changes.

---

# Release Process

```
Feature Complete

↓

Testing

↓

Code Review

↓

Release Branch

↓

QA

↓

Production Deployment

↓

Tag Release
```

Versioning follows **Semantic Versioning (SemVer)**.

Example

```
v1.0.0

v1.1.0

v1.2.3

v2.0.0
```

---

# Need Help?

If you have questions about:

- Architecture
- Coding Standards
- Development Workflow
- Repository Structure

please open a discussion or contact the project maintainers before implementing major changes.

---

# License

By contributing to this repository, you agree that your contributions become part of the Datavion AI codebase and are governed by the repository's license.

---

**Datavion AI Engineering Team**

Building enterprise healthcare software with modern engineering practices, scalable architecture, and AI-powered automation.
