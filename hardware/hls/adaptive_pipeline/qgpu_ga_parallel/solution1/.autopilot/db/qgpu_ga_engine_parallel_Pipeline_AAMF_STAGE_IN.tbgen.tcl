set moduleName qgpu_ga_engine_parallel_Pipeline_AAMF_STAGE_IN
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
set cdfgNum 22
set C_modelName {qgpu_ga_engine_parallel_Pipeline_AAMF_STAGE_IN}
set C_modelType { void 0 }
set ap_memory_interface_dict [dict create]
dict set ap_memory_interface_dict aamf_bank_a { MEM_WIDTH 32 MEM_SIZE 2048 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 0 }
dict set ap_memory_interface_dict aamf_bank_b { MEM_WIDTH 32 MEM_SIZE 2048 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 0 }
set C_modelArgList {
	{ a_0_val int 32 regular  }
	{ a_1_val int 32 regular  }
	{ a_2_val int 32 regular  }
	{ a_3_val int 32 regular  }
	{ a_4_val int 32 regular  }
	{ a_5_val int 32 regular  }
	{ a_6_val int 32 regular  }
	{ a_7_val int 32 regular  }
	{ base_addr int 9 regular  }
	{ b_0_val int 32 regular  }
	{ b_1_val int 32 regular  }
	{ b_2_val int 32 regular  }
	{ b_3_val int 32 regular  }
	{ b_4_val int 32 regular  }
	{ b_5_val int 32 regular  }
	{ b_6_val int 32 regular  }
	{ b_7_val int 32 regular  }
	{ aamf_bank_a int 32 regular {array 512 { 3 0 } 0 1 } {global 1}  }
	{ aamf_bank_b int 32 regular {array 512 { 3 0 } 0 1 } {global 1}  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "a_0_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_1_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_2_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_3_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_4_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_5_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_6_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_7_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "base_addr", "interface" : "wire", "bitwidth" : 9, "direction" : "READONLY"} , 
 	{ "Name" : "b_0_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_1_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_2_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_3_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_4_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_5_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_6_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_7_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "aamf_bank_a", "interface" : "memory", "bitwidth" : 32, "direction" : "WRITEONLY", "extern" : 0} , 
 	{ "Name" : "aamf_bank_b", "interface" : "memory", "bitwidth" : 32, "direction" : "WRITEONLY", "extern" : 0} ]}
# RTL Port declarations: 
set portNum 31
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ a_0_val sc_in sc_lv 32 signal 0 } 
	{ a_1_val sc_in sc_lv 32 signal 1 } 
	{ a_2_val sc_in sc_lv 32 signal 2 } 
	{ a_3_val sc_in sc_lv 32 signal 3 } 
	{ a_4_val sc_in sc_lv 32 signal 4 } 
	{ a_5_val sc_in sc_lv 32 signal 5 } 
	{ a_6_val sc_in sc_lv 32 signal 6 } 
	{ a_7_val sc_in sc_lv 32 signal 7 } 
	{ base_addr sc_in sc_lv 9 signal 8 } 
	{ b_0_val sc_in sc_lv 32 signal 9 } 
	{ b_1_val sc_in sc_lv 32 signal 10 } 
	{ b_2_val sc_in sc_lv 32 signal 11 } 
	{ b_3_val sc_in sc_lv 32 signal 12 } 
	{ b_4_val sc_in sc_lv 32 signal 13 } 
	{ b_5_val sc_in sc_lv 32 signal 14 } 
	{ b_6_val sc_in sc_lv 32 signal 15 } 
	{ b_7_val sc_in sc_lv 32 signal 16 } 
	{ aamf_bank_a_address1 sc_out sc_lv 9 signal 17 } 
	{ aamf_bank_a_ce1 sc_out sc_logic 1 signal 17 } 
	{ aamf_bank_a_we1 sc_out sc_logic 1 signal 17 } 
	{ aamf_bank_a_d1 sc_out sc_lv 32 signal 17 } 
	{ aamf_bank_b_address1 sc_out sc_lv 9 signal 18 } 
	{ aamf_bank_b_ce1 sc_out sc_logic 1 signal 18 } 
	{ aamf_bank_b_we1 sc_out sc_logic 1 signal 18 } 
	{ aamf_bank_b_d1 sc_out sc_lv 32 signal 18 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "a_0_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_0_val", "role": "default" }} , 
 	{ "name": "a_1_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_1_val", "role": "default" }} , 
 	{ "name": "a_2_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_2_val", "role": "default" }} , 
 	{ "name": "a_3_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_3_val", "role": "default" }} , 
 	{ "name": "a_4_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_4_val", "role": "default" }} , 
 	{ "name": "a_5_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_5_val", "role": "default" }} , 
 	{ "name": "a_6_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_6_val", "role": "default" }} , 
 	{ "name": "a_7_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_7_val", "role": "default" }} , 
 	{ "name": "base_addr", "direction": "in", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "base_addr", "role": "default" }} , 
 	{ "name": "b_0_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_0_val", "role": "default" }} , 
 	{ "name": "b_1_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_1_val", "role": "default" }} , 
 	{ "name": "b_2_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_2_val", "role": "default" }} , 
 	{ "name": "b_3_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_3_val", "role": "default" }} , 
 	{ "name": "b_4_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_4_val", "role": "default" }} , 
 	{ "name": "b_5_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_5_val", "role": "default" }} , 
 	{ "name": "b_6_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_6_val", "role": "default" }} , 
 	{ "name": "b_7_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_7_val", "role": "default" }} , 
 	{ "name": "aamf_bank_a_address1", "direction": "out", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "aamf_bank_a", "role": "address1" }} , 
 	{ "name": "aamf_bank_a_ce1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_bank_a", "role": "ce1" }} , 
 	{ "name": "aamf_bank_a_we1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_bank_a", "role": "we1" }} , 
 	{ "name": "aamf_bank_a_d1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "aamf_bank_a", "role": "d1" }} , 
 	{ "name": "aamf_bank_b_address1", "direction": "out", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "aamf_bank_b", "role": "address1" }} , 
 	{ "name": "aamf_bank_b_ce1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_bank_b", "role": "ce1" }} , 
 	{ "name": "aamf_bank_b_we1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_bank_b", "role": "we1" }} , 
 	{ "name": "aamf_bank_b_d1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "aamf_bank_b", "role": "d1" }}  ]}

set ArgLastReadFirstWriteLatency {
	qgpu_ga_engine_parallel_Pipeline_AAMF_STAGE_IN {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}
		base_addr {Type I LastRead 0 FirstWrite -1}
		b_0_val {Type I LastRead 0 FirstWrite -1}
		b_1_val {Type I LastRead 0 FirstWrite -1}
		b_2_val {Type I LastRead 0 FirstWrite -1}
		b_3_val {Type I LastRead 0 FirstWrite -1}
		b_4_val {Type I LastRead 0 FirstWrite -1}
		b_5_val {Type I LastRead 0 FirstWrite -1}
		b_6_val {Type I LastRead 0 FirstWrite -1}
		b_7_val {Type I LastRead 0 FirstWrite -1}
		aamf_bank_a {Type O LastRead -1 FirstWrite 0}
		aamf_bank_b {Type O LastRead -1 FirstWrite 0}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "10", "Max" : "10"}
	, {"Name" : "Interval", "Min" : "9", "Max" : "9"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	a_0_val { ap_none {  { a_0_val in_data 0 32 } } }
	a_1_val { ap_none {  { a_1_val in_data 0 32 } } }
	a_2_val { ap_none {  { a_2_val in_data 0 32 } } }
	a_3_val { ap_none {  { a_3_val in_data 0 32 } } }
	a_4_val { ap_none {  { a_4_val in_data 0 32 } } }
	a_5_val { ap_none {  { a_5_val in_data 0 32 } } }
	a_6_val { ap_none {  { a_6_val in_data 0 32 } } }
	a_7_val { ap_none {  { a_7_val in_data 0 32 } } }
	base_addr { ap_none {  { base_addr in_data 0 9 } } }
	b_0_val { ap_none {  { b_0_val in_data 0 32 } } }
	b_1_val { ap_none {  { b_1_val in_data 0 32 } } }
	b_2_val { ap_none {  { b_2_val in_data 0 32 } } }
	b_3_val { ap_none {  { b_3_val in_data 0 32 } } }
	b_4_val { ap_none {  { b_4_val in_data 0 32 } } }
	b_5_val { ap_none {  { b_5_val in_data 0 32 } } }
	b_6_val { ap_none {  { b_6_val in_data 0 32 } } }
	b_7_val { ap_none {  { b_7_val in_data 0 32 } } }
	aamf_bank_a { ap_memory {  { aamf_bank_a_address1 MemPortADDR2 1 9 }  { aamf_bank_a_ce1 MemPortCE2 1 1 }  { aamf_bank_a_we1 MemPortWE2 1 1 }  { aamf_bank_a_d1 MemPortDIN2 1 32 } } }
	aamf_bank_b { ap_memory {  { aamf_bank_b_address1 MemPortADDR2 1 9 }  { aamf_bank_b_ce1 MemPortCE2 1 1 }  { aamf_bank_b_we1 MemPortWE2 1 1 }  { aamf_bank_b_d1 MemPortDIN2 1 32 } } }
}
