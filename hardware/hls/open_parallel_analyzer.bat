@echo off
REM Launcher for Vitis Analyzer on Parallel HLS Accelerator (IP B)
echo Starting Vitis Analyzer for Parallel Accelerator (qgpu_ga_parallel)...
start "" "C:\AMDDesignTools\2025.2\Vitis\bin\vitis_analyzer.bat" "D:\QGPU\hardware\hls\adaptive_pipeline\qgpu_ga_parallel\solution1\solution1_data.json"
