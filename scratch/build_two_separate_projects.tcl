# ==============================================================================
# Script: build_two_separate_projects.tcl
# Creates TWO independent Vivado projects for PYNQ-ZU:
# 1. SEQ_GPU_PYNQZU (Sequential HLS Accelerator)
# 2. PARALLEL_GPU_PYNQZU (Parallel/Pipelined HLS Accelerator)
# Stops after Block Design creation, validation, and HDL wrapper generation.
# No synthesis or implementation is launched.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. BUILD SEQUENTIAL ACCELERATOR PROJECT (SEQ_GPU_PYNQZU)
# ------------------------------------------------------------------------------
puts "\n======================================================================"
puts "  CREATING SEQUENTIAL ACCELERATOR PROJECT (SEQ_GPU_PYNQZU)"
puts "======================================================================\n"

set seq_proj_name "SEQ_GPU_PYNQZU"
set seq_proj_dir  [file normalize "D:/QGPU/HW/vivado/SEQ_GPU_PYNQZU"]
file mkdir $seq_proj_dir
file mkdir "$seq_proj_dir/scripts"
file mkdir "$seq_proj_dir/reports"

create_project -force $seq_proj_name $seq_proj_dir -part xczu5eg-sfvc784-1-e
set_property board_part tul.com.tw:pynqzu:part0:1.1 [current_project]

# Register SEQ_GPU IP repository
set_property ip_repo_paths [list [file normalize "D:/QGPU/HW/vitis/SEQ_GPU/work/hls/impl/ip"]] [current_project]
update_ip_catalog

# Create Block Design
create_bd_design "seq_gpu_bd"

# Instantiate Zynq UltraScale+ MPSoC
set seq_ps [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e zynq_ultra_ps_e_0]
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } $seq_ps
set_property -dict [list CONFIG.PSU__USE__IRQ0 {1} CONFIG.PSU__USE__M_AXI_GP1 {0}] $seq_ps

# Instantiate SEQ_GPU Core
set seq_core [create_bd_cell -type ip -vlnv QGAOPS:hls:seq_gpu:1.0 seq_gpu_0]

# Connect AXI4-Lite control interface via SmartConnect
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { \
    Master "/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD" \
    Clk "Auto" \
} [get_bd_intf_pins seq_gpu_0/s_axi_control]

# Connect Interrupt directly to PS IRQ0
connect_bd_net [get_bd_pins seq_gpu_0/interrupt] [get_bd_pins zynq_ultra_ps_e_0/pl_ps_irq0]

# Address Assignment
assign_bd_address
set_property offset 0xA0000000 [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_seq_gpu_0_Reg}]
set_property range 64K [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_seq_gpu_0_Reg}]

# Validate and Save
validate_bd_design
save_bd_design

# Export standalone BD script
write_bd_tcl -force "$seq_proj_dir/scripts/create_bd.tcl"

# Generate HDL Top Wrapper
set seq_bd_file [get_files seq_gpu_bd.bd]
set seq_wrapper [make_wrapper -files $seq_bd_file -top]
add_files -norecurse $seq_wrapper
set_property top seq_gpu_bd_wrapper [current_fileset]
update_compile_order -fileset sources_1

# Export Address Map
set fp [open "$seq_proj_dir/reports/address_map.txt" w]
puts $fp "SEQ_GPU_PYNQZU Address Map"
puts $fp "=========================="
foreach seg [get_bd_addr_segs -of_objects [get_bd_addr_spaces /zynq_ultra_ps_e_0/Data]] {
    puts $fp "Segment: $seg"
    puts $fp "  Offset: [get_property offset $seg]"
    puts $fp "  Range:  [get_property range $seg]"
    puts $fp "--------------------------"
}
close $fp

puts "\nSUCCESS: SEQ_GPU_PYNQZU project and block design created successfully.\n"
close_project


# ------------------------------------------------------------------------------
# 2. BUILD PARALLEL/PIPELINED ACCELERATOR PROJECT (PARALLEL_GPU_PYNQZU)
# ------------------------------------------------------------------------------
puts "\n======================================================================"
puts "  CREATING PARALLEL/PIPELINED ACCELERATOR PROJECT (PARALLEL_GPU_PYNQZU)"
puts "======================================================================\n"

set par_proj_name "PARALLEL_GPU_PYNQZU"
set par_proj_dir  [file normalize "D:/QGPU/HW/vivado/PARALLEL_GPU_PYNQZU"]
file mkdir $par_proj_dir
file mkdir "$par_proj_dir/scripts"
file mkdir "$par_proj_dir/reports"

create_project -force $par_proj_name $par_proj_dir -part xczu5eg-sfvc784-1-e
set_property board_part tul.com.tw:pynqzu:part0:1.1 [current_project]

# Register PARALLEL_GPU IP repository
set_property ip_repo_paths [list [file normalize "D:/QGPU/HW/vitis/PARALLEL_GPU/work/hls/impl/ip"]] [current_project]
update_ip_catalog

# Create Block Design
create_bd_design "parallel_gpu_bd"

# Instantiate Zynq UltraScale+ MPSoC
set par_ps [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e zynq_ultra_ps_e_0]
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } $par_ps
set_property -dict [list CONFIG.PSU__USE__IRQ0 {1} CONFIG.PSU__USE__M_AXI_GP1 {0}] $par_ps

# Instantiate PARALLEL_GPU Core
set par_core [create_bd_cell -type ip -vlnv QGAOPS:hls:parallel_gpu:1.0 parallel_gpu_0]

# Connect AXI4-Lite control interface via SmartConnect
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { \
    Master "/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD" \
    Clk "Auto" \
} [get_bd_intf_pins parallel_gpu_0/s_axi_control]

# Connect Interrupt directly to PS IRQ0
connect_bd_net [get_bd_pins parallel_gpu_0/interrupt] [get_bd_pins zynq_ultra_ps_e_0/pl_ps_irq0]

# Address Assignment
assign_bd_address
set_property offset 0xA0000000 [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_parallel_gpu_0_Reg}]
set_property range 64K [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_parallel_gpu_0_Reg}]

# Validate and Save
validate_bd_design
save_bd_design

# Export standalone BD script
write_bd_tcl -force "$par_proj_dir/scripts/create_bd.tcl"

# Generate HDL Top Wrapper
set par_bd_file [get_files parallel_gpu_bd.bd]
set par_wrapper [make_wrapper -files $par_bd_file -top]
add_files -norecurse $par_wrapper
set_property top parallel_gpu_bd_wrapper [current_fileset]
update_compile_order -fileset sources_1

# Export Address Map
set fp [open "$par_proj_dir/reports/address_map.txt" w]
puts $fp "PARALLEL_GPU_PYNQZU Address Map"
puts $fp "=============================="
foreach seg [get_bd_addr_segs -of_objects [get_bd_addr_spaces /zynq_ultra_ps_e_0/Data]] {
    puts $fp "Segment: $seg"
    puts $fp "  Offset: [get_property offset $seg]"
    puts $fp "  Range:  [get_property range $seg]"
    puts $fp "--------------------------"
}
close $fp

puts "\nSUCCESS: PARALLEL_GPU_PYNQZU project and block design created successfully.\n"
close_project

puts "=== ALL REQUESTED PROJECTS BUILT AND VALIDATED TO BLOCK DESIGN STAGE ==="
exit 0
