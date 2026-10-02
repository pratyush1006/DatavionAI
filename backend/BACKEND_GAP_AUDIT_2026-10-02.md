# DatavionOS backend gap audit — 2026-10-02

## Executive status

The backend is **not release-ready as a whole**. Individual domains have passing focused tests, but the global runtime and release gates are blocked.

Verified baseline:

- 4,737 Python files compile successfully.
- `pip check` reports no broken dependencies.
- Pytest discovers 1,566 tests before stopping with 28 collection errors.
- The focused module suite used during this audit has passing tests, but it cannot substitute for the global suite.
- Bandit reports one medium-severity finding and 555 low-severity findings.

## P0 — release blockers

### 1. Patient Portal package cannot be read

`apps/patient_management/portal` raises Windows `PermissionError: [WinError 5] Access is denied`.

Impact:

- `manage.py check` fails while importing the root URL configuration.
- OpenAPI generation cannot reliably inspect all routes.
- Pytest collection fails.
- The backend master audit crashes while inspecting portal URL files.
- Migration drift and other Django-wide checks cannot be trusted until access is restored.

Repair: restore filesystem ownership/read permissions for the package, then run Django checks, migration drift, OpenAPI generation, and test collection again.

### 2. Global test collection is broken

`pytest --collect-only` discovers 1,566 tests but exits with 28 collection errors.

Major causes:

- Multiple clinical and compliance suites import `BaseTestCase` or `BaseAPITestCase`, while `apps/common/tests/base.py` exports only `AuthenticatedAPITestCase`.
- Patient family-member tests reference missing `FamilyMemberPermission` and selector exports.
- Patient identifier tests reference missing permission exports.
- Organization branding tests reference a missing selector export.
- Several test directories have non-package/import-name collisions such as `test_api`, `test_models`, `test_services`, and `test_workflows`.
- The unreadable Patient Portal directory is also collected and fails.

Repair: restore compatibility aliases or update imports, restore missing public exports, ensure every nested test directory has correct package boundaries, remove stale bytecode, and rerun collection before running the full suite.

### 3. OpenAPI generation crashes

`manage.py spectacular --validate` terminates with:

`ImproperlyConfigured: Field name invoice_number is not valid for model Customer in CustomerListSerializer.`

The customer field constants contain invoice fields (`invoice_number`, `amount`, `due_date`, `status`, and `customer`) while the serializer is based on the Customer model.

Additional schema gaps:

- Revenue Cycle appeal APIViews have no resolvable serializer.
- Accounts Receivable APIViews have no resolvable serializer.
- `TenantJWTAuthentication` has no drf-spectacular authentication extension.

Repair the customer serializer/model mismatch first, then annotate or convert APIViews and register an authentication extension.

## P1 — high operational risk

### 4. Test database teardown is unreliable

Database-backed suites intermittently fail during flush because PostgreSQL refuses to truncate referenced tables. Observed references include:

- `ai_document_chunks` → `organizations`
- `predictions` → `patients`
- `predictions` → `ai_models`

This also leaves records behind, causing duplicate-user failures on later runs.

Repair: ensure all owning apps/models are included in Django's flush graph, remove unmanaged cross-app table ownership, or provide a safe test-database cleanup strategy using the complete dependency graph.

### 5. RBAC enforcement is inconsistent

Some operational APIs authenticate users but do not enforce domain actions:

- Imaging uses an empty subclass of `IsAuthenticated`.
- Laboratory policy helpers check authentication and organization equality but do not enforce the declared laboratory permissions.

Impact: authenticated organization users may reach acquisition, result, verification, or report workflows without the intended role permission checks.

Repair: enforce the central RBAC permission engine per action and add denial/cross-tenant tests for every workflow endpoint.

### 6. Duplicate URL ownership remains

Static audit detects repeated inclusion for Finance, Nursing, DatavionOS, Imaging, and several Patient Management APIs. Runtime auditing found no duplicate Patient Management paths, but multiple ownership points make route precedence and schema generation fragile.

Repair: designate one canonical URL owner per domain and make compatibility routes explicit aliases rather than repeated includes.

### 7. Production integrations remain placeholders

Concrete production code still raises `NotImplementedError`, including:

- OpenAI, Azure, and Hugging Face embedding providers.
- SMS, push, and WhatsApp notification providers.
- Live transcription provider methods.
- Recruitment list creation service.

Several Imaging policy/integration contract classes are empty placeholders.

Repair: either implement each provider or prevent it from being selectable through configuration and readiness checks.

### 8. Outbound payment HTTP validation needs hardening

Bandit flags `urllib.request.urlopen` in the Razorpay gateway because arbitrary URL schemes may be accepted.

Repair: parse and validate the configured gateway URL, allow only HTTPS, and restrict the hostname to the configured Razorpay API host before opening the request.

## P2 — engineering quality gaps

### 9. Quality configuration is split

Both `pyproject.toml` and `pytest.ini` configure pytest with different discovery patterns and options. Results can differ depending on invocation and plugin behavior.

Repair: keep a single authoritative pytest configuration.

### 10. Coverage policy cannot currently be enforced

The configured threshold is 95% branch-aware coverage, but the suite cannot collect. Any current coverage figure is incomplete.

Repair: fix collection and teardown first, then measure by domain and raise enforcement progressively if the full baseline is below policy.

### 11. Backend audit tooling has defects

The master audit:

- Uses an invalid Windows command construction for its installed-app inspection.
- Crashes instead of recording a warning when a path raises `PermissionError`.
- Produces many filename-duplication warnings that are not meaningful domain duplication.

Repair: pass subprocess arguments as a list, handle inaccessible paths, and base duplicate-source checks on import/module ownership rather than filename equality.

## Recommended repair order

1. Restore Patient Portal filesystem access.
2. Fix test collection imports, missing exports, and package collisions.
3. Correct the Customer/Invoice serializer mismatch and regenerate OpenAPI.
4. Repair test-database teardown and prove repeatable full-suite execution.
5. Enforce central RBAC in Imaging and Laboratory workflows.
6. Consolidate duplicated URL ownership.
7. Complete or disable selectable production provider stubs.
8. Harden the Razorpay outbound URL.
9. Consolidate quality configuration and enforce coverage.
10. Repair the audit tool and make it part of CI.

## Commands used

- `python installer_datavionos_backend_master_e2e_gap_audit.py --skip-tests`
- `python -m pytest --collect-only -q --no-cov -p no:cacheprovider`
- `python -m pip check`
- `python -m bandit -q -r apps config -ll -ii`

The machine-readable audit is available in `datavion-backend-master-gap-report.json`.
