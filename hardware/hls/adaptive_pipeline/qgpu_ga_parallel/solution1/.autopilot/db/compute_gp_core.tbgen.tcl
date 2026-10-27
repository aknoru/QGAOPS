set moduleName compute_gp_core
set isTopModule 0
set isCombinational 0
set isDatapathOnly 0
set isPipelined 0
set isPipelined_legacy 0
set pipeline_type none
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
set C_modelName {compute_gp_core}
set C_modelType { int 257 }
set ap_memory_interface_dict [dict create]
set C_modelArgList {
	{ a_0_val int 32 regular  }
	{ a_1_val int 32 regular  }
	{ a_2_val int 32 regular  }
	{ a_3_val int 32 regular  }
	{ a_4_val int 32 regular  }
	{ a_5_val int 32 regular  }
	{ a_6_val int 32 regular  }
	{ a_7_val int 32 regular  }
	{ b_0_val int 32 regular  }
	{ b_1_val int 32 regular  }
	{ b_2_val int 32 regular  }
	{ b_3_val int 32 regular  }
	{ b_4_val int 32 regular  }
	{ b_5_val int 32 regular  }
	{ b_6_val int 32 regular  }
	{ b_7_val int 32 regular  }
	{ opcode int 2 regular  }
	{ overflow_read int 1 regular  }
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
 	{ "Name" : "b_0_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_1_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_2_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_3_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_4_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_5_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_6_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_7_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "opcode", "interface" : "wire", "bitwidth" : 2, "direction" : "READONLY"} , 
 	{ "Name" : "overflow_read", "interface" : "wire", "bitwidth" : 1, "direction" : "READONLY"} , 
 	{ "Name" : "ap_return", "interface" : "wire", "bitwidth" : 257} ]}
# RTL Port declarations: 
set portNum 33
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
	{ b_0_val sc_in sc_lv 32 signal 8 } 
	{ b_1_val sc_in sc_lv 32 signal 9 } 
	{ b_2_val sc_in sc_lv 32 signal 10 } 
	{ b_3_val sc_in sc_lv 32 signal 11 } 
	{ b_4_val sc_in sc_lv 32 signal 12 } 
	{ b_5_val sc_in sc_lv 32 signal 13 } 
	{ b_6_val sc_in sc_lv 32 signal 14 } 
	{ b_7_val sc_in sc_lv 32 signal 15 } 
	{ opcode sc_in sc_lv 2 signal 16 } 
	{ overflow_read sc_in sc_lv 1 signal 17 } 
	{ ap_return_0 sc_out sc_lv 32 signal -1 } 
	{ ap_return_1 sc_out sc_lv 32 signal -1 } 
	{ ap_return_2 sc_out sc_lv 32 signal -1 } 
	{ ap_return_3 sc_out sc_lv 32 signal -1 } 
	{ ap_return_4 sc_out sc_lv 32 signal -1 } 
	{ ap_return_5 sc_out sc_lv 32 signal -1 } 
	{ ap_return_6 sc_out sc_lv 32 signal -1 } 
	{ ap_return_7 sc_out sc_lv 32 signal -1 } 
	{ ap_return_8 sc_out sc_lv 1 signal -1 } 
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
 	{ "name": "b_0_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_0_val", "role": "default" }} , 
 	{ "name": "b_1_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_1_val", "role": "default" }} , 
 	{ "name": "b_2_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_2_val", "role": "default" }} , 
 	{ "name": "b_3_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_3_val", "role": "default" }} , 
 	{ "name": "b_4_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_4_val", "role": "default" }} , 
 	{ "name": "b_5_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_5_val", "role": "default" }} , 
 	{ "name": "b_6_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_6_val", "role": "default" }} , 
 	{ "name": "b_7_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_7_val", "role": "default" }} , 
 	{ "name": "opcode", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "opcode", "role": "default" }} , 
 	{ "name": "overflow_read", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "overflow_read", "role": "default" }} , 
 	{ "name": "ap_return_0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_0", "role": "default" }} , 
 	{ "name": "ap_return_1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_1", "role": "default" }} , 
 	{ "name": "ap_return_2", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_2", "role": "default" }} , 
 	{ "name": "ap_return_3", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_3", "role": "default" }} , 
 	{ "name": "ap_return_4", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_4", "role": "default" }} , 
 	{ "name": "ap_return_5", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_5", "role": "default" }} , 
 	{ "name": "ap_return_6", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_6", "role": "default" }} , 
 	{ "name": "ap_return_7", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_7", "role": "default" }} , 
 	{ "name": "ap_return_8", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "ap_return_8", "role": "default" }}  ]}

set ArgLastReadFirstWriteLatency {
	compute_gp_core {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}
		b_0_val {Type I LastRead 0 FirstWrite -1}
		b_1_val {Type I LastRead 0 FirstWrite -1}
		b_2_val {Type I LastRead 0 FirstWrite -1}
		b_3_val {Type I LastRead 0 FirstWrite -1}
		b_4_val {Type I LastRead 0 FirstWrite -1}
		b_5_val {Type I LastRead 0 FirstWrite -1}
		b_6_val {Type I LastRead 0 FirstWrite -1}
		b_7_val {Type I LastRead 0 FirstWrite -1}
		opcode {Type I LastRead 0 FirstWrite -1}
		overflow_read {Type I LastRead 0 FirstWrite -1}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
	blade_product_sign {
		left_mask {Type I LastRead 0 FirstWrite -1}
		right_mask {Type I LastRead 0 FirstWrite -1}}
	blade_product_sign {
		left_mask {Type I LastRead 0 FirstWrite -1}
		right_mask {Type I LastRead 0 FirstWrite -1}}
	blade_product_sign {
		left_mask {Type I LastRead 0 FirstWrite -1}
		right_mask {Type I LastRead 0 FirstWrite -1}}
	blade_product_sign {
		left_mask {Type I LastRead 0 FirstWrite -1}
		right_mask {Type I LastRead 0 FirstWrite -1}}
	blade_product_sign {
		left_mask {Type I LastRead 0 FirstWrite -1}
		right_mask {Type I LastRead 0 FirstWrite -1}}
	blade_product_sign {
		left_mask {Type I LastRead 0 FirstWrite -1}
		right_mask {Type I LastRead 0 FirstWrite -1}}
	blade_product_sign {
		left_mask {Type I LastRead 0 FirstWrite -1}
		right_mask {Type I LastRead 0 FirstWrite -1}}
	blade_product_sign {
		left_mask {Type I LastRead 0 FirstWrite -1}
		right_mask {Type I LastRead 0 FirstWrite -1}}
	rescale_and_saturate {
		sum_val {Type I LastRead 0 FirstWrite -1}
		overflow_flag_read {Type I LastRead 1 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "50", "Max" : "50"}
	, {"Name" : "Interval", "Min" : "50", "Max" : "50"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
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
	b_0_val { ap_none {  { b_0_val in_data 0 32 } } }
	b_1_val { ap_none {  { b_1_val in_data 0 32 } } }
	b_2_val { ap_none {  { b_2_val in_data 0 32 } } }
	b_3_val { ap_none {  { b_3_val in_data 0 32 } } }
	b_4_val { ap_none {  { b_4_val in_data 0 32 } } }
	b_5_val { ap_none {  { b_5_val in_data 0 32 } } }
	b_6_val { ap_none {  { b_6_val in_data 0 32 } } }
	b_7_val { ap_none {  { b_7_val in_data 0 32 } } }
	opcode { ap_none {  { opcode in_data 0 2 } } }
	overflow_read { ap_none {  { overflow_read in_data 0 1 } } }
}
