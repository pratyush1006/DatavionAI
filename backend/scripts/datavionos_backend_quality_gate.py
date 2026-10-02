"""DatavionOS backend release quality gate."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(label: str, command: list[str]) -> dict[str, object]:
    print(f"[RUN] {label}: {' '.join(command)}")
    process = subprocess.run(command, cwd=ROOT, env=os.environ.copy())
    return {"label": label, "command": command, "exit_code": process.returncode}


def main() -> int:
    python = sys.executable
    results = [
        run(
            "COMPILE",
            [python, "-B", "-m", "compileall", "-q", "apps", "config", "manage.py"],
        ),
        run("DJANGO_CHECK", [python, "-B", "manage.py", "check"]),
        run(
            "MIGRATION_DRIFT",
            [
                python,
                "-B",
                "manage.py",
                "makemigrations",
                "--check",
                "--dry-run",
                "--no-input",
            ],
        ),
        run("PIP_CHECK", [python, "-B", "-m", "pip", "check"]),
        run(
            "RUFF_CHECK",
            [python, "-B", "-m", "ruff", "check", "apps", "config", "manage.py"],
        ),
        run(
            "RUFF_FORMAT",
            [python, "-B", "-m", "ruff", "format", "--check", "apps", "config"],
        ),
        run("MYPY", [python, "-B", "-m", "mypy", "apps", "config"]),
        run("PYTEST", [python, "-B", "-m", "pytest", "-q", "--no-cov"]),
        run(
            "BANDIT",
            [python, "-B", "-m", "bandit", "-q", "-r", "apps", "config", "-ll", "-ii"],
        ),
        run(
            "SPECTACULAR",
            [
                python,
                "-B",
                "manage.py",
                "spectacular",
                "--file",
                str(ROOT / "datavionos-openapi-quality.yaml"),
                "--validate",
            ],
        ),
    ]
    passed = all(int(item["exit_code"]) == 0 for item in results)
    stamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    report = ROOT / f"datavionos_backend_quality_{stamp}.json"
    report.write_text(
        json.dumps(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "passed": passed,
                "results": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"REPORT: {report}")
    print(
        "DATAVIONOS BACKEND ENTERPRISE QUALITY GATE: " + ("PASS" if passed else "FAIL")
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
