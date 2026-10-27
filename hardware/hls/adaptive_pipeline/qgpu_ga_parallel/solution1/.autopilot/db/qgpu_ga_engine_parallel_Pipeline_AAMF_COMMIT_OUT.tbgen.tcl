set moduleName qgpu_ga_engine_parallel_Pipeline_AAMF_COMMIT_OUT
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
set C_modelName {qgpu_ga_engine_parallel_Pipeline_AAMF_COMMIT_OUT}
set C_modelType { void 0 }
set ap_memory_interface_dict [dict create]
set C_modelArgList {
	{ c_0 int 32 regular {pointer 1}  }
	{ c_7 int 32 regular {pointer 1}  }
	{ c_6 int 32 regular {pointer 1}  }
	{ c_5 int 32 regular {pointer 1}  }
	{ c_4 int 32 regular {pointer 1}  }
	{ c_3 int 32 regular {pointer 1}  }
	{ c_2 int 32 regular {pointer 1}  }
	{ c_1 int 32 regular {pointer 1}  }
	{ c_reg_0 int 32 regular  }
	{ c_reg_1_0 int 32 regular  }
	{ c_reg_2_0 int 32 regular  }
	{ c_reg_3_0 int 32 regular  }
	{ c_reg_4_0 int 32 regular  }
	{ c_reg_5_0 int 32 regular  }
	{ c_reg_6_0 int 32 regular  }
	{ c_reg_7_0 int 32 regular  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "c_0", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_7", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_6", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_5", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_4", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_3", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_2", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_1", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_reg_0", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "c_reg_1_0", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "c_reg_2_0", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "c_reg_3_0", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "c_reg_4_0", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "c_reg_5_0", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "c_reg_6_0", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "c_reg_7_0", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} ]}
# RTL Port declarations: 
set portNum 30
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ c_0 sc_out sc_lv 32 signal 0 } 
	{ c_0_ap_vld sc_out sc_logic 1 outvld 0 } 
	{ c_7 sc_out sc_lv 32 signal 1 } 
	{ c_7_ap_vld sc_out sc_logic 1 outvld 1 } 
	{ c_6 sc_out sc_lv 32 signal 2 } 
	{ c_6_ap_vld sc_out sc_logic 1 outvld 2 } 
	{ c_5 sc_out sc_lv 32 signal 3 } 
	{ c_5_ap_vld sc_out sc_logic 1 outvld 3 } 
	{ c_4 sc_out sc_lv 32 signal 4 } 
	{ c_4_ap_vld sc_out sc_logic 1 outvld 4 } 
	{ c_3 sc_out sc_lv 32 signal 5 } 
	{ c_3_ap_vld sc_out sc_logic 1 outvld 5 } 
	{ c_2 sc_out sc_lv 32 signal 6 } 
	{ c_2_ap_vld sc_out sc_logic 1 outvld 6 } 
	{ c_1 sc_out sc_lv 32 signal 7 } 
	{ c_1_ap_vld sc_out sc_logic 1 outvld 7 } 
	{ c_reg_0 sc_in sc_lv 32 signal 8 } 
	{ c_reg_1_0 sc_in sc_lv 32 signal 9 } 
	{ c_reg_2_0 sc_in sc_lv 32 signal 10 } 
	{ c_reg_3_0 sc_in sc_lv 32 signal 11 } 
	{ c_reg_4_0 sc_in sc_lv 32 signal 12 } 
	{ c_reg_5_0 sc_in sc_lv 32 signal 13 } 
	{ c_reg_6_0 sc_in sc_lv 32 signal 14 } 
	{ c_reg_7_0 sc_in sc_lv 32 signal 15 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "c_0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_0", "role": "default" }} , 
 	{ "name": "c_0_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_0", "role": "ap_vld" }} , 
 	{ "name": "c_7", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_7", "role": "default" }} , 
 	{ "name": "c_7_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_7", "role": "ap_vld" }} , 
 	{ "name": "c_6", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_6", "role": "default" }} , 
 	{ "name": "c_6_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_6", "role": "ap_vld" }} , 
 	{ "name": "c_5", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_5", "role": "default" }} , 
 	{ "name": "c_5_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_5", "role": "ap_vld" }} , 
 	{ "name": "c_4", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_4", "role": "default" }} , 
 	{ "name": "c_4_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_4", "role": "ap_vld" }} , 
 	{ "name": "c_3", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_3", "role": "default" }} , 
 	{ "name": "c_3_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_3", "role": "ap_vld" }} , 
 	{ "name": "c_2", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_2", "role": "default" }} , 
 	{ "name": "c_2_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_2", "role": "ap_vld" }} , 
 	{ "name": "c_1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_1", "role": "default" }} , 
 	{ "name": "c_1_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_1", "role": "ap_vld" }} , 
 	{ "name": "c_reg_0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_reg_0", "role": "default" }} , 
 	{ "name": "c_reg_1_0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_reg_1_0", "role": "default" }} , 
 	{ "name": "c_reg_2_0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_reg_2_0", "role": "default" }} , 
 	{ "name": "c_reg_3_0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_reg_3_0", "role": "default" }} , 
 	{ "name": "c_reg_4_0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_reg_4_0", "role": "default" }} , 
 	{ "name": "c_reg_5_0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_reg_5_0", "role": "default" }} , 
 	{ "name": "c_reg_6_0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_reg_6_0", "role": "default" }} , 
 	{ "name": "c_reg_7_0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_reg_7_0", "role": "default" }}  ]}

