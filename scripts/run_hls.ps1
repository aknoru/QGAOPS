# =========================================================================
#  QGAOPS-QGPU: HLS Build Launcher for PowerShell (AMD Vitis 2025.2)
# =========================================================================

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$tclScript = Join-Path $scriptDir "hand_ga_engine\hardware\hls\scripts\run_hls.tcl"

if (-not (Test-Path $tclScript)) {
    Write-Error "[ERROR] Cannot find HLS script at: $tclScript"
    exit 1
}

Write-Host "[QGPU HLS] Running HLS flow via AMD Vitis 2025.2 environment..." -ForegroundColor Cyan

$cmd = "call C:\AMDDesignTools\2025.2\Vitis\.settings64-Vitis_for_HLS.bat && cd /d `"$scriptDir\hand_ga_engine\hardware\hls\scripts`" && vitis-run --mode hls --tcl `"$tclScript`""

cmd.exe /c $cmd
if ($LASTEXITCODE -eq 0) {
    Write-Host "[QGPU HLS] Build succeeded! IP package ready in hand_ga_engine/hardware/hls/qgpu_core/solution1/impl/ip/" -ForegroundColor Green
} else {
    Write-Host "[QGPU HLS] Build finished with exit code $LASTEXITCODE" -ForegroundColor Yellow
}
