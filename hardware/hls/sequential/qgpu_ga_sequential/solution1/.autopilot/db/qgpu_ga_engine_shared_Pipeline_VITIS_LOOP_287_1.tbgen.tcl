set moduleName qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_287_1
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
set C_modelName {qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_287_1}
set C_modelType { void 0 }
set ap_memory_interface_dict [dict create]
dict set ap_memory_interface_dict a { MEM_WIDTH 32 MEM_SIZE 32 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 1 }
dict set ap_memory_interface_dict b { MEM_WIDTH 32 MEM_SIZE 32 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 1 }
dict set ap_memory_interface_dict aamf_seq_bank_a { MEM_WIDTH 32 MEM_SIZE 2048 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 0 }
dict set ap_memory_interface_dict aamf_seq_bank_b { MEM_WIDTH 32 MEM_SIZE 2048 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 0 }
set C_modelArgList {
	{ a int 32 regular {array 8 { 1 } 1 1 }  }
	{ base_addr int 9 regular  }
	{ b int 32 regular {array 8 { 1 } 1 1 }  }
	{ aamf_seq_bank_a int 32 regular {array 512 { 3 0 } 0 1 } {global 1}  }
	{ aamf_seq_bank_b int 32 regular {array 512 { 3 0 } 0 1 } {global 1}  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "a", "interface" : "memory", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "base_addr", "interface" : "wire", "bitwidth" : 9, "direction" : "READONLY"} , 
 	{ "Name" : "b", "interface" : "memory", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "aamf_seq_bank_a", "interface" : "memory", "bitwidth" : 32, "direction" : "WRITEONLY", "extern" : 0} , 
 	{ "Name" : "aamf_seq_bank_b", "interface" : "memory", "bitwidth" : 32, "direction" : "WRITEONLY", "extern" : 0} ]}
# RTL Port declarations: 
set portNum 21
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ a_address0 sc_out sc_lv 3 signal 0 } 
	{ a_ce0 sc_out sc_logic 1 signal 0 } 
	{ a_q0 sc_in sc_lv 32 signal 0 } 
	{ base_addr sc_in sc_lv 9 signal 1 } 
	{ b_address0 sc_out sc_lv 3 signal 2 } 
	{ b_ce0 sc_out sc_logic 1 signal 2 } 
	{ b_q0 sc_in sc_lv 32 signal 2 } 
	{ aamf_seq_bank_a_address1 sc_out sc_lv 9 signal 3 } 
	{ aamf_seq_bank_a_ce1 sc_out sc_logic 1 signal 3 } 
	{ aamf_seq_bank_a_we1 sc_out sc_logic 1 signal 3 } 
	{ aamf_seq_bank_a_d1 sc_out sc_lv 32 signal 3 } 
	{ aamf_seq_bank_b_address1 sc_out sc_lv 9 signal 4 } 
	{ aamf_seq_bank_b_ce1 sc_out sc_logic 1 signal 4 } 
	{ aamf_seq_bank_b_we1 sc_out sc_logic 1 signal 4 } 
	{ aamf_seq_bank_b_d1 sc_out sc_lv 32 signal 4 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "a_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "a", "role": "address0" }} , 
 	{ "name": "a_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "a", "role": "ce0" }} , 
 	{ "name": "a_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a", "role": "q0" }} , 
 	{ "name": "base_addr", "direction": "in", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "base_addr", "role": "default" }} , 
 	{ "name": "b_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "b", "role": "address0" }} , 
 	{ "name": "b_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "b", "role": "ce0" }} , 
 	{ "name": "b_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b", "role": "q0" }} , 
 	{ "name": "aamf_seq_bank_a_address1", "direction": "out", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "aamf_seq_bank_a", "role": "address1" }} , 
 	{ "name": "aamf_seq_bank_a_ce1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_seq_bank_a", "role": "ce1" }} , 
 	{ "name": "aamf_seq_bank_a_we1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_seq_bank_a", "role": "we1" }} , 
 	{ "name": "aamf_seq_bank_a_d1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "aamf_seq_bank_a", "role": "d1" }} , 
 	{ "name": "aamf_seq_bank_b_address1", "direction": "out", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "aamf_seq_bank_b", "role": "address1" }} , 
 	{ "name": "aamf_seq_bank_b_ce1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_seq_bank_b", "role": "ce1" }} , 
 	{ "name": "aamf_seq_bank_b_we1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_seq_bank_b", "role": "we1" }} , 
 	{ "name": "aamf_seq_bank_b_d1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "aamf_seq_bank_b", "role": "d1" }}  ]}

set ArgLastReadFirstWriteLatency {
	qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_287_1 {
		a {Type I LastRead 0 FirstWrite -1}
		base_addr {Type I LastRead 0 FirstWrite -1}
		b {Type I LastRead 0 FirstWrite -1}
		aamf_seq_bank_a {Type O LastRead -1 FirstWrite 1}
		aamf_seq_bank_b {Type O LastRead -1 FirstWrite 1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "10", "Max" : "10"}
	, {"Name" : "Interval", "Min" : "9", "Max" : "9"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
]}

set Spec2ImplPortList { 
	a { ap_memory {  { a_address0 mem_address 1 3 }  { a_ce0 mem_ce 1 1 }  { a_q0 mem_dout 0 32 } } }
	base_addr { ap_none {  { base_addr in_data 0 9 } } }
	b { ap_memory {  { b_address0 mem_address 1 3 }  { b_ce0 mem_ce 1 1 }  { b_q0 mem_dout 0 32 } } }
	aamf_seq_bank_a { ap_memory {  { aamf_seq_bank_a_address1 MemPortADDR2 1 9 }  { aamf_seq_bank_a_ce1 MemPortCE2 1 1 }  { aamf_seq_bank_a_we1 MemPortWE2 1 1 }  { aamf_seq_bank_a_d1 MemPortDIN2 1 32 } } }
	aamf_seq_bank_b { ap_memory {  { aamf_seq_bank_b_address1 MemPortADDR2 1 9 }  { aamf_seq_bank_b_ce1 MemPortCE2 1 1 }  { aamf_seq_bank_b_we1 MemPortWE2 1 1 }  { aamf_seq_bank_b_d1 MemPortDIN2 1 32 } } }
}
