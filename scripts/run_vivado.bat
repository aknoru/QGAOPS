@echo off
REM =========================================================================
REM  QGAOPS-QGPU: Vivado Block Design & Bitstream Launcher (AMD Vivado 2025.2)
REM =========================================================================

setlocal enabledelayedexpansion

echo [QGPU Vivado] Initializing AMD Vivado environment...
call C:\AMDDesignTools\2025.2\Vivado\settings64.bat

set SCRIPT_DIR=%~dp0
set BD_SCRIPT=%SCRIPT_DIR%hand_ga_engine\hardware\vivado\scripts\create_block_design.tcl
set BIT_SCRIPT=%SCRIPT_DIR%hand_ga_engine\hardware\vivado\scripts\build_bitstream.tcl

echo [QGPU Vivado] 1. Creating Vivado Block Design for ZedBoard...
cd /d "%SCRIPT_DIR%hand_ga_engine\hardware\vivado\scripts"
vivado -mode batch -source "%BD_SCRIPT%"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Block design generation failed.
    exit /b %ERRORLEVEL%
)

echo [QGPU Vivado] 2. Running Synthesis, Implementation, and Bitstream Generation...
vivado -mode batch -source "%BIT_SCRIPT%"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Bitstream build failed.
    exit /b %ERRORLEVEL%
)

echo [QGPU Vivado] Bitstream generation COMPLETE!
endlocal
