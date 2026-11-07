# 🚀 OMEGA-MCP One-Click PyPI Deployment Script
param (
    [switch]$TestPyPI = $false
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         OMEGA-MCP PyPI PUBLISHING GATEWAY                " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$distPath = "packages/omega-mcp/dist/*"

# 1. Verify Twine
Write-Host "`n[1/3] Running PyPI package verification with Twine..." -ForegroundColor Yellow
python -m twine check $distPath
if ($LASTEXITCODE -ne 0) {
    Write-Host "`u{274c} Twine check failed! Aborting publish." -ForegroundColor Red
    exit 1
}
Write-Host "`u{2705} Packages verified 100% compliant!" -ForegroundColor Green

# 2. Upload
if ($TestPyPI) {
    Write-Host "`n[2/3] Uploading to TestPyPI..." -ForegroundColor Yellow
    python -m twine upload --repository testpypi $distPath
} else {
    Write-Host "`n[2/3] Uploading to Official PyPI Production..." -ForegroundColor Yellow
    Write-Host "Enter your PyPI API token (__token__ / pypi-...) when prompted:" -ForegroundColor Cyan
    python -m twine upload $distPath
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n==========================================================" -ForegroundColor Green
    Write-Host "  `u{2705} SUCCESS: OMEGA-MCP IS NOW LIVE ON PYPI!        " -ForegroundColor Green
    Write-Host "  Install via: pip install omega-mcp                     " -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Green
} else {
    Write-Host "`n`u{274c} Upload interrupted or cancelled." -ForegroundColor Red
}
