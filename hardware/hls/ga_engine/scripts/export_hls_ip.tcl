# ==============================================================================
# Vitis HLS Tcl Script: IP Export / Packaging
# Target Board : PYNQ-Z2
# Target Part  : xc7z020clg400-1
# ==============================================================================

open_project prj_qgpu_ga_csim
open_solution "solution1"

puts "=================================================================="
puts "  EXPORTING VITIS HLS IP TO IP CATALOG"
puts "=================================================================="
export_design -format ip_catalog \
              -description "QGAOPS-QGPU Cl(3,0) Geometric Algebra Accelerator IP" \
              -vendor "qgpu" \
              -library "hls" \
              -version "1.0" \
              -display_name "QGPU_GA_Engine"

exit
