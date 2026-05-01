# Cross Domain Integrator - Easy Manual Trigger (PowerShell)
# This script runs the Cross Domain Integrator from anywhere
# Usage: powershell -ExecutionPolicy Bypass -File run-cross-domain.ps1

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "CROSS DOMAIN INTEGRATOR - Manual Trigger" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Timestamp: $(Get-Date)" -ForegroundColor Gray
Write-Host "Location: $(Get-Location)" -ForegroundColor Gray
Write-Host ""
Write-Host "[RUNNING] Cross Domain Integrator..." -ForegroundColor Yellow
Write-Host ""

# Run the integrator
python skills/cross_domain_integrator.py
$ExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
if ($ExitCode -eq 0) {
    Write-Host "[SUCCESS] Integration completed successfully!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Process exited with code $ExitCode" -ForegroundColor Red
}
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next: Check /Pending_Approval/ and /Approved/ folders" -ForegroundColor Gray
Write-Host "Summary: Logs/cross_domain_*.md" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"
