param(
    [string]$Command = "help"
)

switch ($Command) {

    "help" {
        Write-Host ""
        Write-Host "Datavion AI"
        Write-Host "============"
        Write-Host ""
        Write-Host "install"
        Write-Host "run"
        Write-Host "check"
        Write-Host "migrate"
        Write-Host "makemigrations"
        Write-Host "shell"
        Write-Host "test"
        Write-Host "lint"
        Write-Host "format"
        Write-Host "typecheck"
        Write-Host "security"
        Write-Host "coverage"
        Write-Host "precommit"
        Write-Host "clean"
    }

    "install" {
        pip install -r requirements/dev.txt
        pre-commit install
    }

    "run" {
        python manage.py runserver
    }

    "check" {
        python manage.py check
    }

    "migrate" {
        python manage.py migrate
    }

    "makemigrations" {
        python manage.py makemigrations
    }

    "shell" {
        python manage.py shell
    }

    "test" {
        pytest
    }

    "lint" {
        ruff check .
    }

    "format" {
        black .
        ruff check . --fix
    }

    "typecheck" {
        mypy .
    }

    "security" {
        bandit -c pyproject.toml -r apps
    }

    "coverage" {
        coverage run -m pytest
        coverage report
        coverage html
    }

    "precommit" {
        pre-commit run --all-files
    }

    "clean" {

        Get-ChildItem -Recurse -Directory "__pycache__" |
            Remove-Item -Recurse -Force

        Remove-Item .coverage -ErrorAction SilentlyContinue
        Remove-Item -Recurse htmlcov -ErrorAction SilentlyContinue
        Remove-Item -Recurse .pytest_cache -ErrorAction SilentlyContinue
        Remove-Item -Recurse .ruff_cache -ErrorAction SilentlyContinue
        Remove-Item -Recurse .mypy_cache -ErrorAction SilentlyContinue
    }

    default {
        Write-Host "Unknown command."
    }
}
