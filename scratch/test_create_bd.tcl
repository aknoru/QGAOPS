# Test creating project and BD
set proj_name "QGAOPS_QGPU_PYNQZU"
set proj_dir "D:/QGPU/HW/vivado"
file mkdir $proj_dir
file mkdir "$proj_dir/scripts"
file mkdir "$proj_dir/reports"
file mkdir "$proj_dir/bd"

create_project -force $proj_name $proj_dir -part xczu5eg-sfvc784-1-e
set_property board_part tul.com.tw:pynqzu:part0:1.1 [current_project]

set_property ip_repo_paths [list D:/QGPU/HW/vitis/SEQ_GPU/work/hls/impl/ip D:/QGPU/HW/vitis/PARALLEL_GPU/work/hls/impl/ip] [current_project]
update_ip_catalog

# Create Block Design
create_bd_design "qgpu_bd"

# Instantiate Zynq UltraScale+ MPSoC
set ps_ip [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e zynq_ultra_ps_e_0]

# Apply board automation for PS
catch {
    apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" } [get_bd_cells zynq_ultra_ps_e_0]
}

puts "PS applied board preset successfully"

# Check available pins on PS
set ps_pins [get_bd_pins zynq_ultra_ps_e_0/*]
puts "PS pins found: [llength $ps_pins]"

exit 0
