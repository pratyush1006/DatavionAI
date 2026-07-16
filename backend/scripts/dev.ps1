param(
    [string]$Command = "help"
)

$ErrorActionPreference = "Stop"

function Show-Banner {
    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host "        Datavion AI Developer CLI" -ForegroundColor Cyan
    Write-Host "===============================================" -ForegroundColor Cyan
    Write-Host ""
}

switch ($Command) {

    "help" {

        Show-Banner

        Write-Host "Available Commands"
        Write-Host "------------------"
        Write-Host ""

        Write-Host "install           Install development dependencies"
        Write-Host "run               Run Django development server"
        Write-Host "check             Run Django system checks"
        Write-Host "migrate           Apply database migrations"
        Write-Host "makemigrations    Create new migrations"
        Write-Host "shell             Open Django shell"
        Write-Host "test              Run Django test suite"
        Write-Host "lint              Run Ruff lint"
        Write-Host "format            Auto-fix and format code"
        Write-Host "typecheck         Run MyPy"
        Write-Host "security          Run Bandit security scan"
        Write-Host "coverage          Run test coverage"
        Write-Host "quality           Run complete quality pipeline"
        Write-Host "precommit         Run all pre-commit hooks"
        Write-Host "ci                Simulate GitHub Actions checks"
        Write-Host "clean             Remove generated cache files"

        Write-Host ""
    }

    "install" {

        Show-Banner

        Write-Host "Installing Development Dependencies..."
        Write-Host ""

        pip install -r requirements/development.txt
        pip install -r requirements/testing.txt
        pip install -r requirements/production.txt

        pre-commit install

        Write-Host ""
        Write-Host "Installation Complete." -ForegroundColor Green
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

        python manage.py test
    }

    "lint" {

        Write-Host ""
        Write-Host "Running Ruff Lint..."
        Write-Host ""

        ruff check .

        Write-Host ""
        Write-Host "Lint Complete." -ForegroundColor Green
    }

    "format" {

        Write-Host ""
        Write-Host "Running Ruff Auto Fix..."
        Write-Host ""

        ruff check . --fix

        Write-Host ""
        Write-Host "Running Ruff Formatter..."
        Write-Host ""

        ruff format .

        Write-Host ""
        Write-Host "Formatting Complete." -ForegroundColor Green
    }

    "typecheck" {

        Write-Host ""
        Write-Host "Running MyPy..."
        Write-Host ""

        mypy apps/common

        mypy apps/accounts/services
        mypy apps/accounts/selectors

        mypy apps/configuration/services
        mypy apps/configuration/selectors

        Write-Host ""
        Write-Host "MyPy Complete." -ForegroundColor Green
    }

    "security" {

        Write-Host ""
        Write-Host "Running Bandit..."
        Write-Host ""

        bandit -c pyproject.toml -r apps

        Write-Host ""
        Write-Host "Security Scan Complete." -ForegroundColor Green
    }

    "coverage" {

        Write-Host ""
        Write-Host "Running Coverage..."
        Write-Host ""

        coverage erase

        coverage run -m pytest

        coverage report

        coverage html

        coverage xml

        Write-Host ""
        Write-Host "Coverage Complete." -ForegroundColor Green
    }

    "quality" {

        Show-Banner

        Write-Host "1. Ruff Auto Fix"
        ruff check . --fix

        Write-Host ""
        Write-Host "2. Ruff Format"
        ruff format .

        Write-Host ""
        Write-Host "3. MyPy"

        mypy apps/common

        mypy apps/accounts/services
        mypy apps/accounts/selectors

        mypy apps/configuration/services
        mypy apps/configuration/selectors

        Write-Host ""
        Write-Host "4. Bandit"
        bandit -c pyproject.toml -r apps

        Write-Host ""
        Write-Host "5. Django System Check"
        python manage.py check

        Write-Host ""
        Write-Host "6. Migration Check"
        python manage.py makemigrations --check

        Write-Host ""
        Write-Host "7. Test Suite"
        python manage.py test

        Write-Host ""
        Write-Host "===============================================" -ForegroundColor Green
        Write-Host "Quality Pipeline Completed Successfully." -ForegroundColor Green
        Write-Host "===============================================" -ForegroundColor Green
    }

    "precommit" {

        Show-Banner

        Write-Host "Running Ruff Auto Fix..."
        ruff check . --fix

        Write-Host ""
        Write-Host "Running Ruff Formatter..."
        ruff format .

        Write-Host ""
        Write-Host "Running Pre-Commit..."
        pre-commit run --all-files

        Write-Host ""
        Write-Host "Pre-Commit Completed." -ForegroundColor Green
    }

    "ci" {

        Show-Banner

        Write-Host "Running CI Pipeline..."
        Write-Host ""

        pre-commit run --all-files

        python manage.py check

        python manage.py makemigrations --check

        python manage.py test

        Write-Host ""
        Write-Host "CI Simulation Completed." -ForegroundColor Green
    }

    "clean" {

        Write-Host ""
        Write-Host "Cleaning Project..."
        Write-Host ""

        Get-ChildItem -Recurse -Directory "__pycache__" -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force

        Remove-Item .coverage -ErrorAction SilentlyContinue

        Remove-Item -Recurse htmlcov -Force -ErrorAction SilentlyContinue

        Remove-Item coverage.xml -ErrorAction SilentlyContinue

        Remove-Item -Recurse .pytest_cache -Force -ErrorAction SilentlyContinue

        Remove-Item -Recurse .ruff_cache -Force -ErrorAction SilentlyContinue

        Remove-Item -Recurse .mypy_cache -Force -ErrorAction SilentlyContinue

        Write-Host ""
        Write-Host "Cleanup Complete." -ForegroundColor Green
    }

    default {

        Write-Host ""
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "Run:" -NoNewline
        Write-Host " .\scripts\dev.ps1 help" -ForegroundColor Yellow
    }
}
