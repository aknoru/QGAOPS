# ==============================================================================
# Vitis HLS Tcl Script: C Simulation
# Target Board : PYNQ-Z2
# Target Part  : xc7z020clg400-1
# Target Clock : 100 MHz (10.0 ns)
# ==============================================================================

# Open / create HLS project
open_project -reset prj_qgpu_ga_csim

# Set top-level synthesizable function
set_top qgpu_ga_engine

# Add synthesizable source files
add_files ../src/qgpu_ga_top.cpp -cflags "-I../include"
add_files ../src/qgpu_ga_engine_shared.cpp -cflags "-I../include"
add_files ../src/qgpu_ga_engine_parallel.cpp -cflags "-I../include"

# Add testbench and golden vector data
add_files -tb ../tb/tb_qgpu_ga_engine.cpp -cflags "-I../include"
add_files -tb ../vectors/golden_vectors.csv

# Configure solution
open_solution -reset "solution1" -flow_target vivado
set_part {xc7z020clg400-1}
create_clock -period 10.0 -name default

# Run C Simulation
puts "=================================================================="
puts "  RUNNING VITIS HLS C SIMULATION (CSIM)"
puts "=================================================================="
csim_design -argv "hardware/hls/ga_engine/vectors/golden_vectors.csv"

exit
