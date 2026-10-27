set moduleName compute_gp_seq_core_Pipeline_RESCALE_LOOP
set isTopModule 0
set isCombinational 0
set isDatapathOnly 0
set isPipelined 1
set isPipelined_legacy 1
set pipeline_type loop_auto_rewind
set FunctionProtocol ap_ctrl_hs
set restart_counter_num 0
set isOneStateSeq 0
set ProfileFlag 0
set StallSigGenFlag 0
set isEnableWaveformDebug 1
set hasInterrupt 0
set DLRegFirstOffset 0
set DLRegItemOffset 0
set svuvm_can_support 1
set cdfgNum 27
set C_modelName {compute_gp_seq_core_Pipeline_RESCALE_LOOP}
set C_modelType { void 0 }
set ap_memory_interface_dict [dict create]
dict set ap_memory_interface_dict c { MEM_WIDTH 32 MEM_SIZE 32 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 0 }
set C_modelArgList {
	{ accum_load_reload int 67 regular  }
	{ accum_1_load_reload int 67 regular  }
	{ accum_2_load_reload int 67 regular  }
	{ accum_3_load_reload int 67 regular  }
	{ accum_4_load_reload int 67 regular  }
	{ accum_5_load_reload int 67 regular  }
	{ accum_6_load_reload int 67 regular  }
	{ accum_7_load_reload int 67 regular  }
	{ c int 32 regular {array 8 { 0 3 } 0 1 }  }
	{ write_flag_0_out int 1 regular {pointer 1}  }
	{ overflow_0_out int 1 regular {pointer 1}  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "accum_load_reload", "interface" : "wire", "bitwidth" : 67, "direction" : "READONLY"} , 
 	{ "Name" : "accum_1_load_reload", "interface" : "wire", "bitwidth" : 67, "direction" : "READONLY"} , 
 	{ "Name" : "accum_2_load_reload", "interface" : "wire", "bitwidth" : 67, "direction" : "READONLY"} , 
 	{ "Name" : "accum_3_load_reload", "interface" : "wire", "bitwidth" : 67, "direction" : "READONLY"} , 
 	{ "Name" : "accum_4_load_reload", "interface" : "wire", "bitwidth" : 67, "direction" : "READONLY"} , 
 	{ "Name" : "accum_5_load_reload", "interface" : "wire", "bitwidth" : 67, "direction" : "READONLY"} , 
 	{ "Name" : "accum_6_load_reload", "interface" : "wire", "bitwidth" : 67, "direction" : "READONLY"} , 
 	{ "Name" : "accum_7_load_reload", "interface" : "wire", "bitwidth" : 67, "direction" : "READONLY"} , 
 	{ "Name" : "c", "interface" : "memory", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "write_flag_0_out", "interface" : "wire", "bitwidth" : 1, "direction" : "WRITEONLY"} , 
 	{ "Name" : "overflow_0_out", "interface" : "wire", "bitwidth" : 1, "direction" : "WRITEONLY"} ]}
# RTL Port declarations: 
set portNum 22
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ accum_load_reload sc_in sc_lv 67 signal 0 } 
	{ accum_1_load_reload sc_in sc_lv 67 signal 1 } 
	{ accum_2_load_reload sc_in sc_lv 67 signal 2 } 
	{ accum_3_load_reload sc_in sc_lv 67 signal 3 } 
	{ accum_4_load_reload sc_in sc_lv 67 signal 4 } 
	{ accum_5_load_reload sc_in sc_lv 67 signal 5 } 
	{ accum_6_load_reload sc_in sc_lv 67 signal 6 } 
	{ accum_7_load_reload sc_in sc_lv 67 signal 7 } 
	{ c_address0 sc_out sc_lv 3 signal 8 } 
	{ c_ce0 sc_out sc_logic 1 signal 8 } 
	{ c_we0 sc_out sc_logic 1 signal 8 } 
	{ c_d0 sc_out sc_lv 32 signal 8 } 
	{ write_flag_0_out sc_out sc_lv 1 signal 9 } 
	{ write_flag_0_out_ap_vld sc_out sc_logic 1 outvld 9 } 
	{ overflow_0_out sc_out sc_lv 1 signal 10 } 
	{ overflow_0_out_ap_vld sc_out sc_logic 1 outvld 10 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "accum_load_reload", "direction": "in", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_load_reload", "role": "default" }} , 
 	{ "name": "accum_1_load_reload", "direction": "in", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_1_load_reload", "role": "default" }} , 
 	{ "name": "accum_2_load_reload", "direction": "in", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_2_load_reload", "role": "default" }} , 
 	{ "name": "accum_3_load_reload", "direction": "in", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_3_load_reload", "role": "default" }} , 
 	{ "name": "accum_4_load_reload", "direction": "in", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_4_load_reload", "role": "default" }} , 
 	{ "name": "accum_5_load_reload", "direction": "in", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_5_load_reload", "role": "default" }} , 
 	{ "name": "accum_6_load_reload", "direction": "in", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_6_load_reload", "role": "default" }} , 
 	{ "name": "accum_7_load_reload", "direction": "in", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_7_load_reload", "role": "default" }} , 
 	{ "name": "c_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "c", "role": "address0" }} , 
 	{ "name": "c_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "c", "role": "ce0" }} , 
 	{ "name": "c_we0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "c", "role": "we0" }} , 
 	{ "name": "c_d0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c", "role": "d0" }} , 
 	{ "name": "write_flag_0_out", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "write_flag_0_out", "role": "default" }} , 
 	{ "name": "write_flag_0_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "write_flag_0_out", "role": "ap_vld" }} , 
 	{ "name": "overflow_0_out", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "overflow_0_out", "role": "default" }} , 
 	{ "name": "overflow_0_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "overflow_0_out", "role": "ap_vld" }}  ]}

set ArgLastReadFirstWriteLatency {
	compute_gp_seq_core_Pipeline_RESCALE_LOOP {
		accum_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_1_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_2_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_3_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_4_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_5_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_6_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_7_load_reload {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 2}
		write_flag_0_out {Type O LastRead -1 FirstWrite 1}
		overflow_0_out {Type O LastRead -1 FirstWrite 1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "11", "Max" : "11"}
	, {"Name" : "Interval", "Min" : "9", "Max" : "9"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
]}

set Spec2ImplPortList { 
	accum_load_reload { ap_none {  { accum_load_reload in_data 0 67 } } }
	accum_1_load_reload { ap_none {  { accum_1_load_reload in_data 0 67 } } }
	accum_2_load_reload { ap_none {  { accum_2_load_reload in_data 0 67 } } }
	accum_3_load_reload { ap_none {  { accum_3_load_reload in_data 0 67 } } }
	accum_4_load_reload { ap_none {  { accum_4_load_reload in_data 0 67 } } }
	accum_5_load_reload { ap_none {  { accum_5_load_reload in_data 0 67 } } }
	accum_6_load_reload { ap_none {  { accum_6_load_reload in_data 0 67 } } }
	accum_7_load_reload { ap_none {  { accum_7_load_reload in_data 0 67 } } }
	c { ap_memory {  { c_address0 mem_address 1 3 }  { c_ce0 mem_ce 1 1 }  { c_we0 mem_we 1 1 }  { c_d0 mem_din 1 32 } } }
	write_flag_0_out { ap_vld {  { write_flag_0_out out_data 1 1 }  { write_flag_0_out_ap_vld out_vld 1 1 } } }
	overflow_0_out { ap_vld {  { overflow_0_out out_data 1 1 }  { overflow_0_out_ap_vld out_vld 1 1 } } }
}
