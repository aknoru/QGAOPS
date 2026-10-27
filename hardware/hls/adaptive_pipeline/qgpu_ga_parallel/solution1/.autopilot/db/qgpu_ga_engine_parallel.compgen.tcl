# This script segment is generated automatically by AutoPilot

set name qgpu_ga_parallel_top_mul_32s_32s_64_2_1
if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler $name BINDTYPE {op} TYPE {mul} IMPL {auto} LATENCY 1 ALLOW_PRAGMA 1
}


if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler qgpu_ga_parallel_top_qgpu_ga_engine_parallel_aamf_bank_a_RAM_2P_BRAM_1R1W BINDTYPE {storage} TYPE {ram_2p} IMPL {bram} LATENCY 2 ALLOW_PRAGMA 1
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
    id 292 \
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
    id 293 \
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
    id 294 \
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
    id 295 \
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
    id 296 \
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
    id 297 \
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
    id 298 \
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
    id 299 \
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
    id 300 \
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
    id 301 \
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
    id 302 \
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
    id 303 \
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
    id 304 \
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
    id 305 \
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
    id 306 \
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
    id 307 \
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
    id 308 \
    name c_0 \
    type other \
    dir O \
    reset_level 1 \
    sync_rst true \
    corename dc_c_0 \
    op interface \
    ports { c_0 { O 32 vector } c_0_ap_vld { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 309 \
    name c_1 \
    type other \
    dir O \
    reset_level 1 \
    sync_rst true \
    corename dc_c_1 \
    op interface \
    ports { c_1 { O 32 vector } c_1_ap_vld { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 310 \
    name c_2 \
    type other \
    dir O \
    reset_level 1 \
    sync_rst true \
    corename dc_c_2 \
    op interface \
    ports { c_2 { O 32 vector } c_2_ap_vld { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 311 \
    name c_3 \
    type other \
    dir O \
    reset_level 1 \
    sync_rst true \
    corename dc_c_3 \
    op interface \
    ports { c_3 { O 32 vector } c_3_ap_vld { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 312 \
    name c_4 \
    type other \
    dir O \
    reset_level 1 \
    sync_rst true \
    corename dc_c_4 \
    op interface \
    ports { c_4 { O 32 vector } c_4_ap_vld { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 313 \
    name c_5 \
    type other \
    dir O \
    reset_level 1 \
    sync_rst true \
    corename dc_c_5 \
    op interface \
    ports { c_5 { O 32 vector } c_5_ap_vld { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 314 \
    name c_6 \
    type other \
    dir O \
    reset_level 1 \
    sync_rst true \
    corename dc_c_6 \
    op interface \
    ports { c_6 { O 32 vector } c_6_ap_vld { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 315 \
    name c_7 \
    type other \
    dir O \
    reset_level 1 \
    sync_rst true \
    corename dc_c_7 \
    op interface \
    ports { c_7 { O 32 vector } c_7_ap_vld { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 316 \
    name opcode \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_opcode \
    op interface \
    ports { opcode { I 22 vector } } \
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
    ports { ap_return { O 32 vector } } \
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


