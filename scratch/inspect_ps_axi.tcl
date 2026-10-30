open_project D:/QGPU/HW/vivado/QGAOPS_QGPU_PYNQZU.xpr
open_bd_design [get_files qgpu_bd.bd]
set intfs [get_bd_intf_pins zynq_ultra_ps_e_0/*]
puts "PS INTF PINS: $intfs"
set axi_props [list_property [get_bd_cells zynq_ultra_ps_e_0] *HPM*]
puts "PS HPM PROPS: $axi_props"
exit 0
