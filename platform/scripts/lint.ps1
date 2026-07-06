Write-Host ""
Write-Host "Running Ruff..."

ruff check .

Write-Host ""
Write-Host "Formatting..."

ruff format .

Write-Host ""
Write-Host "Lint completed."
