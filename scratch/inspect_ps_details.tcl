create_project -in_memory -part xczu5eg-sfvc784-1-e
set_property board_part tul.com.tw:pynqzu:part0:1.1 [current_project]
create_bd_design "test_bd"
set ps [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e ps_0]
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } [get_bd_cells ps_0]

puts "--- INTF PINS ---"
foreach p [get_bd_intf_pins ps_0/*] {
    puts "INTF_PIN: $p"
}

puts "--- PINS ---"
foreach p [get_bd_pins ps_0/*clk*] {
    puts "CLK_PIN: $p"
}
foreach p [get_bd_pins ps_0/*rst*] {
    puts "RST_PIN: $p"
}

puts "--- M_AXI PROPERTIES ---"
foreach prop [list_property $ps *HPM*] {
    puts "PROP: $prop = [get_property $prop $ps]"
}

exit 0
