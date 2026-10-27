# Export IP for sequential accelerator with fresh synthesis RTL and AXI4-Lite interface
open_project qgpu_ga_sequential
open_solution solution1
source ./qgpu_ga_sequential/solution1/directives.tcl
csynth_design
export_design -format ip_catalog -vendor qgpu -library hls -version 1.0 -display_name qgpu_ga_sequential_ip
exit