set ArgLastReadFirstWriteLatency {
	qgpu_ga_engine_parallel_Pipeline_AAMF_COMMIT_OUT {
		c_0 {Type O LastRead -1 FirstWrite 0}
		c_7 {Type O LastRead -1 FirstWrite 0}
		c_6 {Type O LastRead -1 FirstWrite 0}
		c_5 {Type O LastRead -1 FirstWrite 0}
		c_4 {Type O LastRead -1 FirstWrite 0}
		c_3 {Type O LastRead -1 FirstWrite 0}
		c_2 {Type O LastRead -1 FirstWrite 0}
		c_1 {Type O LastRead -1 FirstWrite 0}
		c_reg_0 {Type I LastRead 0 FirstWrite -1}
		c_reg_1_0 {Type I LastRead 0 FirstWrite -1}
		c_reg_2_0 {Type I LastRead 0 FirstWrite -1}
		c_reg_3_0 {Type I LastRead 0 FirstWrite -1}
		c_reg_4_0 {Type I LastRead 0 FirstWrite -1}
		c_reg_5_0 {Type I LastRead 0 FirstWrite -1}
		c_reg_6_0 {Type I LastRead 0 FirstWrite -1}
		c_reg_7_0 {Type I LastRead 0 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "10", "Max" : "10"}
	, {"Name" : "Interval", "Min" : "9", "Max" : "9"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	c_0 { ap_vld {  { c_0 out_data 1 32 }  { c_0_ap_vld out_vld 1 1 } } }
	c_7 { ap_vld {  { c_7 out_data 1 32 }  { c_7_ap_vld out_vld 1 1 } } }
	c_6 { ap_vld {  { c_6 out_data 1 32 }  { c_6_ap_vld out_vld 1 1 } } }
	c_5 { ap_vld {  { c_5 out_data 1 32 }  { c_5_ap_vld out_vld 1 1 } } }
	c_4 { ap_vld {  { c_4 out_data 1 32 }  { c_4_ap_vld out_vld 1 1 } } }
	c_3 { ap_vld {  { c_3 out_data 1 32 }  { c_3_ap_vld out_vld 1 1 } } }
	c_2 { ap_vld {  { c_2 out_data 1 32 }  { c_2_ap_vld out_vld 1 1 } } }
	c_1 { ap_vld {  { c_1 out_data 1 32 }  { c_1_ap_vld out_vld 1 1 } } }
	c_reg_0 { ap_none {  { c_reg_0 in_data 0 32 } } }
	c_reg_1_0 { ap_none {  { c_reg_1_0 in_data 0 32 } } }
	c_reg_2_0 { ap_none {  { c_reg_2_0 in_data 0 32 } } }
	c_reg_3_0 { ap_none {  { c_reg_3_0 in_data 0 32 } } }
	c_reg_4_0 { ap_none {  { c_reg_4_0 in_data 0 32 } } }
	c_reg_5_0 { ap_none {  { c_reg_5_0 in_data 0 32 } } }
	c_reg_6_0 { ap_none {  { c_reg_6_0 in_data 0 32 } } }
	c_reg_7_0 { ap_none {  { c_reg_7_0 in_data 0 32 } } }
}
