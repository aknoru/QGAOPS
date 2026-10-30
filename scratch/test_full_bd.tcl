# Open project and BD
open_project D:/QGPU/HW/vivado/QGAOPS_QGPU_PYNQZU.xpr
open_bd_design [get_files qgpu_bd.bd]

# Instantiate SEQ_GPU and PARALLEL_GPU
set seq_ip [create_bd_cell -type ip -vlnv QGAOPS:hls:seq_gpu:1.0 seq_gpu_0]
set par_ip [create_bd_cell -type ip -vlnv QGAOPS:hls:parallel_gpu:1.0 parallel_gpu_0]

puts "IPs instantiated successfully"

# Apply connection automation for AXI interfaces
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { \
    Master "/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD" \
    Clk "Auto" \
} [get_bd_intf_pins seq_gpu_0/s_axi_control]

apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { \
    Master "/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD" \
    Clk "Auto" \
} [get_bd_intf_pins parallel_gpu_0/s_axi_control]

puts "AXI connection automation completed"

# Check interrupts: enable pl_ps_irq0 on Zynq PS
set_property -dict [list CONFIG.PSU__USE__IRQ0 {1}] [get_bd_cells zynq_ultra_ps_e_0]
set concat_ip [create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat xlconcat_0]
set_property -dict [list CONFIG.NUM_PORTS {2}] $concat_ip

connect_bd_net [get_bd_pins seq_gpu_0/interrupt] [get_bd_pins xlconcat_0/In0]
connect_bd_net [get_bd_pins parallel_gpu_0/interrupt] [get_bd_pins xlconcat_0/In1]
connect_bd_net [get_bd_pins xlconcat_0/dout] [get_bd_pins zynq_ultra_ps_e_0/pl_ps_irq0]

puts "Interrupts connected successfully"

# Validate BD design
validate_bd_design
puts "BD validated successfully"

# Check address segments
set segs [get_bd_addr_segs]
foreach seg $segs {
    puts "ADDR_SEG: $seg -> Offset: [get_property offset $seg] Range: [get_property range $seg]"
}

save_bd_design
exit 0
