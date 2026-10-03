"""
DatavionAI Production Credential Rotation Utility

Run from:
    D:\Datavion-Payment\DatavionAI

Command:
    python rotate_production_credentials.py

What it does:
1. Generates a new Django SECRET_KEY.
2. Generates a new PostgreSQL password.
3. Changes the live PostgreSQL role password.
4. Updates .env and .env.docker without printing secrets.
5. Recreates backend and celery.
6. Runs Django deployment checks.
7. Does NOT recreate PostgreSQL, Redis, frontend, nginx, or cloudflared.

IMPORTANT:
- Secrets are never printed.
- PostgreSQL data volume is not deleted or recreated.
- Existing Django authentication state may be invalidated after SECRET_KEY rotation.
"""

from __future__ import annotations

import datetime as dt
import re
import secrets
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path.cwd()
ENV = ROOT / ".env"
ENV_DOCKER = ROOT / ".env.docker"

SECRET_KEY_PATTERN = re.compile(
    r"^(\s*SECRET_KEY\s*=\s*)(.*?)(\r?\n)?$"
)


def fail(message: str) -> "NoReturn":
    print(f"ERROR: {message}")
    raise SystemExit(1)


def run(
    args: list[str],
    *,
    input_text: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    print("> " + " ".join(args))

    result = subprocess.run(
        args,
        input=input_text,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )

    if result.stdout.strip():
        print(result.stdout.rstrip())

    if result.stderr.strip():
        print(result.stderr.rstrip(), file=sys.stderr)

    if check and result.returncode != 0:
        fail(
            f"Command failed with exit code "
            f"{result.returncode}."
        )

    return result


def read_env_file(path: Path) -> list[str]:
    if not path.exists():
        fail(f"Missing required file: {path}")

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as fh:
        return fh.readlines()


def get_env_value(
    lines: list[str],
    key: str,
) -> str | None:
    prefix = key + "="

    for raw in lines:
        stripped = raw.strip()

        if stripped.startswith(prefix):
            return stripped[len(prefix):]

    return None


def replace_env_key(
    lines: list[str],
    key: str,
    value: str,
) -> tuple[list[str], bool]:
    prefix = key + "="
    output: list[str] = []
    replaced = False

    for raw in lines:
        if raw.endswith("\r\n"):
            newline = "\r\n"
            body = raw[:-2]
        elif raw.endswith("\n"):
            newline = "\n"
            body = raw[:-1]
        else:
            newline = ""
            body = raw

        if body.strip().startswith(prefix):
            output.append(
                f"{prefix}{value}{newline}"
            )
            replaced = True
        else:
            output.append(raw)

    return output, replaced


def upsert_env_key(
    lines: list[str],
    key: str,
    value: str,
) -> list[str]:
    updated, replaced = replace_env_key(
        lines,
        key,
        value,
    )

    if replaced:
        return updated

    newline = "\r\n"

    if updated:
        last = updated[-1]

        if last.endswith("\r\n"):
            newline = "\r\n"
        elif last.endswith("\n"):
            newline = "\n"

    if updated and not updated[-1].endswith(
        ("\n", "\r")
    ):
        updated[-1] += newline

    updated.append(
        f"{key}={value}{newline}"
    )

    return updated


def write_env_file(
    path: Path,
    lines: list[str],
) -> None:
    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:
        fh.writelines(lines)


def is_placeholder(
    value: str | None,
) -> bool:
    if value is None:
        return True

    upper = value.strip().upper()

    return (
        not value.strip()
        or "REPLACE_WITH" in upper
        or upper in {
            "CHANGE_ME",
            "CHANGEME",
            "YOUR_PASSWORD",
            "YOUR_SECRET",
        }
    )


def main() -> int:
    print("=" * 78)
    print(
        "DatavionAI Production Credential Rotation"
    )
    print("=" * 78)

    print(f"Working directory: {ROOT}")

    if not ENV.exists():
        fail(
            f"{ENV} was not found. "
            "Run this from the DatavionAI project root."
        )

    if not ENV_DOCKER.exists():
        fail(
            f"{ENV_DOCKER} was not found. "
            "Run this from the DatavionAI project root."
        )

    print("\nChecking Docker...")

    docker_version = run(
        ["docker", "--version"],
        check=False,
    )

    if docker_version.returncode != 0:
        fail(
            "Docker is not available on PATH."
        )

    print("\nChecking Docker Compose...")

    compose_version = run(
        ["docker", "compose", "version"],
        check=False,
    )

    if compose_version.returncode != 0:
        fail(
            "Docker Compose is not available."
        )

    env_lines = read_env_file(ENV)
    env_docker_lines = read_env_file(
        ENV_DOCKER
    )

    postgres_db = (
        get_env_value(
            env_lines,
            "POSTGRES_DB",
        )
        or get_env_value(
            env_docker_lines,
            "POSTGRES_DB",
        )
    )

    postgres_user = (
        get_env_value(
            env_lines,
            "POSTGRES_USER",
        )
        or get_env_value(
            env_docker_lines,
            "POSTGRES_USER",
        )
    )

    if not postgres_db:
        fail(
            "POSTGRES_DB is missing from .env/.env.docker."
        )

    if not postgres_user:
        fail(
            "POSTGRES_USER is missing from .env/.env.docker."
        )

    current_db_password = get_env_value(
        env_lines,
        "POSTGRES_PASSWORD",
    )

    current_docker_db_password = get_env_value(
        env_docker_lines,
        "POSTGRES_PASSWORD",
    )

    if is_placeholder(
        current_db_password
    ) or is_placeholder(
        current_docker_db_password
    ):
        fail(
            "POSTGRES_PASSWORD still contains "
            "a placeholder. Set the current live "
            "password first."
        )

    print(f"\nDatabase: {postgres_db}")
    print(f"Database role: {postgres_user}")
    print(
        "Secrets: generated locally "
        "and never displayed."
    )

    print(
        "\nChecking Docker Compose service state..."
    )

    ps = run(
        [
            "docker",
            "compose",
            "ps",
            "--format",
            "table",
        ],
        check=False,
    )

    if ps.returncode != 0:
        fail(
            "Unable to inspect Docker Compose services."
        )

    if (
        "datavion_postgres" not in ps.stdout
        or "Up" not in ps.stdout
    ):
        fail(
            "datavion_postgres does not appear "
            "to be running."
        )

    # ---------------------------------------------------------
    # Generate credentials
    # ---------------------------------------------------------

    new_secret_key = secrets.token_urlsafe(64)

    new_db_password = secrets.token_urlsafe(36)

    # ---------------------------------------------------------
    # Backup environment files before modification
    # ---------------------------------------------------------

    timestamp = dt.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    env_backup = ROOT / (
        f".env.backup_{timestamp}"
    )

    env_docker_backup = ROOT / (
        f".env.docker.backup_{timestamp}"
    )

    env_backup.write_bytes(
        ENV.read_bytes()
    )

    env_docker_backup.write_bytes(
        ENV_DOCKER.read_bytes()
    )

    print(
        "\nEnvironment backups created:"
    )
    print(f"  {env_backup.name}")
    print(f"  {env_docker_backup.name}")

    # ---------------------------------------------------------
    # Change PostgreSQL live role password
    # ---------------------------------------------------------

    print(
        "\nChanging the live PostgreSQL "
        "role password..."
    )

    escaped_user = postgres_user.replace(
        '"',
        '""',
    )

    escaped_password = new_db_password.replace(
        "'",
        "''",
    )

    sql = (
        f'ALTER ROLE "{escaped_user}" '
        f"PASSWORD '{escaped_password}';\n"
    )

    psql = run(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "postgres",
            "psql",
            "-U",
            postgres_user,
            "-d",
            postgres_db,
            "-v",
            "ON_ERROR_STOP=1",
        ],
        input_text=sql,
        check=False,
    )

    if psql.returncode != 0:
        fail(
            "PostgreSQL password rotation failed. "
            "Environment files were NOT changed."
        )

    print(
        "PostgreSQL password changed successfully."
    )

    # ---------------------------------------------------------
    # Update environment configuration
    # ---------------------------------------------------------

    print(
        "\nUpdating .env..."
    )

    new_env = env_lines

    new_env = upsert_env_key(
        new_env,
        "POSTGRES_PASSWORD",
        new_db_password,
    )

    existing_secret_key = get_env_value(
        env_lines,
        "SECRET_KEY",
    )

    if existing_secret_key is not None:
        new_env = upsert_env_key(
            new_env,
            "SECRET_KEY",
            new_secret_key,
        )

    print(
        "Updating .env.docker..."
    )

    new_env_docker = env_docker_lines

    new_env_docker = upsert_env_key(
        new_env_docker,
        "POSTGRES_PASSWORD",
        new_db_password,
    )

    new_env_docker = upsert_env_key(
        new_env_docker,
        "DATABASE_PASSWORD",
        new_db_password,
    )

    new_env_docker = upsert_env_key(
        new_env_docker,
        "SECRET_KEY",
        new_secret_key,
    )

    write_env_file(
        ENV,
        new_env,
    )

    write_env_file(
        ENV_DOCKER,
        new_env_docker,
    )

    print(
        "Environment files updated."
    )

    # ---------------------------------------------------------
    # Recreate backend and celery only
    # ---------------------------------------------------------

    print(
        "\nRecreating backend and celery..."
    )

    run(
        [
            "docker",
            "compose",
            "up",
            "-d",
            "--no-deps",
            "--force-recreate",
            "backend",
            "celery",
        ]
    )

    print(
        "\nWaiting for backend startup..."
    )

    time.sleep(8)

    # ---------------------------------------------------------
    # Django system check
    # ---------------------------------------------------------

    print(
        "\nRunning Django deployment checks..."
    )

    check = run(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "backend",
            "python",
            "manage.py",
            "check",
            "--deploy",
        ],
        check=False,
    )

    if check.returncode != 0:
        print(
            "\nWARNING:"
        )
        print(
            "Django deployment check returned "
            f"exit code {check.returncode}."
        )
        print(
            "Review the output above before "
            "considering rotation complete."
        )
        return check.returncode

    # ---------------------------------------------------------
    # Service status
    # ---------------------------------------------------------

    print(
        "\nChecking final Docker Compose state..."
    )

    run(
        [
            "docker",
            "compose",
            "ps",
            "--format",
            "table",
        ]
    )

    completed_at = (
        dt.datetime.now()
        .astimezone()
        .isoformat(
            timespec="seconds"
        )
    )

    print("\n" + "=" * 78)
    print(
        "CREDENTIAL ROTATION COMPLETED"
    )
    print("=" * 78)

    print(
        f"Completed at: {completed_at}"
    )

    print(
        "Django SECRET_KEY: rotated"
    )

    print(
        "PostgreSQL password: rotated"
    )

    print(
        "backend: recreated"
    )

    print(
        "celery: recreated"
    )

    print(
        "postgres: NOT recreated"
    )

    print(
        "redis: NOT recreated"
    )

    print(
        "frontend: NOT recreated"
    )

    print(
        "nginx: NOT recreated"
    )

    print(
        "cloudflared: NOT recreated"
    )

    print("\nNext steps:")
    print(
        "1. Test production login."
    )
    print(
        "2. Complete OTP verification."
    )
    print(
        "3. Open the dashboard."
    )
    print(
        "4. Test logout."
    )
    print(
        "5. Login again."
    )
    print(
        "6. Run the public HTTPS curl checks."
    )

    print(
        "\nIMPORTANT:"
    )
    print(
        "Existing authentication sessions/tokens "
        "may have been invalidated by SECRET_KEY rotation."
    )

    print(
        "\nCredential values were intentionally "
        "not printed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
