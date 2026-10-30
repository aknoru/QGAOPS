open_project D:/QGPU/HW/vivado/SEQ_GPU_PYNQZU/SEQ_GPU_PYNQZU.xpr
open_bd_design [get_files seq_gpu_bd.bd]
puts "Currently assigned segments:"
foreach seg [get_bd_addr_segs] {
    puts "seg: $seg"
}
close_project
exit
