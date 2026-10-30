# =========================================================================
#  QGAOPS-QGPU: HLS Build Launcher for PowerShell (AMD Vitis 2025.2)
# =========================================================================

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot  = Split-Path -Parent $scriptDir
$tclScript = Join-Path $repoRoot "hardware\hls\scripts\run_hls.tcl"
$workDir   = Join-Path $repoRoot "hardware\hls\scripts"

if (-not (Test-Path $tclScript)) {
    Write-Error "[ERROR] Cannot find HLS script at: $tclScript"
    exit 1
}

Write-Host "[QGPU HLS] Running HLS flow via AMD Vitis 2025.2 environment..." -ForegroundColor Cyan

$cmd = "call C:\AMDDesignTools\2025.2\Vitis\.settings64-Vitis_for_HLS.bat && cd /d `"$workDir`" && vitis-run --mode hls --tcl `"$tclScript`""

cmd.exe /c $cmd
if ($LASTEXITCODE -eq 0) {
    Write-Host "[QGPU HLS] Build succeeded! IP package ready in hardware/hls/qgpu_accel_proj/solution1/impl/ip/" -ForegroundColor Green
} else {
    Write-Host "[QGPU HLS] Build finished with exit code $LASTEXITCODE" -ForegroundColor Yellow
}
