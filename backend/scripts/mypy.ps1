Write-Host ""
Write-Host "==============================="
Write-Host "Running MyPy..."
Write-Host "==============================="
Write-Host ""

mypy apps/common

mypy apps/accounts/services
mypy apps/accounts/selectors

mypy apps/configuration/services
mypy apps/configuration/selectors

Write-Host ""
Write-Host "MyPy completed."
