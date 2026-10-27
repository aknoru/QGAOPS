# Dedicated Vitis HLS project for IP A: resource-shared sequential accelerator.
open_project -reset qgpu_ga_sequential
set_top qgpu_ga_sequential_top
add_files ../ga_engine/src/qgpu_ga_sequential_top.cpp -cflags "-I../ga_engine/include"
add_files ../ga_engine/src/qgpu_ga_engine_shared.cpp -cflags "-I../ga_engine/include"
add_files -tb ../ga_engine/tb/tb_qgpu_ga_engine.cpp -cflags "-I../ga_engine/include -DQGPU_TEST_SEQUENTIAL_ONLY"
add_files -tb ../ga_engine/vectors/golden_vectors.csv
open_solution -reset solution1 -flow_target vivado
set_part {xc7z020clg400-1}
create_clock -period 10.0 -name default
# The baseline source intentionally has no HLS pragmas.  Keep the control
# interface as project configuration rather than embedding directives in C++.
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top a
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top b
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top c
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top opcode
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top status
csim_design -argv "../ga_engine/vectors/golden_vectors.csv"
# Run these GUI-visible commands separately after a successful C simulation:
# csynth_design; cosim_design -trace_level all -argv "../ga_engine/vectors/golden_vectors.csv";
# export_design -format ip_catalog -vendor qgpu -library hls -version 1.0 -display_name qgpu_ga_sequential_ip
exit
