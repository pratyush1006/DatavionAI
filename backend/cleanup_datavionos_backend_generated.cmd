@echo off
setlocal EnableExtensions

echo ==============================================================
echo DatavionOS Backend Generated Artifact Cleanup
echo ==============================================================
echo.

cd /d D:\Datavion-Payment\DatavionAI\backend

echo [1/8] Removing Python cache directories...
for /d /r %%D in (__pycache__) do (
    if exist "%%D" rd /s /q "%%D"
)

echo [2/8] Removing Python bytecode...
del /s /q "*.pyc" 2>nul
del /s /q "*.pyo" 2>nul

echo [3/8] Removing pytest caches...
for /d /r %%D in (.pytest_cache) do (
    if exist "%%D" rd /s /q "%%D"
)

echo [4/8] Removing mypy/ruff caches...
for /d /r %%D in (.mypy_cache) do (
    if exist "%%D" rd /s /q "%%D"
)

for /d /r %%D in (.ruff_cache) do (
    if exist "%%D" rd /s /q "%%D"
)

echo [5/8] Removing coverage artifacts...
if exist ".coverage" del /q ".coverage"
if exist "htmlcov" rd /s /q "htmlcov"

echo [6/8] Removing generated test artifacts...
if exist "test-results" rd /s /q "test-results"
if exist "playwright-report" rd /s /q "playwright-report"

echo [7/8] Removing temporary Python build artifacts...
if exist "build" rd /s /q "build"

for /d /r %%D in (*.egg-info) do (
    if exist "%%D" rd /s /q "%%D"
)

echo [8/8] Cleanup complete.
echo.

echo ==============================================================
echo IMPORTANT
echo ==============================================================
echo This cleanup intentionally DOES NOT delete:
echo.
echo   Django apps
echo   models
echo   serializers
echo   services
echo   selectors
echo   API URLs
echo   migrations
echo   settings
echo   requirements
echo   installer Python files
echo   source configuration
echo.
echo ==============================================================
echo DatavionOS backend generated-artifact cleanup completed.
echo ==============================================================
pause
endlocal
