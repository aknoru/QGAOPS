# Dedicated Vitis HLS project for IP B: parallel/pipelined accelerator.
open_project -reset qgpu_ga_parallel
set_top qgpu_ga_parallel_top
add_files ../ga_engine/src/qgpu_ga_parallel_top.cpp -cflags "-I../ga_engine/include"
add_files ../ga_engine/src/qgpu_ga_engine_parallel.cpp -cflags "-I../ga_engine/include"
add_files -tb ../ga_engine/tb/tb_qgpu_ga_engine.cpp -cflags "-I../ga_engine/include -DQGPU_TEST_PARALLEL_ONLY"
add_files -tb ../ga_engine/vectors/golden_vectors.csv
open_solution -reset solution1 -flow_target vivado
set_part {xc7z020clg400-1}
create_clock -period 10.0 -name default
csim_design -argv "../ga_engine/vectors/golden_vectors.csv"
# Run these GUI-visible commands separately after a successful C simulation:
# csynth_design; cosim_design -trace_level all -argv "../ga_engine/vectors/golden_vectors.csv";
# export_design -format ip_catalog -vendor qgpu -library hls -version 1.0 -display_name qgpu_ga_parallel_ip
exit
