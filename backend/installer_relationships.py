from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = (
    ROOT / ".relationship_completion_backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
)
MANIFEST_SHA256 = "67bca7ec081a71c0b25ba6d30b0a69ea767318b96e6da32f158b36402487791b"
PAYLOAD = "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"


def load_manifest():
    m = json.loads(gzip.decompress(base64.b64decode(PAYLOAD)).decode())
    if (
        hashlib.sha256(json.dumps(m, sort_keys=True).encode()).hexdigest()
        != MANIFEST_SHA256
    ):
        raise RuntimeError("Manifest integrity check failed")
    return m


def backup(p):
    if p.exists():
        q = BACKUP_ROOT / p.relative_to(ROOT)
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)


def write(p, c):
    x = ROOT / p
    x.parent.mkdir(parents=True, exist_ok=True)
    backup(x)
    x.write_text(
        c.replace("\r\n", "\n").replace("\r", "\n"), encoding="utf-8", newline="\n"
    )
    print("WROTE " + str(p))


def verify(manifest):
    ok = True
    for p in manifest:
        x = ROOT / p
        if not x.is_file():
            print("FAIL missing " + p)
            ok = False
    py = [ROOT / p for p in manifest if p.endswith(".py")]
    for x in py:
        r = subprocess.run(
            [sys.executable, "-m", "py_compile", str(x)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if r.returncode:
            print("FAIL py_compile " + str(x))
            print(r.stderr)
            ok = False
        else:
            print("PASS py_compile " + str(x))
    model = (
        ROOT / r"apps\patient_management\relationships\models\relationship.py"
    ).read_text(encoding="utf-8")
    registry = (
        ROOT / r"apps\patient_management\relationships\workflow_registry.py"
    ).read_text(encoding="utf-8")
    urls = (
        ROOT / r"apps\patient_management\relationships\api\urls\relationship.py"
    ).read_text(encoding="utf-8")
    views = (
        ROOT / r"apps\patient_management\relationships\api\views\lifecycle.py"
    ).read_text(encoding="utf-8")
    view_init = (
        ROOT / r"apps\patient_management\relationships\api\views\__init__.py"
    ).read_text(encoding="utf-8")
    checks = [
        (
            "canonical Patient",
            "from apps.patient_management.patients.models import Patient" in model,
        ),
        (
            "self relationship protection",
            (
                "self.related_patient_id" in model
                and "self.patient_id" in model
                and "self.related_patient_id == self.patient_id" in model
                and "ValidationError" in model
            ),
        ),
        (
            "external invariant",
            (
                "Relationship name is required for " in model
                and "an external relationship." in model
            ),
        ),
        ("verify registered", '"relationship.verify"' in registry),
        ("terminate registered", '"relationship.terminate"' in registry),
        ("set primary registered", '"relationship.set_primary"' in registry),
        (
            "verify API view",
            "PatientRelationshipVerifyAPIView" in views
            and "PatientRelationshipVerifyAPIView" in view_init,
        ),
        (
            "terminate API view",
            "PatientRelationshipTerminateAPIView" in views
            and "PatientRelationshipTerminateAPIView" in view_init,
        ),
        (
            "set-primary API view",
            "PatientRelationshipSetPrimaryAPIView" in views
            and "PatientRelationshipSetPrimaryAPIView" in view_init,
        ),
        ("verify URL", 'name="verify"' in urls),
        ("terminate URL", 'name="terminate"' in urls),
        ("set-primary URL", 'name="set-primary"' in urls),
    ]
    for n, v in checks:
        print(("PASS " if v else "FAIL ") + n)
        ok &= v
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-only", action="store_true")
    a = ap.parse_args()
    m = load_manifest()
    print("DatavionOS Relationships Installer")
    if not a.verify_only:
        for p, c in m.items():
            write(p, c)
        print("BACKUP " + str(BACKUP_ROOT))
    return 0 if verify(m) else 1


if __name__ == "__main__":
    raise SystemExit(main())
