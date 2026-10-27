# Dedicated synthesis, co-simulation, and export for IP A (sequential accelerator)
open_project qgpu_ga_sequential
open_solution solution1
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top a
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top b
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top c
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top opcode
set_directive_interface -mode s_axilite -bundle control qgpu_ga_sequential_top status
csynth_design
exit
