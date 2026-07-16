###############################################################################
# Datavion AI
# Enterprise Makefile
###############################################################################

.DEFAULT_GOAL := help

PYTHON := python
MANAGE := $(PYTHON) manage.py
PYTEST := pytest

###############################################################################
# Help
###############################################################################

.PHONY: help

help:
	@echo ""
	@echo "Datavion AI Commands"
	@echo "===================="
	@echo ""
	@echo "make install         Install development dependencies"
	@echo "make check           Django system check"
	@echo "make migrate         Apply migrations"
	@echo "make makemigrations  Create migrations"
	@echo "make run             Run development server"
	@echo "make shell           Django shell"
	@echo "make test            Run tests"
	@echo "make lint            Ruff lint"
	@echo "make format          Format code"
	@echo "make typecheck       MyPy"
	@echo "make security        Bandit"
	@echo "make coverage        Coverage report"
	@echo "make clean           Clean caches"
	@echo "make precommit       Run pre-commit"
	@echo ""

###############################################################################
# Dependencies
###############################################################################

.PHONY: install

install:
	pip install -r requirements/dev.txt
	pre-commit install

###############################################################################
# Django
###############################################################################

.PHONY: run

run:
	$(MANAGE) runserver

.PHONY: shell

shell:
	$(MANAGE) shell

.PHONY: check

check:
	$(MANAGE) check

.PHONY: makemigrations

makemigrations:
	$(MANAGE) makemigrations

.PHONY: migrate

migrate:
	$(MANAGE) migrate

.PHONY: createsuperuser

createsuperuser:
	$(MANAGE) createsuperuser

###############################################################################
# Testing
###############################################################################

.PHONY: test

test:
	$(PYTEST)

.PHONY: coverage

coverage:
	coverage run -m pytest
	coverage report
	coverage html

###############################################################################
# Formatting
###############################################################################

.PHONY: format

format:
	black .
	ruff check . --fix

###############################################################################
# Lint
###############################################################################

.PHONY: lint

lint:
	ruff check .

###############################################################################
# Type Checking
###############################################################################

.PHONY: typecheck

typecheck:
	mypy .

###############################################################################
# Security
###############################################################################

.PHONY: security

security:
	bandit -c pyproject.toml -r apps

###############################################################################
# Pre-commit
###############################################################################

.PHONY: precommit

precommit:
	pre-commit run --all-files

###############################################################################
# Clean
###############################################################################

.PHONY: clean

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -f .coverage
