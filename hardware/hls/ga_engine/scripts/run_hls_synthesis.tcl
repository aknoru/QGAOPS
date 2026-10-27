# ==============================================================================
# Vitis HLS Tcl Script: Synthesis for Architecture Variants A & B
# Target Board : PYNQ-Z2
# Target Part  : xc7z020clg400-1
# Target Clock : 100 MHz (10.0 ns)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Synthesize Variant A: Resource-Shared Architecture
# ------------------------------------------------------------------------------
open_project -reset prj_qgpu_shared
set_top qgpu_ga_engine_shared
add_files ../src/qgpu_ga_engine_shared.cpp -cflags "-I../include"
add_files -tb ../tb/tb_qgpu_ga_engine.cpp -cflags "-I../include"
add_files -tb ../vectors/golden_vectors.csv

open_solution -reset "solution_shared" -flow_target vivado
set_part {xc7z020clg400-1}
create_clock -period 10.0 -name default

puts "=================================================================="
puts "  RUNNING VITIS HLS SYNTHESIS: VARIANT A (RESOURCE-SHARED)"
puts "=================================================================="
csynth_design

# ------------------------------------------------------------------------------
# 2. Synthesize Variant B: Parallel Pipelined Architecture
# ------------------------------------------------------------------------------
open_project -reset prj_qgpu_parallel
set_top qgpu_ga_engine_parallel
add_files ../src/qgpu_ga_engine_parallel.cpp -cflags "-I../include"
add_files -tb ../tb/tb_qgpu_ga_engine.cpp -cflags "-I../include"
add_files -tb ../vectors/golden_vectors.csv

open_solution -reset "solution_parallel" -flow_target vivado
set_part {xc7z020clg400-1}
create_clock -period 10.0 -name default

puts "=================================================================="
puts "  RUNNING VITIS HLS SYNTHESIS: VARIANT B (PARALLEL PIPELINED)"
puts "=================================================================="
csynth_design

exit
