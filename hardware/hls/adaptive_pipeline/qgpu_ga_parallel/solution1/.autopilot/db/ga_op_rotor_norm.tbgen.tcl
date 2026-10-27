set moduleName ga_op_rotor_norm
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
set C_modelName {ga_op_rotor_norm}
set C_modelType { int 33 }
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
 	{ "Name" : "ap_return", "interface" : "wire", "bitwidth" : 33} ]}
# RTL Port declarations: 
set portNum 20
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
	{ ap_return_0 sc_out sc_lv 32 signal -1 } 
	{ ap_return_1 sc_out sc_lv 1 signal -1 } 
	{ grp_fu_2387_p_din0 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_2387_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_2387_p_dout0 sc_in sc_lv 64 signal -1 } 
	{ grp_fu_2387_p_ce sc_out sc_logic 1 signal -1 } 
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
 	{ "name": "ap_return_0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_0", "role": "default" }} , 
 	{ "name": "ap_return_1", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "ap_return_1", "role": "default" }} , 
 	{ "name": "grp_fu_2387_p_din0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_2387_p_din0", "role": "default" }} , 
 	{ "name": "grp_fu_2387_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_2387_p_din1", "role": "default" }} , 
 	{ "name": "grp_fu_2387_p_dout0", "direction": "in", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "grp_fu_2387_p_dout0", "role": "default" }} , 
 	{ "name": "grp_fu_2387_p_ce", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_fu_2387_p_ce", "role": "default" }}  ]}

set ArgLastReadFirstWriteLatency {
	ga_op_rotor_norm {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "4", "Max" : "4"}
	, {"Name" : "Interval", "Min" : "4", "Max" : "4"}
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
}
