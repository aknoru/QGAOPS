# Stage 11: Vivado Project & Block Design Builder Test
set proj_name "QGAOPS_QGPU_PYNQZU"
set proj_dir "D:/QGPU/HW/vivado"

file mkdir "$proj_dir"
file mkdir "$proj_dir/scripts"
file mkdir "$proj_dir/reports"
file mkdir "$proj_dir/bd"

create_project -force $proj_name $proj_dir -part xczu5eg-sfvc784-1-e
set_property board_part tul.com.tw:pynqzu:part0:1.1 [current_project]

set_property ip_repo_paths [list D:/QGPU/HW/vitis/SEQ_GPU/work/hls/impl/ip D:/QGPU/HW/vitis/PARALLEL_GPU/work/hls/impl/ip] [current_project]
update_ip_catalog

# Create block design
create_bd_design "qgpu_bd"

# 1. Instantiate Zynq UltraScale+ MPSoC
set ps_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e zynq_ultra_ps_e_0]
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } $ps_cell

# Enable IRQ0 on PS, disable unused second AXI master (HPM1)
set_property -dict [list CONFIG.PSU__USE__IRQ0 {1} CONFIG.PSU__USE__M_AXI_GP1 {0}] $ps_cell

# 2. Instantiate SEQ_GPU and PARALLEL_GPU
set seq_cell [create_bd_cell -type ip -vlnv QGAOPS:hls:seq_gpu:1.0 seq_gpu_0]
set par_cell [create_bd_cell -type ip -vlnv QGAOPS:hls:parallel_gpu:1.0 parallel_gpu_0]

# 3. Connection automation for AXI interfaces (SmartConnect + Processor System Reset)
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { \
    Master "/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD" \
    Clk "Auto" \
} [get_bd_intf_pins seq_gpu_0/s_axi_control]

apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { \
    Master "/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD" \
    Clk "Auto" \
} [get_bd_intf_pins parallel_gpu_0/s_axi_control]

# 4. Interrupts: Concat IP
set concat_cell [create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat xlconcat_0]
set_property -dict [list CONFIG.NUM_PORTS {2}] $concat_cell
connect_bd_net [get_bd_pins seq_gpu_0/interrupt] [get_bd_pins xlconcat_0/In0]
connect_bd_net [get_bd_pins parallel_gpu_0/interrupt] [get_bd_pins xlconcat_0/In1]
connect_bd_net [get_bd_pins xlconcat_0/dout] [get_bd_pins zynq_ultra_ps_e_0/pl_ps_irq0]

# 5. Address assignment
assign_bd_address
set_property offset 0xA0000000 [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_seq_gpu_0_Reg}]
set_property range 64K [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_seq_gpu_0_Reg}]

set_property offset 0xA0010000 [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_parallel_gpu_0_Reg}]
set_property range 64K [get_bd_addr_segs {zynq_ultra_ps_e_0/Data/SEG_parallel_gpu_0_Reg}]

# 6. Validate BD
validate_bd_design
save_bd_design

puts "=== BLOCK DESIGN VALIDATION PASSED ==="

# Print Address Map
puts "=== ASSIGNED ADDRESS MAP ==="
foreach seg [get_bd_addr_segs -of_objects [get_bd_addr_spaces /zynq_ultra_ps_e_0/Data]] {
    puts "Segment: $seg"
    puts "  Offset: [get_property offset $seg]"
    puts "  Range:  [get_property range $seg]"
}

# 7. Write BD Tcl for standalone generation
write_bd_tcl -force "$proj_dir/scripts/create_bd.tcl"
puts "Wrote standalone BD script to $proj_dir/scripts/create_bd.tcl"

# 8. Create HDL Wrapper
set bd_file [get_files qgpu_bd.bd]
set wrapper_file [make_wrapper -files $bd_file -top]
add_files -norecurse $wrapper_file
update_compile_order -fileset sources_1
puts "Wrapper generated: $wrapper_file"

exit 0
