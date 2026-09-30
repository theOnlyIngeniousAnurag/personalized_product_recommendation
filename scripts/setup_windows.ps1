# Windows PowerShell Automated Setup Script
# Monash FIT5212 Personalized Product Recommendation System

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Personalized Product Recommendation System - Windows Setup" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# 1. Verify Python Installation
Write-Host "`n[1/4] Verifying Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command py -ErrorAction SilentlyContinue
if ($null -eq $pythonCmd) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
}

if ($null -eq $pythonCmd) {
    Write-Host "[ERROR] Python was not found in PATH. Please install Python 3.10+." -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Using Python executable: $($pythonCmd.Source)" -ForegroundColor Green

# 2. Create Virtual Environment
if (-not (Test-Path ".venv")) {
    Write-Host "`n[2/4] Creating virtual environment (.venv)..." -ForegroundColor Yellow
    & $pythonCmd.Source -m venv .venv
    Write-Host "[OK] Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "`n[2/4] Virtual environment (.venv) already exists." -ForegroundColor Green
}

# 3. Install Dependencies
Write-Host "`n[3/4] Installing Python dependencies..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools -q
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt -q
Write-Host "[OK] Dependencies installed." -ForegroundColor Green

# 4. Run Verification Check & Tests
Write-Host "`n[4/4] Executing setup check and automated tests..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe scripts/check_setup.py
& .\.venv\Scripts\python.exe -m pytest -v

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "Setup Complete! To launch the Streamlit application:" -ForegroundColor Green
Write-Host "  .\.venv\Scripts\python.exe -m streamlit run app/streamlit_app.py --server.port 3000" -ForegroundColor White
Write-Host "To launch the FastAPI REST service:" -ForegroundColor Green
Write-Host "  .\.venv\Scripts\python.exe -m uvicorn api.recommendation_api:app --host 127.0.0.1 --port 8000" -ForegroundColor White
Write-Host "================================================================" -ForegroundColor Cyan
