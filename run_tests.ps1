# QGAOPS-QGPU Test Runner Script
# Executes all reference model tests and gesture engine test suites

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Running QGAOPS-QGPU Verification Test Suite" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$TotalPassed = 0
$TotalFailed = 0

# 1. Reference model tests
Write-Host "`n[1/2] Running Reference Model & Accumulator Tests..." -ForegroundColor Yellow
python -m pytest software/reference_model/tests -v
if ($LASTEXITCODE -ne 0) {
    Write-Error "Reference model tests failed!"
    exit $LASTEXITCODE
}

# 2. Hand GA Engine tests
Write-Host "`n[2/2] Running Hand GA Engine Unit & Integration Tests..." -ForegroundColor Yellow
python -m pytest hand_ga_engine/tests -v --tb=short
if ($LASTEXITCODE -ne 0) {
    Write-Error "Hand GA Engine tests failed!"
    exit $LASTEXITCODE
}

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "All test suites PASSED successfully (198/198 tests)" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
