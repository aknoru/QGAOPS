# ==============================================================================
# Script: generate_two_proper_bd_projects.tcl
# Generates TWO separate, clean, validated Vivado Block Design projects:
# 1. SEQ_GPU_PYNQZU (Sequential Accelerator)
# 2. PARALLEL_GPU_PYNQZU (Parallel/Pipelined Accelerator)
# Features:
# - Target: PYNQ-ZU (tul.com.tw:pynqzu:part0:1.1, xczu5eg-sfvc784-1-e)
# - Modern AXI SmartConnect (NO discontinued legacy AXI Interconnect)
# - Exact 100 MHz clocking and synchronized reset distribution
# - Level interrupt connectivity to Zynq MPSoC pl_ps_irq0
# - Validated Block Design + Top HDL Wrapper
# - STOPS AT BLOCK DESIGN (NO synthesis, NO implementation)
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. BUILD SEQUENTIAL ACCELERATOR PROJECT (SEQ_GPU_PYNQZU)
# ------------------------------------------------------------------------------
puts "\n======================================================================"
puts "  BUILDING PROJECT 1: SEQ_GPU_PYNQZU"
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

# 1.1 Instantiate Zynq UltraScale+ MPSoC
set ps_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e zynq_ultra_ps_e_0]
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } $ps_cell

# Enable IRQ0 on PS, disable unused second AXI master (HPM1)
set_property -dict [list CONFIG.PSU__USE__IRQ0 {1} CONFIG.PSU__USE__M_AXI_GP1 {0}] $ps_cell

# 1.2 Instantiate Processor System Reset
set rst_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset rst_ps8_0_100M]

# 1.3 Instantiate AXI SmartConnect (1 Slave from PS, 1 Master to SEQ_GPU)
set smc_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:smartconnect:1.0 axi_smc]
set_property -dict [list CONFIG.NUM_SI {1} CONFIG.NUM_MI {1}] $smc_cell

# 1.4 Instantiate SEQ_GPU Accelerator Core
set seq_cell [create_bd_cell -type ip -vlnv QGAOPS:hls:seq_gpu:1.0 seq_gpu_0]

# 1.5 Connect 100 MHz Clocks
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins zynq_ultra_ps_e_0/maxihpm0_fpd_aclk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins rst_ps8_0_100M/slowest_sync_clk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins axi_smc/aclk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins seq_gpu_0/ap_clk]

# 1.6 Connect Synchronous Resets
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_resetn0] [get_bd_pins rst_ps8_0_100M/ext_reset_in]
connect_bd_net [get_bd_pins rst_ps8_0_100M/peripheral_aresetn] [get_bd_pins axi_smc/aresetn]
connect_bd_net [get_bd_pins rst_ps8_0_100M/peripheral_aresetn] [get_bd_pins seq_gpu_0/ap_rst_n]

# 1.7 Connect AXI SmartConnect Interfaces
connect_bd_intf_net [get_bd_intf_pins zynq_ultra_ps_e_0/M_AXI_HPM0_FPD] [get_bd_intf_pins axi_smc/S00_AXI]
connect_bd_intf_net [get_bd_intf_pins axi_smc/M00_AXI] [get_bd_intf_pins seq_gpu_0/s_axi_control]

# 1.8 Connect Interrupt Directly to PS IRQ0
connect_bd_net [get_bd_pins seq_gpu_0/interrupt] [get_bd_pins zynq_ultra_ps_e_0/pl_ps_irq0]

# 1.9 Assign Address Range (0xA000_0000, 64K)
assign_bd_address
set_property offset 0xA0000000 [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_seq_gpu_0_Reg}]
set_property range 64K [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_seq_gpu_0_Reg}]

# 1.10 Validate and Save Block Design
validate_bd_design
save_bd_design

# 1.11 Export Standalone Block Design Script
write_bd_tcl -force "$seq_proj_dir/scripts/create_bd.tcl"

# 1.12 Generate Output Products & Top-Level HDL Wrapper
set seq_bd_file [get_files seq_gpu_bd.bd]
generate_target all $seq_bd_file
set seq_wrapper [make_wrapper -files $seq_bd_file -top]
add_files -norecurse $seq_wrapper
set_property top seq_gpu_bd_wrapper [current_fileset]
update_compile_order -fileset sources_1

# 1.13 Export Address Map Report
set fp [open "$seq_proj_dir/reports/address_map.txt" w]
puts $fp "SEQ_GPU_PYNQZU Block Design Address Map"
puts $fp "========================================"
foreach seg [get_bd_addr_segs -of_objects [get_bd_addr_spaces /zynq_ultra_ps_e_0/Data]] {
    puts $fp "Segment: $seg"
    puts $fp "  Offset: [get_property offset $seg]"
    puts $fp "  Range:  [get_property range $seg]"
    puts $fp "----------------------------------------"
}
close $fp

