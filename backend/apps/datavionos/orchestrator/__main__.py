"""CLI for the DatavionOS central release orchestrator."""

from __future__ import annotations

import argparse
from pathlib import Path

from .runner import run_orchestrator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    report = run_orchestrator(Path.cwd(), report_only=args.report)
    print("=" * 70)
    print("DATAVIONOS CENTRAL RELEASE ORCHESTRATOR")
    print(f"MODE: {report.mode}")
    for result in report.results:
        print(f"[{result.status}] {result.key} | {result.label}")
        if result.detail:
            print(result.detail)
    print(f"STATUS: {report.status}")
    return 0 if report.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
