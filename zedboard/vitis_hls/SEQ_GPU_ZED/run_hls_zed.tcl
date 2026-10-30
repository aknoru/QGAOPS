set proj_dir "D:/QGPU/zedboard/vitis_hls/SEQ_GPU_ZED/work"
file mkdir $proj_dir
cd $proj_dir

open_project -reset proj_seq_zed
set_top seq_gpu
add_files D:/QGPU/HW/hls/SEQ_GPU/src/seq_gpu.cpp -cflags "-std=c++14 -ID:/QGPU/HW/hls/common/include -ID:/QGPU/HW/hls/SEQ_GPU/include"
add_files -tb D:/QGPU/HW/hls/SEQ_GPU/testbench/tb_seq_gpu.cpp -cflags "-std=c++14 -ID:/QGPU/HW/hls/common/include -ID:/QGPU/HW/hls/common/tests -ID:/QGPU/HW/hls/SEQ_GPU/include"

open_solution -reset "solution1" -flow_target vivado
set_part {xc7z020clg484-1}
create_clock -period 10.0 -name default

puts "=== RUNNING CSIM FOR ZEDBOARD ==="
csim_design

puts "=== RUNNING CSYNTH FOR ZEDBOARD ==="
csynth_design

puts "=== RUNNING EXPORT IP FOR ZEDBOARD ==="
export_design -format ip_catalog -vendor "QGAOPS" -version "1.0" -display_name "SEQ_GPU_ZED"
exit

