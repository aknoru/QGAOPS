set moduleName seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP
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
set cdfgNum 18
set C_modelName {seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP}
set C_modelType { void 0 }
set ap_memory_interface_dict [dict create]
dict set ap_memory_interface_dict a { MEM_WIDTH 32 MEM_SIZE 32 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 1 }
dict set ap_memory_interface_dict b { MEM_WIDTH 32 MEM_SIZE 32 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 1 }
set C_modelArgList {
	{ a int 32 regular {array 8 { 1 } 1 1 }  }
	{ b int 32 regular {array 8 { 1 } 1 1 }  }
	{ opcode int 2 regular  }
	{ accum_load_out int 67 regular {pointer 1}  }
	{ accum_1_load_out int 67 regular {pointer 1}  }
	{ accum_2_load_out int 67 regular {pointer 1}  }
	{ accum_3_load_out int 67 regular {pointer 1}  }
	{ accum_4_load_out int 67 regular {pointer 1}  }
	{ accum_5_load_out int 67 regular {pointer 1}  }
	{ accum_6_load_out int 67 regular {pointer 1}  }
	{ accum_7_load_out int 67 regular {pointer 1}  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "a", "interface" : "memory", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b", "interface" : "memory", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "opcode", "interface" : "wire", "bitwidth" : 2, "direction" : "READONLY"} , 
 	{ "Name" : "accum_load_out", "interface" : "wire", "bitwidth" : 67, "direction" : "WRITEONLY"} , 
 	{ "Name" : "accum_1_load_out", "interface" : "wire", "bitwidth" : 67, "direction" : "WRITEONLY"} , 
 	{ "Name" : "accum_2_load_out", "interface" : "wire", "bitwidth" : 67, "direction" : "WRITEONLY"} , 
 	{ "Name" : "accum_3_load_out", "interface" : "wire", "bitwidth" : 67, "direction" : "WRITEONLY"} , 
 	{ "Name" : "accum_4_load_out", "interface" : "wire", "bitwidth" : 67, "direction" : "WRITEONLY"} , 
 	{ "Name" : "accum_5_load_out", "interface" : "wire", "bitwidth" : 67, "direction" : "WRITEONLY"} , 
 	{ "Name" : "accum_6_load_out", "interface" : "wire", "bitwidth" : 67, "direction" : "WRITEONLY"} , 
 	{ "Name" : "accum_7_load_out", "interface" : "wire", "bitwidth" : 67, "direction" : "WRITEONLY"} ]}
