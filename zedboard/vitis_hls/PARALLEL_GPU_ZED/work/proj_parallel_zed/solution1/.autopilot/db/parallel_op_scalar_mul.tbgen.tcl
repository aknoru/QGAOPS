set moduleName parallel_op_scalar_mul
set isTopModule 0
set isCombinational 0
set isDatapathOnly 1
set isPipelined 1
set isPipelined_legacy 1
set pipeline_type function
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
set cdfgNum 16
set C_modelName {parallel_op_scalar_mul}
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
	{ scalar_val int 32 regular  }
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
 	{ "Name" : "scalar_val", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "ap_return", "interface" : "wire", "bitwidth" : 257} ]}
# RTL Port declarations: 
set portNum 52
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ a_0_val sc_in sc_lv 32 signal 0 } 
	{ a_1_val sc_in sc_lv 32 signal 1 } 
	{ a_2_val sc_in sc_lv 32 signal 2 } 
	{ a_3_val sc_in sc_lv 32 signal 3 } 
	{ a_4_val sc_in sc_lv 32 signal 4 } 
	{ a_5_val sc_in sc_lv 32 signal 5 } 
	{ a_6_val sc_in sc_lv 32 signal 6 } 
	{ a_7_val sc_in sc_lv 32 signal 7 } 
	{ scalar_val sc_in sc_lv 32 signal 8 } 
	{ ap_return_0 sc_out sc_lv 32 signal -1 } 
	{ ap_return_1 sc_out sc_lv 32 signal -1 } 
	{ ap_return_2 sc_out sc_lv 32 signal -1 } 
	{ ap_return_3 sc_out sc_lv 32 signal -1 } 
	{ ap_return_4 sc_out sc_lv 32 signal -1 } 
	{ ap_return_5 sc_out sc_lv 32 signal -1 } 
	{ ap_return_6 sc_out sc_lv 32 signal -1 } 
	{ ap_return_7 sc_out sc_lv 32 signal -1 } 
	{ ap_return_8 sc_out sc_lv 1 signal -1 } 
	{ grp_fu_1360_p_din0 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1360_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1360_p_dout0 sc_in sc_lv 64 signal -1 } 
	{ grp_fu_1360_p_ce sc_out sc_logic 1 signal -1 } 
	{ grp_fu_1364_p_din0 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1364_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1364_p_dout0 sc_in sc_lv 64 signal -1 } 
	{ grp_fu_1364_p_ce sc_out sc_logic 1 signal -1 } 
	{ grp_fu_1368_p_din0 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1368_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1368_p_dout0 sc_in sc_lv 64 signal -1 } 
	{ grp_fu_1368_p_ce sc_out sc_logic 1 signal -1 } 
	{ grp_fu_1372_p_din0 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1372_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1372_p_dout0 sc_in sc_lv 64 signal -1 } 
	{ grp_fu_1372_p_ce sc_out sc_logic 1 signal -1 } 
	{ grp_fu_1376_p_din0 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1376_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1376_p_dout0 sc_in sc_lv 64 signal -1 } 
	{ grp_fu_1376_p_ce sc_out sc_logic 1 signal -1 } 
	{ grp_fu_1380_p_din0 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1380_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1380_p_dout0 sc_in sc_lv 64 signal -1 } 
	{ grp_fu_1380_p_ce sc_out sc_logic 1 signal -1 } 
	{ grp_fu_1384_p_din0 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1384_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1384_p_dout0 sc_in sc_lv 64 signal -1 } 
	{ grp_fu_1384_p_ce sc_out sc_logic 1 signal -1 } 
	{ grp_fu_1388_p_din0 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1388_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_fu_1388_p_dout0 sc_in sc_lv 64 signal -1 } 
	{ grp_fu_1388_p_ce sc_out sc_logic 1 signal -1 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "a_0_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_0_val", "role": "default" }} , 
 	{ "name": "a_1_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_1_val", "role": "default" }} , 
 	{ "name": "a_2_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_2_val", "role": "default" }} , 
 	{ "name": "a_3_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_3_val", "role": "default" }} , 
 	{ "name": "a_4_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_4_val", "role": "default" }} , 
 	{ "name": "a_5_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_5_val", "role": "default" }} , 
 	{ "name": "a_6_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_6_val", "role": "default" }} , 
 	{ "name": "a_7_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_7_val", "role": "default" }} , 
 	{ "name": "scalar_val", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "scalar_val", "role": "default" }} , 
 	{ "name": "ap_return_0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_0", "role": "default" }} , 
 	{ "name": "ap_return_1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_1", "role": "default" }} , 
 	{ "name": "ap_return_2", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_2", "role": "default" }} , 
 	{ "name": "ap_return_3", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_3", "role": "default" }} , 
 	{ "name": "ap_return_4", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_4", "role": "default" }} , 
 	{ "name": "ap_return_5", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_5", "role": "default" }} , 
 	{ "name": "ap_return_6", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_6", "role": "default" }} , 
 	{ "name": "ap_return_7", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_7", "role": "default" }} , 
 	{ "name": "ap_return_8", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "ap_return_8", "role": "default" }} , 
 	{ "name": "grp_fu_1360_p_din0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1360_p_din0", "role": "default" }} , 
 	{ "name": "grp_fu_1360_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1360_p_din1", "role": "default" }} , 
 	{ "name": "grp_fu_1360_p_dout0", "direction": "in", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "grp_fu_1360_p_dout0", "role": "default" }} , 
 	{ "name": "grp_fu_1360_p_ce", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_fu_1360_p_ce", "role": "default" }} , 
 	{ "name": "grp_fu_1364_p_din0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1364_p_din0", "role": "default" }} , 
 	{ "name": "grp_fu_1364_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1364_p_din1", "role": "default" }} , 
 	{ "name": "grp_fu_1364_p_dout0", "direction": "in", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "grp_fu_1364_p_dout0", "role": "default" }} , 
 	{ "name": "grp_fu_1364_p_ce", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_fu_1364_p_ce", "role": "default" }} , 
 	{ "name": "grp_fu_1368_p_din0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1368_p_din0", "role": "default" }} , 
 	{ "name": "grp_fu_1368_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1368_p_din1", "role": "default" }} , 
 	{ "name": "grp_fu_1368_p_dout0", "direction": "in", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "grp_fu_1368_p_dout0", "role": "default" }} , 
 	{ "name": "grp_fu_1368_p_ce", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_fu_1368_p_ce", "role": "default" }} , 
 	{ "name": "grp_fu_1372_p_din0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1372_p_din0", "role": "default" }} , 
 	{ "name": "grp_fu_1372_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1372_p_din1", "role": "default" }} , 
 	{ "name": "grp_fu_1372_p_dout0", "direction": "in", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "grp_fu_1372_p_dout0", "role": "default" }} , 
 	{ "name": "grp_fu_1372_p_ce", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_fu_1372_p_ce", "role": "default" }} , 
 	{ "name": "grp_fu_1376_p_din0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1376_p_din0", "role": "default" }} , 
 	{ "name": "grp_fu_1376_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1376_p_din1", "role": "default" }} , 
 	{ "name": "grp_fu_1376_p_dout0", "direction": "in", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "grp_fu_1376_p_dout0", "role": "default" }} , 
 	{ "name": "grp_fu_1376_p_ce", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_fu_1376_p_ce", "role": "default" }} , 
 	{ "name": "grp_fu_1380_p_din0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1380_p_din0", "role": "default" }} , 
 	{ "name": "grp_fu_1380_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1380_p_din1", "role": "default" }} , 
 	{ "name": "grp_fu_1380_p_dout0", "direction": "in", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "grp_fu_1380_p_dout0", "role": "default" }} , 
 	{ "name": "grp_fu_1380_p_ce", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_fu_1380_p_ce", "role": "default" }} , 
 	{ "name": "grp_fu_1384_p_din0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1384_p_din0", "role": "default" }} , 
 	{ "name": "grp_fu_1384_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1384_p_din1", "role": "default" }} , 
 	{ "name": "grp_fu_1384_p_dout0", "direction": "in", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "grp_fu_1384_p_dout0", "role": "default" }} , 
 	{ "name": "grp_fu_1384_p_ce", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_fu_1384_p_ce", "role": "default" }} , 
 	{ "name": "grp_fu_1388_p_din0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1388_p_din0", "role": "default" }} , 
 	{ "name": "grp_fu_1388_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_fu_1388_p_din1", "role": "default" }} , 
 	{ "name": "grp_fu_1388_p_dout0", "direction": "in", "datatype": "sc_lv", "bitwidth":64, "type": "signal", "bundle":{"name": "grp_fu_1388_p_dout0", "role": "default" }} , 
 	{ "name": "grp_fu_1388_p_ce", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_fu_1388_p_ce", "role": "default" }}  ]}

set ArgLastReadFirstWriteLatency {
	parallel_op_scalar_mul {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}
		scalar_val {Type I LastRead 0 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "3", "Max" : "3"}
	, {"Name" : "Interval", "Min" : "1", "Max" : "1"}
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
	scalar_val { ap_none {  { scalar_val in_data 0 32 } } }
}
