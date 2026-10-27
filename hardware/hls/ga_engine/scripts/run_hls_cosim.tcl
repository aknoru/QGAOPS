# ==============================================================================
# Vitis HLS Tcl Script: C/RTL Co-Simulation
# Target Board : PYNQ-Z2
# Target Part  : xc7z020clg400-1
# Target Clock : 100 MHz (10.0 ns)
# ==============================================================================

open_project prj_qgpu_ga_csim
open_solution "solution1"

puts "=================================================================="
puts "  RUNNING VITIS HLS C/RTL CO-SIMULATION"
puts "=================================================================="
cosim_design -trace_level all -argv "hardware/hls/ga_engine/vectors/golden_vectors.csv"

exit
