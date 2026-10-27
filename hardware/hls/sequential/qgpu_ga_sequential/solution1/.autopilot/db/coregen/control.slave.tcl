dict set slaves control {ports {opcode {type i_ap_none width 32} a {type i_ap_memory width 32} b {type i_ap_memory width 32} c {type o_ap_memory width 32} status {type o_ap_vld width 32} ap_start {type ap_ctrl width 1} ap_done {type ap_ctrl width 1} ap_ready {type ap_ctrl width 1} ap_idle {type ap_ctrl width 1}} mems {a {width 32} b {width 32} c {width 32}} has_ctrl 1}
set datawidth 32
set addrwidth 64
set intr_clr_mode TOW
