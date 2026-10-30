# Phase D/E Test: Create Block Design with AXI SmartConnect
set proj_dir "D:/QGPU/HW/vivado"
set proj_name "QGAOPS_QGPU_PYNQZU"

create_project -force $proj_name $proj_dir -part xczu5eg-sfvc784-1-e
set_property board_part tul.com.tw:pynqzu:part0:1.1 [current_project]

set_property ip_repo_paths [list \
    [file normalize "D:/QGPU/HW/vitis/SEQ_GPU/work/hls/impl/ip"] \
    [file normalize "D:/QGPU/HW/vitis/PARALLEL_GPU/work/hls/impl/ip"] \
] [current_project]
update_ip_catalog

# Create Block Design
create_bd_design "qgpu_bd"

# 1. Instantiate Zynq UltraScale+ MPSoC
set ps_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e zynq_ultra_ps_e_0]
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } $ps_cell

# Enable IRQ0, disable unused second AXI master (HPM1)
set_property -dict [list CONFIG.PSU__USE__IRQ0 {1} CONFIG.PSU__USE__M_AXI_GP1 {0}] $ps_cell

# 2. Instantiate Processor System Reset
set rst_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset rst_ps8_0_100M]

# 3. Instantiate AXI SmartConnect (1 Slave, 2 Masters)
set smc_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:smartconnect:1.0 axi_smc]
set_property -dict [list CONFIG.NUM_SI {1} CONFIG.NUM_MI {2}] $smc_cell

# 4. Instantiate Accelerators
set seq_cell [create_bd_cell -type ip -vlnv QGAOPS:hls:seq_gpu:1.0 seq_gpu_0]
set par_cell [create_bd_cell -type ip -vlnv QGAOPS:hls:parallel_gpu:1.0 parallel_gpu_0]

# 5. Connect Clocks
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins zynq_ultra_ps_e_0/maxihpm0_fpd_aclk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins rst_ps8_0_100M/slowest_sync_clk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins axi_smc/aclk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins seq_gpu_0/ap_clk]
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_clk0] [get_bd_pins parallel_gpu_0/ap_clk]

# 6. Connect Resets
connect_bd_net [get_bd_pins zynq_ultra_ps_e_0/pl_resetn0] [get_bd_pins rst_ps8_0_100M/ext_reset_in]
connect_bd_net [get_bd_pins rst_ps8_0_100M/peripheral_aresetn] [get_bd_pins axi_smc/aresetn]
connect_bd_net [get_bd_pins rst_ps8_0_100M/peripheral_aresetn] [get_bd_pins seq_gpu_0/ap_rst_n]
connect_bd_net [get_bd_pins rst_ps8_0_100M/peripheral_aresetn] [get_bd_pins parallel_gpu_0/ap_rst_n]

# 7. Connect AXI Interfaces
connect_bd_intf_net [get_bd_intf_pins zynq_ultra_ps_e_0/M_AXI_HPM0_FPD] [get_bd_intf_pins axi_smc/S00_AXI]
connect_bd_intf_net [get_bd_intf_pins axi_smc/M00_AXI] [get_bd_intf_pins seq_gpu_0/s_axi_control]
connect_bd_intf_net [get_bd_intf_pins axi_smc/M01_AXI] [get_bd_intf_pins parallel_gpu_0/s_axi_control]

# 8. Connect Interrupts
set concat_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat xlconcat_0]
set_property -dict [list CONFIG.NUM_PORTS {2}] $concat_cell
connect_bd_net [get_bd_pins seq_gpu_0/interrupt] [get_bd_pins xlconcat_0/In0]
connect_bd_net [get_bd_pins parallel_gpu_0/interrupt] [get_bd_pins xlconcat_0/In1]
connect_bd_net [get_bd_pins xlconcat_0/dout] [get_bd_pins zynq_ultra_ps_e_0/pl_ps_irq0]

# 9. Assign Address Ranges
assign_bd_address
set_property offset 0xA0000000 [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_seq_gpu_0_Reg}]
set_property range 64K [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_seq_gpu_0_Reg}]

set_property offset 0xA0010000 [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_parallel_gpu_0_Reg}]
set_property range 64K [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_parallel_gpu_0_Reg}]

# 10. Validate BD
validate_bd_design
save_bd_design

puts "=== BD VALIDATION WITH SMARTCONNECT SUCCESSFUL ==="

# 11. Create Top HDL Wrapper
set bd_file [get_files qgpu_bd.bd]
set wrapper_file [make_wrapper -files $bd_file -top]
add_files -norecurse $wrapper_file
set_property top qgpu_bd_wrapper [current_fileset]
update_compile_order -fileset sources_1
puts "Wrapper created: $wrapper_file"

# 12. Export Address Map
file mkdir "$proj_dir/reports"
set fp [open "$proj_dir/reports/qgpu_bd_address_map.txt" w]
puts $fp "QGAOPS-QGPU PYNQ-ZU Address Map (SmartConnect Architecture)"
puts $fp "==========================================================="
foreach seg [get_bd_addr_segs -of_objects [get_bd_addr_spaces /zynq_ultra_ps_e_0/Data]] {
    puts $fp "Segment: $seg"
    puts $fp "  Offset: [get_property offset $seg]"
    puts $fp "  Range:  [get_property range $seg]"
    puts $fp "-----------------------------------------------------------"
}
close $fp

# 13. Export Standalone BD Tcl
file mkdir "$proj_dir/scripts"
write_bd_tcl -force "$proj_dir/scripts/create_bd.tcl"
puts "Exported create_bd.tcl"

exit 0
