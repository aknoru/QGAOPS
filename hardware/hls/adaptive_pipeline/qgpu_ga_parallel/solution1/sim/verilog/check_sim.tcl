# ==============================================================
# Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
# Tool Version Limit: 2025.11
# Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
# Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
# 
# ==============================================================
proc sc_sim_check {ret err logfile} {
	if {$::AESL_AUTOSIM::gDebug == 1} {
		puts stdout "[debug_prompt arg check_sim.tcl] start...";
	}
    set errfile "err.log"
    if {[file exists $errfile] && [file size $errfile] != 0} {
        set fl [open $errfile r]
        while {[gets $fl line] >= 0} {
            if {[string first "AESL_mErrNo = " $line] == 0} {
                set mismatch_num [string range $line [string length "AESL_mErrNo = "] end]
                if {$mismatch_num != 0} {
                    ::AP::printMsg ERR COSIM 403 COSIM_403_986 ${mismatch_num}
                    break
                }
            }
        }
    }
    if {$ret || $err != ""} {
        if { [lindex $::errorCode 0] eq "CHILDSTATUS"} {
            set status [lindex $::errorCode 2]
            if {$status != ""} {
                ::AP::printMsg ERR COSIM 404 COSIM_404_987 $status
            } else {
                ::AP::printMsg ERR COSIM 405 COSIM_405_988
            }
        } else {
            ::AP::printMsg ERR COSIM 405 COSIM_405_989
        }
    }
	if {$::AESL_AUTOSIM::gDebug == 1} {
		puts stdout "[debug_prompt arg check_sim.tcl] finish...";
	}
}

proc rtl_sim_check {} {
	if {$::AESL_AUTOSIM::gDebug == 1} {
		puts stdout "[debug_prompt arg check_sim.tcl] start...";
	}
    set errfile "err.log"
    if {[file exists $errfile] && [file size $errfile] != 0} {
        set fl [open $errfile r]
        set unmatch_num 0
        while {[gets $fl line] >= 0} {
            if {[string first "unmatched" $line] != -1} {
                set unmatch_num [expr $unmatch_num + 1]
            }
        }
        if {$unmatch_num != 0} {
            ::AP::printMsg ERR COSIM 406 COSIM_406_991 ${unmatch_num}
        }
    }
    if {[file exists ".aesl_error"]} {
        set errfl [open ".aesl_error" r]
        gets $errfl line
        if {$line != 0} {
            ::AP::printMsg ERR COSIM 407 COSIM_407_992 $line
        }
    }
    if {[file exists ".exit.err"]} {
        ::AP::printMsg ERR COSIM 405 COSIM_405_993
    }
	if {$::AESL_AUTOSIM::gDebug == 1} {
		puts stdout "[debug_prompt arg check_sim.tcl] finish...";
	}
}

proc check_tvin_file {} {
	if {$::AESL_AUTOSIM::gDebug == 1} {
		puts stdout "[debug_prompt arg check_sim.tcl] start...";
	}
    set rtlfilelist {
         "c.qgpu_ga_parallel_top.autotvin_a_0.dat"
         "c.qgpu_ga_parallel_top.autotvin_a_1.dat"
         "c.qgpu_ga_parallel_top.autotvin_a_2.dat"
         "c.qgpu_ga_parallel_top.autotvin_a_3.dat"
         "c.qgpu_ga_parallel_top.autotvin_a_4.dat"
         "c.qgpu_ga_parallel_top.autotvin_a_5.dat"
         "c.qgpu_ga_parallel_top.autotvin_a_6.dat"
         "c.qgpu_ga_parallel_top.autotvin_a_7.dat"
         "c.qgpu_ga_parallel_top.autotvin_b_0.dat"
         "c.qgpu_ga_parallel_top.autotvin_b_1.dat"
         "c.qgpu_ga_parallel_top.autotvin_b_2.dat"
         "c.qgpu_ga_parallel_top.autotvin_b_3.dat"
         "c.qgpu_ga_parallel_top.autotvin_b_4.dat"
         "c.qgpu_ga_parallel_top.autotvin_b_5.dat"
         "c.qgpu_ga_parallel_top.autotvin_b_6.dat"
         "c.qgpu_ga_parallel_top.autotvin_b_7.dat"
         "c.qgpu_ga_parallel_top.autotvin_opcode.dat"
    }
    foreach rtlfile $rtlfilelist {
        if {[file isfile $rtlfile]} {
        } else {
            ::AP::printMsg ERR COSIM 320 COSIM_320_994
            return 1
        }
    }
	if {$::AESL_AUTOSIM::gDebug == 1} {
		puts stdout "[debug_prompt arg check_sim.tcl] finish...";
	}
    return 0
}

proc check_tvout_file {} {
	if {$::AESL_AUTOSIM::gDebug == 1} {
		puts stdout "[debug_prompt arg check_sim.tcl] start...";
	}
    set rtlfilelist {
         "rtl.qgpu_ga_parallel_top.autotvout_c_0.dat"
         "rtl.qgpu_ga_parallel_top.autotvout_c_1.dat"
         "rtl.qgpu_ga_parallel_top.autotvout_c_2.dat"
         "rtl.qgpu_ga_parallel_top.autotvout_c_3.dat"
         "rtl.qgpu_ga_parallel_top.autotvout_c_4.dat"
         "rtl.qgpu_ga_parallel_top.autotvout_c_5.dat"
         "rtl.qgpu_ga_parallel_top.autotvout_c_6.dat"
         "rtl.qgpu_ga_parallel_top.autotvout_c_7.dat"
         "rtl.qgpu_ga_parallel_top.autotvout_status.dat"
    }
    foreach rtlfile $rtlfilelist {
        if {[file isfile $rtlfile]} {
        } else {
            ::AP::printMsg ERR COSIM 303 COSIM_303_996
            return 1
        }
    }
	if {$::AESL_AUTOSIM::gDebug == 1} {
		puts stdout "[debug_prompt arg check_sim.tcl] finish...";
	}
    return 0
}
