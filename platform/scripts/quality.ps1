Write-Host ""
Write-Host "========================================"
Write-Host "DatavionAI Quality Pipeline"
Write-Host "========================================"
Write-Host ""

& "$PSScriptRoot\lint.ps1"

& "$PSScriptRoot\mypy.ps1"

python manage.py check

python manage.py makemigrations --check

python manage.py test

Write-Host ""
Write-Host "========================================"
Write-Host "Quality checks completed successfully."
Write-Host "========================================"