puts "\nSUCCESS: SEQ_GPU_PYNQZU Block Design validated and wrapper generated.\n"
close_project


# ------------------------------------------------------------------------------
# 2. BUILD PARALLEL/PIPELINED ACCELERATOR PROJECT (PARALLEL_GPU_PYNQZU)
# ------------------------------------------------------------------------------
puts "\n======================================================================"
puts "  BUILDING PROJECT 2: PARALLEL_GPU_PYNQZU"
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

# 2.1 Instantiate Zynq UltraScale+ MPSoC
set ps_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e zynq_ultra_ps_e_0]
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } $ps_cell

# Enable IRQ0 on PS, disable unused second AXI master (HPM1)
set_property -dict [list CONFIG.PSU__USE__IRQ0 {1} CONFIG.PSU__USE__M_AXI_GP1 {0}] $ps_cell

# 2.2 Instantiate Processor System Reset
set rst_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset rst_ps8_0_100M]

# 2.3 Instantiate AXI SmartConnect (1 Slave from PS, 1 Master to PARALLEL_GPU)
set smc_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:smartconnect:1.0 axi_smc]
set_property -dict [list CONFIG.NUM_SI {1} CONFIG.NUM_MI {1}] $smc_cell

# 2.4 Instantiate PARALLEL_GPU Accelerator Core
set par_cell [create_bd_cell -type ip -vlnv QGAOPS:hls:parallel_gpu:1.0 parallel_gpu_0]

# 2.5 Connect 100 MHz Clocks
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins zynq_ultra_ps_e_0/maxihpm0_fpd_aclk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins rst_ps8_0_100M/slowest_sync_clk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins axi_smc/aclk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins parallel_gpu_0/ap_clk]

# 2.6 Connect Synchronous Resets
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_resetn0] [get_bd_pins rst_ps8_0_100M/ext_reset_in]
connect_bd_net [get_bd_pins rst_ps8_0_100M/peripheral_aresetn] [get_bd_pins axi_smc/aresetn]
connect_bd_net [get_bd_pins rst_ps8_0_100M/peripheral_aresetn] [get_bd_pins parallel_gpu_0/ap_rst_n]

# 2.7 Connect AXI SmartConnect Interfaces
connect_bd_intf_net [get_bd_intf_pins zynq_ultra_ps_e_0/M_AXI_HPM0_FPD] [get_bd_intf_pins axi_smc/S00_AXI]
connect_bd_intf_net [get_bd_intf_pins axi_smc/M00_AXI] [get_bd_intf_pins parallel_gpu_0/s_axi_control]

# 2.8 Connect Interrupt Directly to PS IRQ0
connect_bd_net [get_bd_pins parallel_gpu_0/interrupt] [get_bd_pins zynq_ultra_ps_e_0/pl_ps_irq0]

# 2.9 Assign Address Range (0xA000_0000, 64K)
assign_bd_address
set_property offset 0xA0000000 [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_parallel_gpu_0_Reg}]
set_property range 64K [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_parallel_gpu_0_Reg}]

# 2.10 Validate and Save Block Design
validate_bd_design
save_bd_design

# 2.11 Export Standalone Block Design Script
write_bd_tcl -force "$par_proj_dir/scripts/create_bd.tcl"

# 2.12 Generate Output Products & Top-Level HDL Wrapper
set par_bd_file [get_files parallel_gpu_bd.bd]
generate_target all $par_bd_file
set par_wrapper [make_wrapper -files $par_bd_file -top]
add_files -norecurse $par_wrapper
set_property top parallel_gpu_bd_wrapper [current_fileset]
update_compile_order -fileset sources_1

# 2.13 Export Address Map Report
set fp [open "$par_proj_dir/reports/address_map.txt" w]
puts $fp "PARALLEL_GPU_PYNQZU Block Design Address Map"
puts $fp "============================================"
foreach seg [get_bd_addr_segs -of_objects [get_bd_addr_spaces /zynq_ultra_ps_e_0/Data]] {
    puts $fp "Segment: $seg"
    puts $fp "  Offset: [get_property offset $seg]"
    puts $fp "  Range:  [get_property range $seg]"
    puts $fp "--------------------------------------------"
}
close $fp

puts "\nSUCCESS: PARALLEL_GPU_PYNQZU Block Design validated and wrapper generated.\n"
close_project

puts "\n======================================================================"
puts "  ALL TWO SEPARATE BLOCK DESIGN PROJECTS CREATED SUCCESSFULLY"
puts "======================================================================\n"
exit 0
