# Changelog

All notable changes to **Datavion AI** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- Ongoing feature development.

### Changed

- Ongoing improvements.

### Deprecated

- None.

### Removed

- None.

### Fixed

- Ongoing bug fixes.

### Security

- Ongoing security improvements.

---

## [1.1.0] - 2026-06-30

### Added

#### Repository Foundation

- Enterprise repository structure.
- `pyproject.toml`
- `.pre-commit-config.yaml`
- `.editorconfig`
- `.gitignore`
- `Makefile`
- Windows PowerShell development scripts.
- Documentation standards.

#### Engineering Standards

- Ruff
- Black
- MyPy
- Pytest
- Coverage
- Bandit
- Pre-Commit

#### Documentation

- README
- CONTRIBUTING
- CHANGELOG

#### Architecture

- Common module architecture.
- Core module architecture.
- Shared module architecture.
- Service Layer pattern.
- Selector pattern.
- API-first architecture.

#### Developer Experience

- Cross-platform development workflow.
- Windows PowerShell scripts.
- Linux/macOS Makefile.
- Enterprise code quality tooling.

### Changed

- Standardized Django project architecture.
- Standardized application folder structure.
- Standardized engineering guidelines.
- Standardized documentation.
- Improved developer workflow.

### Fixed

- Repository inconsistencies.
- Module standardization issues.
- Cross-platform development support.

### Security

- Added secret detection.
- Added Bandit security scanning.
- Added secure environment variable policy.
- Added pre-commit security checks.

---

## [1.0.0] - Initial Release

### Added

#### Core Modules

- Organizations
- Accounts
- RBAC
- Departments
- Teams
- Employees

#### Authentication

- JWT Authentication
- Login API
- Refresh Token API
- Current User API

#### Authorization

- Role-Based Access Control (RBAC)
- Permission framework

#### API

- Django REST Framework
- OpenAPI Schema
- Swagger UI
- ReDoc

---

# Release Policy

Datavion AI follows **Semantic Versioning (SemVer)**.

## MAJOR

Breaking API or architecture changes.

Example:

```
1.0.0 → 2.0.0
```

---

## MINOR

New functionality added without breaking existing APIs.

Example:

```
1.1.0 → 1.2.0
```

---

## PATCH

Bug fixes and security fixes.

Example:

```
1.2.0 → 1.2.1
```

---

# Change Categories

Use these sections for every release:

- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security

---

# Release Checklist

Before creating a release:

- [ ] Update version.
- [ ] Update CHANGELOG.
- [ ] Update documentation.
- [ ] Run pre-commit hooks.
- [ ] Run `python manage.py check`.
- [ ] Run Ruff.
- [ ] Run Black.
- [ ] Run MyPy.
- [ ] Run Bandit.
- [ ] Run Pytest.
- [ ] Verify coverage target.
- [ ] CI pipeline passes.
- [ ] Create Git tag.
- [ ] Publish GitHub Release.

---

# Version Tags

Examples:

```
v1.0.0
v1.1.0
v1.2.0
v1.2.1
v2.0.0
```

---

# Maintainers

Datavion AI Engineering Team

---

For questions about releases or versioning, contact the project maintainers or open a GitHub issue.
