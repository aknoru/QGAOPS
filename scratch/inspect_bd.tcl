open_project D:/QGPU/HW/vivado/PARALLEL_GPU_PYNQZU/PARALLEL_GPU_PYNQZU.xpr
open_bd_design [get_files parallel_gpu_bd.bd]
puts "=== SMARTCONNECT MASTER INTERFACES ==="
puts [get_bd_intf_pins smartconnect_ctrl_0/M*]
puts "=== ALL CELLS IN BD ==="
puts [get_bd_cells]
close_project
exit
