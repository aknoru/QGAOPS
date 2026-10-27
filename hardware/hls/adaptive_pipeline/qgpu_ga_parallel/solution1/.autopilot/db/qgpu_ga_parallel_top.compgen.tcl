# This script segment is generated automatically by AutoPilot

# clear list
if {${::AESL::PGuard_autoexp_gen}} {
    cg_default_interface_gen_dc_begin
    cg_default_interface_gen_bundle_begin
    AESL_LIB_XILADAPTER::native_axis_begin
}

set axilite_register_dict [dict create]
set port_control {
a_0 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 16
	offset_end 23
}
a_1 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 24
	offset_end 31
}
a_2 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 32
	offset_end 39
}
a_3 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 40
	offset_end 47
}
a_4 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 48
	offset_end 55
}
a_5 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 56
	offset_end 63
}
a_6 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 64
	offset_end 71
}
a_7 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 72
	offset_end 79
}
b_0 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 80
	offset_end 87
}
b_1 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 88
	offset_end 95
}
b_2 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 96
	offset_end 103
}
b_3 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 104
	offset_end 111
}
b_4 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 112
	offset_end 119
}
b_5 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 120
	offset_end 127
}
b_6 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 128
	offset_end 135
}
b_7 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 136
	offset_end 143
}
c_0 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 144
	offset_end 151
}
c_1 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 160
	offset_end 167
}
c_2 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 176
	offset_end 183
}
c_3 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 192
	offset_end 199
}
c_4 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 208
	offset_end 215
}
c_5 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 224
	offset_end 231
}
c_6 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 240
	offset_end 247
}
c_7 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 256
	offset_end 263
}
opcode { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 272
	offset_end 279
}
status { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 280
	offset_end 287
}
ap_start { }
ap_done { }
ap_ready { }
ap_idle { }
interrupt {
}
}
dict set axilite_register_dict control $port_control


# Native S_AXILite:
if {${::AESL::PGuard_simmodel_gen}} {
	if {[info proc ::AESL_LIB_XILADAPTER::s_axilite_gen] == "::AESL_LIB_XILADAPTER::s_axilite_gen"} {
		eval "::AESL_LIB_XILADAPTER::s_axilite_gen { \
			id 317 \
			corename qgpu_ga_parallel_top_control_axilite \
			name qgpu_ga_parallel_top_control_s_axi \
			ports {$port_control} \
			op interface \
			interrupt_clear_mode TOW \
			interrupt_trigger_type default \
			is_flushable 0 \
			is_datawidth64 0 \
			is_addrwidth64 1 \
			enable_mem_auto_widen 1 \
		} "
	} else {
		puts "@W \[IMPL-110\] Cannot find AXI Lite interface model in the library. Ignored generation of AXI Lite  interface for 'control'"
	}
}

if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler qgpu_ga_parallel_top_control_s_axi BINDTYPE interface TYPE interface_s_axilite
}


# Adapter definition:
set PortName ap_clk
set DataWd 1 
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc cg_default_interface_gen_clock] == "cg_default_interface_gen_clock"} {
eval "cg_default_interface_gen_clock { \
    id -1 \
    name ${PortName} \
    reset_level 0 \
    sync_rst true \
    corename apif_ap_clk \
    data_wd ${DataWd} \
    op interface \
}"
} else {
puts "@W \[IMPL-113\] Cannot find bus interface model in the library. Ignored generation of bus interface for '${PortName}'"
}
}


# Adapter definition:
set PortName ap_rst_n
set DataWd 1 
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc cg_default_interface_gen_reset] == "cg_default_interface_gen_reset"} {
eval "cg_default_interface_gen_reset { \
    id -2 \
    name ${PortName} \
    reset_level 0 \
    sync_rst true \
    corename apif_ap_rst_n \
    data_wd ${DataWd} \
    op interface \
}"
} else {
puts "@W \[IMPL-114\] Cannot find bus interface model in the library. Ignored generation of bus interface for '${PortName}'"
}
}



# merge
if {${::AESL::PGuard_autoexp_gen}} {
    cg_default_interface_gen_dc_end
    cg_default_interface_gen_bundle_end
    AESL_LIB_XILADAPTER::native_axis_end
}


