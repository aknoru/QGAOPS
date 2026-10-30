set moduleName parallel_op_sandwich
set isTopModule 0
set isCombinational 0
set isDatapathOnly 0
set isPipelined 1
set isPipelined_legacy 1
set pipeline_type dataflow
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
set C_modelName {parallel_op_sandwich}
set C_modelType { void 0 }
set ap_memory_interface_dict [dict create]
set C_modelArgList {
	{ a_0_val3 int 32 regular {ap_stable 0} }
	{ a_1_val5 int 32 regular {ap_stable 0} }
	{ a_2_val7 int 32 regular {ap_stable 0} }
	{ a_3_val9 int 32 regular {ap_stable 0} }
	{ a_4_val11 int 32 regular {ap_stable 0} }
	{ a_5_val13 int 32 regular {ap_stable 0} }
	{ a_6_val15 int 32 regular {ap_stable 0} }
	{ a_7_val17 int 32 regular {ap_stable 0} }
	{ b_0_val18 int 32 regular {ap_stable 0} }
	{ b_1_val19 int 32 regular {ap_stable 0} }
	{ b_2_val20 int 32 regular {ap_stable 0} }
	{ b_3_val21 int 32 regular {ap_stable 0} }
	{ b_4_val22 int 32 regular {ap_stable 0} }
	{ b_5_val23 int 32 regular {ap_stable 0} }
	{ b_6_val24 int 32 regular {ap_stable 0} }
	{ b_7_val25 int 32 regular {ap_stable 0} }
	{ c_0 int 32 regular {pointer 1}  }
	{ c_1 int 32 regular {pointer 1}  }
	{ c_2 int 32 regular {pointer 1}  }
	{ c_3 int 32 regular {pointer 1}  }
	{ c_4 int 32 regular {pointer 1}  }
	{ c_5 int 32 regular {pointer 1}  }
	{ c_6 int 32 regular {pointer 1}  }
	{ c_7 int 32 regular {pointer 1}  }
	{ overflow_in int 1 regular {pointer 0 stable }  }
	{ overflow_out int 1 regular {pointer 1}  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "a_0_val3", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_1_val5", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_2_val7", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_3_val9", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_4_val11", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_5_val13", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_6_val15", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_7_val17", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_0_val18", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_1_val19", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_2_val20", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_3_val21", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_4_val22", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_5_val23", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_6_val24", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_7_val25", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "c_0", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_1", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_2", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_3", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_4", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_5", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_6", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_7", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "overflow_in", "interface" : "wire", "bitwidth" : 1, "direction" : "READONLY"} , 
 	{ "Name" : "overflow_out", "interface" : "wire", "bitwidth" : 1, "direction" : "WRITEONLY"} ]}
