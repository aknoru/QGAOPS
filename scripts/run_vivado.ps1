# =========================================================================
#  QGAOPS-QGPU: Vivado Block Design & Bitstream Launcher (PowerShell)
# =========================================================================

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$bdScript  = Join-Path $scriptDir "hand_ga_engine\hardware\vivado\scripts\create_block_design.tcl"
$bitScript = Join-Path $scriptDir "hand_ga_engine\hardware\vivado\scripts\build_bitstream.tcl"

Write-Host "[QGPU Vivado] Running Vivado Block Design and Bitstream build..." -ForegroundColor Cyan

$cmd = "call C:\AMDDesignTools\2025.2\Vivado\settings64.bat && cd /d `"$scriptDir\hand_ga_engine\hardware\vivado\scripts`" && vivado -mode batch -source `"$bdScript`" && vivado -mode batch -source `"$bitScript`""

cmd.exe /c $cmd
if ($LASTEXITCODE -eq 0) {
    Write-Host "[QGPU Vivado] Complete system bitstream built successfully!" -ForegroundColor Green
} else {
    Write-Host "[QGPU Vivado] Vivado exited with error code $LASTEXITCODE" -ForegroundColor Yellow
}
