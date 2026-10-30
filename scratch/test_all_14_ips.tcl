create_project -in_memory -part xczu5eg-sfvc784-1-e
set_property board_part tul.com.tw:pynqzu:part0:1.1 [current_project]

set_property ip_repo_paths [list \
    [file normalize "D:/QGPU/HW/vitis/SEQ_GPU/work/hls/impl/ip"] \
    [file normalize "D:/QGPU/HW/vitis/PARALLEL_GPU/work/hls/impl/ip"] \
] [current_project]
update_ip_catalog

create_bd_design "test_all_ips"

# 1. PS
set ps [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e zynq_ultra_ps_e_0]
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } $ps
set_property -dict [list \
    CONFIG.PSU__USE__IRQ0 {1} \
    CONFIG.PSU__USE__M_AXI_GP1 {0} \
    CONFIG.PSU__USE__S_AXI_GP2 {1} \
] $ps

# 2. Clocking Wizard
set clk_wiz [create_bd_cell -type ip -vlnv xilinx.com:ip:clk_wiz clk_wiz_0]
set_property -dict [list \
    CONFIG.CLKOUT1_REQUESTED_OUT_FREQ {100.000} \
    CONFIG.CLKOUT2_REQUESTED_OUT_FREQ {200.000} \
    CONFIG.CLKOUT2_USED {true} \
    CONFIG.USE_RESET {false} \
] $clk_wiz

# 3. Proc Sys Reset
set rst [create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset rst_ps8_0_100M]

# 4. SmartConnect Control (1 SI, 4 MI)
set smc_ctrl [create_bd_cell -type ip -vlnv xilinx.com:ip:smartconnect:1.0 smartconnect_ctrl]
set_property -dict [list CONFIG.NUM_SI {1} CONFIG.NUM_MI {4}] $smc_ctrl

# 5. SmartConnect DMA (2 SI, 1 MI)
set smc_dma [create_bd_cell -type ip -vlnv xilinx.com:ip:smartconnect:1.0 smartconnect_dma]
set_property -dict [list CONFIG.NUM_SI {2} CONFIG.NUM_MI {1}] $smc_dma

# 6. Accelerator
set accel [create_bd_cell -type ip -vlnv QGAOPS:hls:seq_gpu:1.0 seq_gpu_0]

# 7. AXI Register Slice
set reg_slice [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_register_slice axi_register_slice_0]

# 8. AXI Protocol Checker
set pc [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_protocol_checker axi_protocol_checker_0]

# 9. AXI DMA
set dma [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_dma axi_dma_0]
set_property -dict [list \
    CONFIG.c_include_sg {0} \
    CONFIG.c_sg_include_stscntrl_strm {0} \
] $dma

# 10. AXI4-Stream Data FIFO
set fifo [create_bd_cell -type ip -vlnv xilinx.com:ip:axis_data_fifo axis_data_fifo_0]

# 11. AXI Interrupt Controller
set intc [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_intc axi_intc_0]

# 12. AXI BRAM Controller + Block Memory Generator
set bram_ctrl [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_bram_ctrl axi_bram_ctrl_0]
set_property -dict [list CONFIG.SINGLE_PORT_BRAM {1}] $bram_ctrl
set bmem [create_bd_cell -type ip -vlnv xilinx.com:ip:blk_mem_gen blk_mem_gen_0]

# 13. System ILA
set ila [create_bd_cell -type ip -vlnv xilinx.com:ip:system_ila system_ila_0]
set_property -dict [list \
    CONFIG.C_NUM_MONITOR_SLOTS {2} \
    CONFIG.C_SLOT_0_INTF_TYPE {xilinx.com:interface:aximm_rtl:1.0} \
    CONFIG.C_SLOT_1_INTF_TYPE {xilinx.com:interface:axis_rtl:1.0} \
] $ila

puts "ALL 14 IPS CREATED SUCCESSFULLY IN MEMORY"
exit 0
