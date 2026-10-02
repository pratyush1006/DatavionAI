from __future__ import annotations

from pathlib import Path

from apps.datavionos.orchestrator.manifest import GATE_MANIFEST, validate_manifest
from apps.datavionos.orchestrator.runner import run_orchestrator

BACKEND = Path(__file__).resolve().parents[2]


def test_manifest_is_explicit_and_unique():
    validate_manifest(BACKEND)
    keys = [gate.key for gate in GATE_MANIFEST]
    assert keys
    assert len(keys) == len(set(keys))


def test_manifest_does_not_auto_discover_installers():
    commands = [token for gate in GATE_MANIFEST for token in gate.command]
    assert "installer_*.py" not in commands
    assert "glob" not in commands


def test_report_mode_is_read_only():
    report = run_orchestrator(BACKEND, report_only=True)
    assert report.status == "PASS"
    assert report.mode == "REPORT_ONLY"
    assert all(r.status in {"PLAN_ONLY", "PASS"} for r in report.results)


def test_family_members_is_protected():
    protected = {p for gate in GATE_MANIFEST for p in gate.protected_paths}
    assert "apps/patient_management/family_members" in protected


def test_mutating_gate_does_not_self_trigger_protected_integrity():
    gate = next(g for g in GATE_MANIFEST if g.key == "saas_billing_constants")
    assert gate.mutation is True
    assert "apps/platform/saas_billing" not in gate.protected_paths


def test_frontend_release_gates_are_explicit():
    keys = [gate.key for gate in GATE_MANIFEST]
    assert "frontend_typecheck" in keys
    assert "frontend_production_build" in keys

    frontend_gates = {
        gate.key: gate for gate in GATE_MANIFEST if gate.scope == "frontend"
    }

    assert frontend_gates["frontend_typecheck"].command
    assert frontend_gates["frontend_production_build"].command
    assert "npm.cmd" in " ".join(frontend_gates["frontend_typecheck"].command)
    assert "npm.cmd" in " ".join(frontend_gates["frontend_production_build"].command)
