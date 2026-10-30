open_project D:/QGPU/HW/vivado/SEQ_GPU_PYNQZU/SEQ_GPU_PYNQZU.xpr
puts "Simulation fileset: [get_filesets sim_1]"
puts "Simulation top: [get_property top [get_filesets sim_1]]"
puts "Target simulator: [get_property target_simulator [current_project]]"
close_project
exit
