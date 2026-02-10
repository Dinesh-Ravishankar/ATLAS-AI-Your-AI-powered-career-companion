# ============================================================
#  Atlas AI — One-Click Startup Script (PowerShell)
#  Run from project root:  .\start.ps1
# ============================================================

$Host.UI.RawUI.WindowTitle = "Atlas AI Launcher"

Write-Host ""
Write-Host "  ╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║          ATLAS AI — Starting Up           ║" -ForegroundColor Cyan
Write-Host "  ╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$root = $PSScriptRoot
if (-not $root) { $root = Get-Location }

# ---------- 1. Backend (FastAPI on port 8000) ----------
Write-Host "[1/2] Starting Backend (FastAPI)..." -ForegroundColor Yellow

$backendDir = Join-Path $root "backend"
$pythonExe  = "C:\Users\dines\AppData\Roaming\uv\python\cpython-3.11.14-windows-x86_64-none\python.exe"

# Fallback to generic python if uv python not found
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

Start-Process -FilePath $pythonExe `
    -ArgumentList "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" `
    -WorkingDirectory $backendDir `
    -WindowStyle Normal

Write-Host "      Backend  ->  http://localhost:8000" -ForegroundColor Green
Write-Host "      API Docs ->  http://localhost:8000/docs" -ForegroundColor Green

# ---------- 2. Frontend (Next.js on port 3000) ----------
Write-Host "[2/2] Starting Frontend (Next.js)..." -ForegroundColor Yellow

$frontendDir = Join-Path $root "frontend"

Start-Process -FilePath "npm" `
    -ArgumentList "run", "dev" `
    -WorkingDirectory $frontendDir `
    -WindowStyle Normal

Write-Host "      Frontend ->  http://localhost:3000" -ForegroundColor Green

# ---------- Done ----------
Write-Host ""
Write-Host "  ╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║        Both servers are starting!         ║" -ForegroundColor Cyan
Write-Host "  ╠═══════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "  ║  Frontend : http://localhost:3000         ║" -ForegroundColor White
Write-Host "  ║  Backend  : http://localhost:8000         ║" -ForegroundColor White
Write-Host "  ║  API Docs : http://localhost:8000/docs    ║" -ForegroundColor White
Write-Host "  ╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Tip: Close this window to stop both servers." -ForegroundColor DarkGray
Write-Host ""

# Wait a few seconds then open the browser
Start-Sleep -Seconds 4
Start-Process "http://localhost:3000"
