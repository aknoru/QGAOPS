# This script segment is generated automatically by AutoPilot

if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler qgpu_ga_parallel_top_sparsemux_17_3_2_1_1 BINDTYPE {op} TYPE {sparsemux} IMPL {compactencoding_dontcare}
}


if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler qgpu_ga_parallel_top_sparsemux_5_8_3_1_1 BINDTYPE {op} TYPE {sparsemux} IMPL {compactencoding_realdef}
}


if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler qgpu_ga_parallel_top_sparsemux_17_3_67_1_1 BINDTYPE {op} TYPE {sparsemux} IMPL {compactencoding_dontcare}
}


if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler qgpu_ga_parallel_top_compute_gp_core_BASIS_MASKS_ROM_AUTO_1R BINDTYPE {storage} TYPE {rom} IMPL {auto} LATENCY 2 ALLOW_PRAGMA 1
}


# clear list
if {${::AESL::PGuard_autoexp_gen}} {
    cg_default_interface_gen_dc_begin
    cg_default_interface_gen_bundle_begin
    AESL_LIB_XILADAPTER::native_axis_begin
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 114 \
    name a_0_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_a_0_val \
    op interface \
    ports { a_0_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 115 \
    name a_1_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_a_1_val \
    op interface \
    ports { a_1_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 116 \
    name a_2_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_a_2_val \
    op interface \
    ports { a_2_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 117 \
    name a_3_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_a_3_val \
    op interface \
    ports { a_3_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 118 \
    name a_4_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_a_4_val \
    op interface \
    ports { a_4_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 119 \
    name a_5_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_a_5_val \
    op interface \
    ports { a_5_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 120 \
    name a_6_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_a_6_val \
    op interface \
    ports { a_6_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 121 \
    name a_7_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_a_7_val \
    op interface \
    ports { a_7_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 122 \
    name b_0_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_b_0_val \
    op interface \
    ports { b_0_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 123 \
    name b_1_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_b_1_val \
    op interface \
    ports { b_1_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 124 \
    name b_2_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_b_2_val \
    op interface \
    ports { b_2_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 125 \
    name b_3_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_b_3_val \
    op interface \
    ports { b_3_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 126 \
    name b_4_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_b_4_val \
    op interface \
    ports { b_4_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 127 \
    name b_5_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_b_5_val \
    op interface \
    ports { b_5_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 128 \
    name b_6_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_b_6_val \
    op interface \
    ports { b_6_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 129 \
    name b_7_val \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_b_7_val \
    op interface \
    ports { b_7_val { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 130 \
    name opcode \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_opcode \
    op interface \
    ports { opcode { I 2 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 131 \
    name overflow_read \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_overflow_read \
    op interface \
    ports { overflow_read { I 1 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id -1 \
    name ap_ctrl \
    type ap_ctrl \
    reset_level 1 \
    sync_rst true \
    corename ap_ctrl \
    op interface \
    ports { ap_start { I 1 bit } ap_ready { O 1 bit } ap_done { O 1 bit } ap_idle { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id -2 \
    name ap_return \
    type ap_return \
    reset_level 1 \
    sync_rst true \
    corename ap_return \
    op interface \
    ports { ap_return { O 1 vector } } \
} "
}


# Adapter definition:
set PortName ap_clk
set DataWd 1 
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc cg_default_interface_gen_clock] == "cg_default_interface_gen_clock"} {
eval "cg_default_interface_gen_clock { \
    id -3 \
    name ${PortName} \
    reset_level 1 \
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
set PortName ap_rst
set DataWd 1 
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc cg_default_interface_gen_reset] == "cg_default_interface_gen_reset"} {
eval "cg_default_interface_gen_reset { \
    id -4 \
    name ${PortName} \
    reset_level 1 \
    sync_rst true \
    corename apif_ap_rst \
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


