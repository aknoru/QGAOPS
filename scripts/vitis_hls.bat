@echo off
REM =========================================================================
REM  vitis_hls compatibility wrapper for AMD Vitis 2025.2
REM =========================================================================

call C:\AMDDesignTools\2025.2\Vitis\.settings64-Vitis_for_HLS.bat

set ARGS=
:loop
if "%~1"=="" goto done
if "%~1"=="-f" (
    shift
    set "TCL_FILE=%~1"
    goto run_tcl
)
set ARGS=%ARGS% %1
shift
goto loop

:run_tcl
REM Fix relative paths if user passed hardware/... instead of hand_ga_engine/hardware/...
if not exist "%TCL_FILE%" (
    if exist "%~dp0hand_ga_engine\%TCL_FILE%" (
        set "TCL_FILE=%~dp0hand_ga_engine\%TCL_FILE%"
    )
)
echo [vitis_hls wrapper] vitis-run --mode hls --tcl "%TCL_FILE%"
vitis-run --mode hls --tcl "%TCL_FILE%"
exit /b %ERRORLEVEL%

:done
vitis-run --mode hls %ARGS%
exit /b %ERRORLEVEL%