# RTL Port declarations: 
set portNum 29
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
	{ b_address0 sc_out sc_lv 3 signal 1 } 
	{ b_ce0 sc_out sc_logic 1 signal 1 } 
	{ b_q0 sc_in sc_lv 32 signal 1 } 
	{ opcode sc_in sc_lv 2 signal 2 } 
	{ accum_load_out sc_out sc_lv 67 signal 3 } 
	{ accum_load_out_ap_vld sc_out sc_logic 1 outvld 3 } 
	{ accum_1_load_out sc_out sc_lv 67 signal 4 } 
	{ accum_1_load_out_ap_vld sc_out sc_logic 1 outvld 4 } 
	{ accum_2_load_out sc_out sc_lv 67 signal 5 } 
	{ accum_2_load_out_ap_vld sc_out sc_logic 1 outvld 5 } 
	{ accum_3_load_out sc_out sc_lv 67 signal 6 } 
	{ accum_3_load_out_ap_vld sc_out sc_logic 1 outvld 6 } 
	{ accum_4_load_out sc_out sc_lv 67 signal 7 } 
	{ accum_4_load_out_ap_vld sc_out sc_logic 1 outvld 7 } 
	{ accum_5_load_out sc_out sc_lv 67 signal 8 } 
	{ accum_5_load_out_ap_vld sc_out sc_logic 1 outvld 8 } 
	{ accum_6_load_out sc_out sc_lv 67 signal 9 } 
	{ accum_6_load_out_ap_vld sc_out sc_logic 1 outvld 9 } 
	{ accum_7_load_out sc_out sc_lv 67 signal 10 } 
	{ accum_7_load_out_ap_vld sc_out sc_logic 1 outvld 10 } 
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
 	{ "name": "b_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":3, "type": "signal", "bundle":{"name": "b", "role": "address0" }} , 
 	{ "name": "b_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "b", "role": "ce0" }} , 
 	{ "name": "b_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b", "role": "q0" }} , 
 	{ "name": "opcode", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "opcode", "role": "default" }} , 
 	{ "name": "accum_load_out", "direction": "out", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_load_out", "role": "default" }} , 
 	{ "name": "accum_load_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "accum_load_out", "role": "ap_vld" }} , 
 	{ "name": "accum_1_load_out", "direction": "out", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_1_load_out", "role": "default" }} , 
 	{ "name": "accum_1_load_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "accum_1_load_out", "role": "ap_vld" }} , 
 	{ "name": "accum_2_load_out", "direction": "out", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_2_load_out", "role": "default" }} , 
 	{ "name": "accum_2_load_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "accum_2_load_out", "role": "ap_vld" }} , 
 	{ "name": "accum_3_load_out", "direction": "out", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_3_load_out", "role": "default" }} , 
 	{ "name": "accum_3_load_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "accum_3_load_out", "role": "ap_vld" }} , 
 	{ "name": "accum_4_load_out", "direction": "out", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_4_load_out", "role": "default" }} , 
 	{ "name": "accum_4_load_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "accum_4_load_out", "role": "ap_vld" }} , 
 	{ "name": "accum_5_load_out", "direction": "out", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_5_load_out", "role": "default" }} , 
 	{ "name": "accum_5_load_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "accum_5_load_out", "role": "ap_vld" }} , 
 	{ "name": "accum_6_load_out", "direction": "out", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_6_load_out", "role": "default" }} , 
 	{ "name": "accum_6_load_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "accum_6_load_out", "role": "ap_vld" }} , 
 	{ "name": "accum_7_load_out", "direction": "out", "datatype": "sc_lv", "bitwidth":67, "type": "signal", "bundle":{"name": "accum_7_load_out", "role": "default" }} , 
 	{ "name": "accum_7_load_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "accum_7_load_out", "role": "ap_vld" }}  ]}

set ArgLastReadFirstWriteLatency {
	seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP {
		a {Type I LastRead 2 FirstWrite -1}
		b {Type I LastRead 2 FirstWrite -1}
		opcode {Type I LastRead 0 FirstWrite -1}
		accum_load_out {Type O LastRead -1 FirstWrite 4}
		accum_1_load_out {Type O LastRead -1 FirstWrite 4}
		accum_2_load_out {Type O LastRead -1 FirstWrite 4}
		accum_3_load_out {Type O LastRead -1 FirstWrite 4}
		accum_4_load_out {Type O LastRead -1 FirstWrite 4}
		accum_5_load_out {Type O LastRead -1 FirstWrite 4}
		accum_6_load_out {Type O LastRead -1 FirstWrite 4}
		accum_7_load_out {Type O LastRead -1 FirstWrite 4}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "70", "Max" : "70"}
	, {"Name" : "Interval", "Min" : "65", "Max" : "65"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
]}

set Spec2ImplPortList { 
	a { ap_memory {  { a_address0 mem_address 1 3 }  { a_ce0 mem_ce 1 1 }  { a_q0 mem_dout 0 32 } } }
	b { ap_memory {  { b_address0 mem_address 1 3 }  { b_ce0 mem_ce 1 1 }  { b_q0 mem_dout 0 32 } } }
	opcode { ap_none {  { opcode in_data 0 2 } } }
	accum_load_out { ap_vld {  { accum_load_out out_data 1 67 }  { accum_load_out_ap_vld out_vld 1 1 } } }
	accum_1_load_out { ap_vld {  { accum_1_load_out out_data 1 67 }  { accum_1_load_out_ap_vld out_vld 1 1 } } }
	accum_2_load_out { ap_vld {  { accum_2_load_out out_data 1 67 }  { accum_2_load_out_ap_vld out_vld 1 1 } } }
	accum_3_load_out { ap_vld {  { accum_3_load_out out_data 1 67 }  { accum_3_load_out_ap_vld out_vld 1 1 } } }
	accum_4_load_out { ap_vld {  { accum_4_load_out out_data 1 67 }  { accum_4_load_out_ap_vld out_vld 1 1 } } }
	accum_5_load_out { ap_vld {  { accum_5_load_out out_data 1 67 }  { accum_5_load_out_ap_vld out_vld 1 1 } } }
	accum_6_load_out { ap_vld {  { accum_6_load_out out_data 1 67 }  { accum_6_load_out_ap_vld out_vld 1 1 } } }
	accum_7_load_out { ap_vld {  { accum_7_load_out out_data 1 67 }  { accum_7_load_out_ap_vld out_vld 1 1 } } }
}
