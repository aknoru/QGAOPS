@echo off
REM =========================================================================
REM  QGAOPS-QGPU: HLS Build Launcher for AMD Vitis 2025.2
REM =========================================================================

setlocal enabledelayedexpansion

echo [QGPU HLS] Initializing AMD Vitis HLS environment...
call C:\AMDDesignTools\2025.2\Vitis\.settings64-Vitis_for_HLS.bat

set SCRIPT_DIR=%~dp0
set TCL_SCRIPT=%SCRIPT_DIR%hand_ga_engine\hardware\hls\scripts\run_hls.tcl

if not exist "%TCL_SCRIPT%" (
    echo [ERROR] Cannot find HLS script at: %TCL_SCRIPT%
    exit /b 1
)

echo [QGPU HLS] Executing HLS script via vitis-run: %TCL_SCRIPT%
cd /d "%SCRIPT_DIR%hand_ga_engine\hardware\hls\scripts"
vitis-run --mode hls --tcl "%TCL_SCRIPT%"

if %ERRORLEVEL% equ 0 (
    echo [QGPU HLS] Build succeeded! IP package ready in hand_ga_engine/hardware/hls/qgpu_core/solution1/impl/ip/
) else (
    echo [QGPU HLS] Build failed with error code %ERRORLEVEL%.
)
endlocal
