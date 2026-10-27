@echo off
REM Launcher for Vitis Analyzer on Sequential HLS Accelerator (IP A)
echo Starting Vitis Analyzer for Sequential Accelerator (qgpu_ga_sequential)...
start "" "C:\AMDDesignTools\2025.2\Vitis\bin\vitis_analyzer.bat" "D:\QGPU\hardware\hls\sequential\qgpu_ga_sequential\solution1\solution1_data.json"
