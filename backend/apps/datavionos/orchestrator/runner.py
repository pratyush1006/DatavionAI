"""DatavionOS release orchestrator execution engine."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .manifest import GateSpec, get_gate_manifest, validate_manifest


@dataclass(frozen=True, slots=True)
class GateResult:
    key: str
    label: str
    status: str
    exit_code: int | None
    duration_seconds: float
    detail: str = ""


@dataclass(frozen=True, slots=True)
class OrchestratorReport:
    mode: str
    started_at: str
    finished_at: str
    results: tuple[GateResult, ...]
    status: str

    def as_dict(self):
        return {
            "mode": self.mode,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "status": self.status,
            "results": [
                (
                    r.__dict__
                    if hasattr(r, "__dict__")
                    else {
                        "key": r.key,
                        "label": r.label,
                        "status": r.status,
                        "exit_code": r.exit_code,
                        "duration_seconds": r.duration_seconds,
                        "detail": r.detail,
                    }
                )
                for r in self.results
            ],
        }


def _digest(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    h = hashlib.sha256()
    paths = [path] if path.is_file() else sorted(path.rglob("*"))
    for item in paths:
        if not item.is_file() or "__pycache__" in item.parts or ".next" in item.parts:
            continue
        h.update(
            item.relative_to(path.parent if path.is_file() else path)
            .as_posix()
            .encode()
        )
        h.update(item.read_bytes())
    return h.hexdigest()


def _snapshot(backend: Path, gates: tuple[GateSpec, ...]):
    paths = sorted({p for g in gates for p in g.protected_paths})
    return {p: _digest(backend / p) for p in paths}


def _command(command):
    return [sys.executable if x == "{PYTHON}" else x for x in command]


def run_orchestrator(backend: Path, *, report_only=False) -> OrchestratorReport:
    validate_manifest(backend)
    gates = get_gate_manifest()
    mode = "REPORT_ONLY" if report_only else "RELEASE"
    started = datetime.now().isoformat(timespec="seconds")
    before = _snapshot(backend, gates)
    results = []

    for gate in gates:
        if report_only:
            results.append(
                GateResult(
                    gate.key,
                    gate.label,
                    "PLAN_ONLY",
                    None,
                    0.0,
                    "Registered explicit gate; not executed in report mode.",
                )
            )
            continue
        t0 = time.perf_counter()
        p = subprocess.run(
            _command(gate.command),
            cwd=backend,
            text=True,
            capture_output=True,
        )
        detail = "\n".join(x.strip() for x in (p.stdout, p.stderr) if x and x.strip())
        results.append(
            GateResult(
                gate.key,
                gate.label,
                "PASS" if p.returncode == 0 else "FAIL",
                p.returncode,
                time.perf_counter() - t0,
                detail[-6000:],
            )
        )
        if p.returncode and gate.required:
            break

    after = _snapshot(backend, gates)
    results.append(
        GateResult(
            "protected_domain_integrity",
            "Protected Domain Integrity",
            "PASS" if before == after else "FAIL",
            0,
            0.0,
            (
                "Protected path snapshots unchanged."
                if before == after
                else "Protected paths changed during orchestration."
            ),
        )
    )
    status = "FAIL" if any(r.status == "FAIL" for r in results) else "PASS"
    return OrchestratorReport(
        mode,
        started,
        datetime.now().isoformat(timespec="seconds"),
        tuple(results),
        status,
    )
