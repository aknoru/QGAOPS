create_project -in_memory -part xczu5eg-sfvc784-1-e
set_property board_part tul.com.tw:pynqzu:part0:1.1 [current_project]
create_bd_design "test_bd"
set ps [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e ps_0]
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } [get_bd_cells ps_0]
foreach p [list_property $ps *GP*] {
    puts "GP_PROP: $p = [get_property $p $ps]"
}
exit 0