# RTL Port declarations: 
set portNum 59
set portList { 
	{ a_0_val3 sc_in sc_lv 32 signal 0 } 
	{ a_1_val5 sc_in sc_lv 32 signal 1 } 
	{ a_2_val7 sc_in sc_lv 32 signal 2 } 
	{ a_3_val9 sc_in sc_lv 32 signal 3 } 
	{ a_4_val11 sc_in sc_lv 32 signal 4 } 
	{ a_5_val13 sc_in sc_lv 32 signal 5 } 
	{ a_6_val15 sc_in sc_lv 32 signal 6 } 
	{ a_7_val17 sc_in sc_lv 32 signal 7 } 
	{ b_0_val18 sc_in sc_lv 32 signal 8 } 
	{ b_1_val19 sc_in sc_lv 32 signal 9 } 
	{ b_2_val20 sc_in sc_lv 32 signal 10 } 
	{ b_3_val21 sc_in sc_lv 32 signal 11 } 
	{ b_4_val22 sc_in sc_lv 32 signal 12 } 
	{ b_5_val23 sc_in sc_lv 32 signal 13 } 
	{ b_6_val24 sc_in sc_lv 32 signal 14 } 
	{ b_7_val25 sc_in sc_lv 32 signal 15 } 
	{ c_0 sc_out sc_lv 32 signal 16 } 
	{ c_1 sc_out sc_lv 32 signal 17 } 
	{ c_2 sc_out sc_lv 32 signal 18 } 
	{ c_3 sc_out sc_lv 32 signal 19 } 
	{ c_4 sc_out sc_lv 32 signal 20 } 
	{ c_5 sc_out sc_lv 32 signal 21 } 
	{ c_6 sc_out sc_lv 32 signal 22 } 
	{ c_7 sc_out sc_lv 32 signal 23 } 
	{ overflow_in sc_in sc_lv 1 signal 24 } 
	{ overflow_out sc_out sc_lv 1 signal 25 } 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ a_0_val3_ap_vld sc_in sc_logic 1 invld 0 } 
	{ a_1_val5_ap_vld sc_in sc_logic 1 invld 1 } 
	{ a_2_val7_ap_vld sc_in sc_logic 1 invld 2 } 
	{ a_3_val9_ap_vld sc_in sc_logic 1 invld 3 } 
	{ a_4_val11_ap_vld sc_in sc_logic 1 invld 4 } 
	{ a_5_val13_ap_vld sc_in sc_logic 1 invld 5 } 
	{ a_6_val15_ap_vld sc_in sc_logic 1 invld 6 } 
	{ a_7_val17_ap_vld sc_in sc_logic 1 invld 7 } 
	{ b_0_val18_ap_vld sc_in sc_logic 1 invld 8 } 
	{ b_1_val19_ap_vld sc_in sc_logic 1 invld 9 } 
	{ b_2_val20_ap_vld sc_in sc_logic 1 invld 10 } 
	{ b_3_val21_ap_vld sc_in sc_logic 1 invld 11 } 
	{ b_4_val22_ap_vld sc_in sc_logic 1 invld 12 } 
	{ b_5_val23_ap_vld sc_in sc_logic 1 invld 13 } 
	{ b_6_val24_ap_vld sc_in sc_logic 1 invld 14 } 
	{ b_7_val25_ap_vld sc_in sc_logic 1 invld 15 } 
	{ overflow_in_ap_vld sc_in sc_logic 1 invld 24 } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ c_0_ap_vld sc_out sc_logic 1 outvld 16 } 
	{ c_1_ap_vld sc_out sc_logic 1 outvld 17 } 
	{ c_2_ap_vld sc_out sc_logic 1 outvld 18 } 
	{ c_3_ap_vld sc_out sc_logic 1 outvld 19 } 
	{ c_4_ap_vld sc_out sc_logic 1 outvld 20 } 
	{ c_5_ap_vld sc_out sc_logic 1 outvld 21 } 
	{ c_6_ap_vld sc_out sc_logic 1 outvld 22 } 
	{ c_7_ap_vld sc_out sc_logic 1 outvld 23 } 
	{ overflow_out_ap_vld sc_out sc_logic 1 outvld 25 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_continue sc_in sc_logic 1 continue -1 } 
}
set NewPortList {[ 
	{ "name": "a_0_val3", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_0_val3", "role": "default" }} , 
 	{ "name": "a_1_val5", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_1_val5", "role": "default" }} , 
 	{ "name": "a_2_val7", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_2_val7", "role": "default" }} , 
 	{ "name": "a_3_val9", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_3_val9", "role": "default" }} , 
 	{ "name": "a_4_val11", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_4_val11", "role": "default" }} , 
 	{ "name": "a_5_val13", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_5_val13", "role": "default" }} , 
 	{ "name": "a_6_val15", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_6_val15", "role": "default" }} , 
 	{ "name": "a_7_val17", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_7_val17", "role": "default" }} , 
 	{ "name": "b_0_val18", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_0_val18", "role": "default" }} , 
 	{ "name": "b_1_val19", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_1_val19", "role": "default" }} , 
 	{ "name": "b_2_val20", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_2_val20", "role": "default" }} , 
 	{ "name": "b_3_val21", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_3_val21", "role": "default" }} , 
 	{ "name": "b_4_val22", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_4_val22", "role": "default" }} , 
 	{ "name": "b_5_val23", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_5_val23", "role": "default" }} , 
 	{ "name": "b_6_val24", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_6_val24", "role": "default" }} , 
 	{ "name": "b_7_val25", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_7_val25", "role": "default" }} , 
 	{ "name": "c_0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_0", "role": "default" }} , 
 	{ "name": "c_1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_1", "role": "default" }} , 
 	{ "name": "c_2", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_2", "role": "default" }} , 
 	{ "name": "c_3", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_3", "role": "default" }} , 
 	{ "name": "c_4", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_4", "role": "default" }} , 
 	{ "name": "c_5", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_5", "role": "default" }} , 
 	{ "name": "c_6", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_6", "role": "default" }} , 
 	{ "name": "c_7", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_7", "role": "default" }} , 
 	{ "name": "overflow_in", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "overflow_in", "role": "default" }} , 
 	{ "name": "overflow_out", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "overflow_out", "role": "default" }} , 
 	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "a_0_val3_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "a_0_val3", "role": "ap_vld" }} , 
 	{ "name": "a_1_val5_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "a_1_val5", "role": "ap_vld" }} , 
 	{ "name": "a_2_val7_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "a_2_val7", "role": "ap_vld" }} , 
 	{ "name": "a_3_val9_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "a_3_val9", "role": "ap_vld" }} , 
 	{ "name": "a_4_val11_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "a_4_val11", "role": "ap_vld" }} , 
 	{ "name": "a_5_val13_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "a_5_val13", "role": "ap_vld" }} , 
 	{ "name": "a_6_val15_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "a_6_val15", "role": "ap_vld" }} , 
 	{ "name": "a_7_val17_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "a_7_val17", "role": "ap_vld" }} , 
 	{ "name": "b_0_val18_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "b_0_val18", "role": "ap_vld" }} , 
 	{ "name": "b_1_val19_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "b_1_val19", "role": "ap_vld" }} , 
 	{ "name": "b_2_val20_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "b_2_val20", "role": "ap_vld" }} , 
 	{ "name": "b_3_val21_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "b_3_val21", "role": "ap_vld" }} , 
 	{ "name": "b_4_val22_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "b_4_val22", "role": "ap_vld" }} , 
 	{ "name": "b_5_val23_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "b_5_val23", "role": "ap_vld" }} , 
 	{ "name": "b_6_val24_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "b_6_val24", "role": "ap_vld" }} , 
 	{ "name": "b_7_val25_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "b_7_val25", "role": "ap_vld" }} , 
 	{ "name": "overflow_in_ap_vld", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "invld", "bundle":{"name": "overflow_in", "role": "ap_vld" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "c_0_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_0", "role": "ap_vld" }} , 
 	{ "name": "c_1_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_1", "role": "ap_vld" }} , 
 	{ "name": "c_2_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_2", "role": "ap_vld" }} , 
 	{ "name": "c_3_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_3", "role": "ap_vld" }} , 
 	{ "name": "c_4_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_4", "role": "ap_vld" }} , 
 	{ "name": "c_5_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_5", "role": "ap_vld" }} , 
 	{ "name": "c_6_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_6", "role": "ap_vld" }} , 
 	{ "name": "c_7_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_7", "role": "ap_vld" }} , 
 	{ "name": "overflow_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "overflow_out", "role": "ap_vld" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_continue", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "continue", "bundle":{"name": "ap_continue", "role": "default" }}  ]}

set ArgLastReadFirstWriteLatency {
	parallel_op_sandwich {
		a_0_val3 {Type I LastRead 0 FirstWrite -1}
		a_1_val5 {Type I LastRead 0 FirstWrite -1}
		a_2_val7 {Type I LastRead 0 FirstWrite -1}
		a_3_val9 {Type I LastRead 0 FirstWrite -1}
		a_4_val11 {Type I LastRead 0 FirstWrite -1}
		a_5_val13 {Type I LastRead 0 FirstWrite -1}
		a_6_val15 {Type I LastRead 0 FirstWrite -1}
		a_7_val17 {Type I LastRead 0 FirstWrite -1}
		b_0_val18 {Type I LastRead 0 FirstWrite -1}
		b_1_val19 {Type I LastRead 0 FirstWrite -1}
		b_2_val20 {Type I LastRead 0 FirstWrite -1}
		b_3_val21 {Type I LastRead 0 FirstWrite -1}
		b_4_val22 {Type I LastRead 0 FirstWrite -1}
		b_5_val23 {Type I LastRead 0 FirstWrite -1}
		b_6_val24 {Type I LastRead 0 FirstWrite -1}
		b_7_val25 {Type I LastRead 0 FirstWrite -1}
		c_0 {Type O LastRead -1 FirstWrite 8}
		c_1 {Type O LastRead -1 FirstWrite 8}
		c_2 {Type O LastRead -1 FirstWrite 8}
		c_3 {Type O LastRead -1 FirstWrite 8}
		c_4 {Type O LastRead -1 FirstWrite 8}
		c_5 {Type O LastRead -1 FirstWrite 8}
		c_6 {Type O LastRead -1 FirstWrite 8}
		c_7 {Type O LastRead -1 FirstWrite 8}
		overflow_in {Type I LastRead 8 FirstWrite -1}
		overflow_out {Type O LastRead -1 FirstWrite 9}}
	parallel_product_core {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 1 FirstWrite -1}
		a_4_val {Type I LastRead 2 FirstWrite -1}
		a_5_val {Type I LastRead 2 FirstWrite -1}
		a_6_val {Type I LastRead 3 FirstWrite -1}
		a_7_val {Type I LastRead 3 FirstWrite -1}
		b_0_val {Type I LastRead 0 FirstWrite -1}
		b_1_val {Type I LastRead 0 FirstWrite -1}
		b_2_val {Type I LastRead 0 FirstWrite -1}
		b_3_val {Type I LastRead 0 FirstWrite -1}
		b_4_val {Type I LastRead 0 FirstWrite -1}
		b_5_val {Type I LastRead 0 FirstWrite -1}
		b_6_val {Type I LastRead 0 FirstWrite -1}
		b_7_val {Type I LastRead 0 FirstWrite -1}
		overflow_in {Type I LastRead 8 FirstWrite -1}}
	parallel_op_reverse {
		c_write {Type I LastRead 0 FirstWrite -1}
		c_write_10 {Type I LastRead 0 FirstWrite -1}
		c_write_11 {Type I LastRead 0 FirstWrite -1}
		c_write_12 {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}
		p_read8 {Type I LastRead 0 FirstWrite -1}}
	parallel_product_core_3 {
		p_read {Type I LastRead 0 FirstWrite -1}
		p_read1 {Type I LastRead 0 FirstWrite -1}
		p_read2 {Type I LastRead 0 FirstWrite -1}
		p_read3 {Type I LastRead 0 FirstWrite -1}
		p_read4 {Type I LastRead 0 FirstWrite -1}
		p_read5 {Type I LastRead 0 FirstWrite -1}
		p_read6 {Type I LastRead 0 FirstWrite -1}
		p_read7 {Type I LastRead 0 FirstWrite -1}
		p_read8 {Type I LastRead 0 FirstWrite -1}
		p_read9 {Type I LastRead 0 FirstWrite -1}
		p_read10 {Type I LastRead 0 FirstWrite -1}
		p_read11 {Type I LastRead 0 FirstWrite -1}
		p_read12 {Type I LastRead 0 FirstWrite -1}
		p_read13 {Type I LastRead 0 FirstWrite -1}
		p_read14 {Type I LastRead 0 FirstWrite -1}
		p_read15 {Type I LastRead 0 FirstWrite -1}
		c_0 {Type O LastRead -1 FirstWrite 8}
		c_1 {Type O LastRead -1 FirstWrite 8}
		c_2 {Type O LastRead -1 FirstWrite 8}
		c_3 {Type O LastRead -1 FirstWrite 8}
		c_4 {Type O LastRead -1 FirstWrite 8}
		c_5 {Type O LastRead -1 FirstWrite 8}
		c_6 {Type O LastRead -1 FirstWrite 8}
		c_7 {Type O LastRead -1 FirstWrite 8}
		p_read16 {Type I LastRead 0 FirstWrite -1}
		overflow_out {Type O LastRead -1 FirstWrite 9}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "19", "Max" : "19"}
	, {"Name" : "Interval", "Min" : "1", "Max" : "1"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	a_0_val3 { ap_none {  { a_0_val3 in_data 0 32 }  { a_0_val3_ap_vld in_vld 0 1 } } }
	a_1_val5 { ap_none {  { a_1_val5 in_data 0 32 }  { a_1_val5_ap_vld in_vld 0 1 } } }
	a_2_val7 { ap_none {  { a_2_val7 in_data 0 32 }  { a_2_val7_ap_vld in_vld 0 1 } } }
	a_3_val9 { ap_none {  { a_3_val9 in_data 0 32 }  { a_3_val9_ap_vld in_vld 0 1 } } }
	a_4_val11 { ap_none {  { a_4_val11 in_data 0 32 }  { a_4_val11_ap_vld in_vld 0 1 } } }
	a_5_val13 { ap_none {  { a_5_val13 in_data 0 32 }  { a_5_val13_ap_vld in_vld 0 1 } } }
	a_6_val15 { ap_none {  { a_6_val15 in_data 0 32 }  { a_6_val15_ap_vld in_vld 0 1 } } }
	a_7_val17 { ap_none {  { a_7_val17 in_data 0 32 }  { a_7_val17_ap_vld in_vld 0 1 } } }
	b_0_val18 { ap_none {  { b_0_val18 in_data 0 32 }  { b_0_val18_ap_vld in_vld 0 1 } } }
	b_1_val19 { ap_none {  { b_1_val19 in_data 0 32 }  { b_1_val19_ap_vld in_vld 0 1 } } }
	b_2_val20 { ap_none {  { b_2_val20 in_data 0 32 }  { b_2_val20_ap_vld in_vld 0 1 } } }
	b_3_val21 { ap_none {  { b_3_val21 in_data 0 32 }  { b_3_val21_ap_vld in_vld 0 1 } } }
	b_4_val22 { ap_none {  { b_4_val22 in_data 0 32 }  { b_4_val22_ap_vld in_vld 0 1 } } }
	b_5_val23 { ap_none {  { b_5_val23 in_data 0 32 }  { b_5_val23_ap_vld in_vld 0 1 } } }
	b_6_val24 { ap_none {  { b_6_val24 in_data 0 32 }  { b_6_val24_ap_vld in_vld 0 1 } } }
	b_7_val25 { ap_none {  { b_7_val25 in_data 0 32 }  { b_7_val25_ap_vld in_vld 0 1 } } }
	c_0 { ap_vld {  { c_0 out_data 1 32 }  { c_0_ap_vld out_vld 1 1 } } }
	c_1 { ap_vld {  { c_1 out_data 1 32 }  { c_1_ap_vld out_vld 1 1 } } }
	c_2 { ap_vld {  { c_2 out_data 1 32 }  { c_2_ap_vld out_vld 1 1 } } }
	c_3 { ap_vld {  { c_3 out_data 1 32 }  { c_3_ap_vld out_vld 1 1 } } }
	c_4 { ap_vld {  { c_4 out_data 1 32 }  { c_4_ap_vld out_vld 1 1 } } }
	c_5 { ap_vld {  { c_5 out_data 1 32 }  { c_5_ap_vld out_vld 1 1 } } }
	c_6 { ap_vld {  { c_6 out_data 1 32 }  { c_6_ap_vld out_vld 1 1 } } }
	c_7 { ap_vld {  { c_7 out_data 1 32 }  { c_7_ap_vld out_vld 1 1 } } }
	overflow_in { ap_none {  { overflow_in in_data 0 1 }  { overflow_in_ap_vld in_vld 0 1 } } }
	overflow_out { ap_vld {  { overflow_out out_data 1 1 }  { overflow_out_ap_vld out_vld 1 1 } } }
}
