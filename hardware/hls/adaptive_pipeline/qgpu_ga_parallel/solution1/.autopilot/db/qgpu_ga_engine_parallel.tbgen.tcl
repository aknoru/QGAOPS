set moduleName qgpu_ga_engine_parallel
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
set C_modelName {qgpu_ga_engine_parallel}
set C_modelType { int 32 }
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
	{ c_0 int 32 regular {pointer 1}  }
	{ c_1 int 32 regular {pointer 1}  }
	{ c_2 int 32 regular {pointer 1}  }
	{ c_3 int 32 regular {pointer 1}  }
	{ c_4 int 32 regular {pointer 1}  }
	{ c_5 int 32 regular {pointer 1}  }
	{ c_6 int 32 regular {pointer 1}  }
	{ c_7 int 32 regular {pointer 1}  }
	{ opcode int 22 regular  }
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
 	{ "Name" : "c_0", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_1", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_2", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_3", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_4", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_5", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_6", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "c_7", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "opcode", "interface" : "wire", "bitwidth" : 22, "direction" : "READONLY"} , 
 	{ "Name" : "ap_return", "interface" : "wire", "bitwidth" : 32} ]}
# RTL Port declarations: 
set portNum 40
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
	{ c_0 sc_out sc_lv 32 signal 16 } 
	{ c_0_ap_vld sc_out sc_logic 1 outvld 16 } 
	{ c_1 sc_out sc_lv 32 signal 17 } 
	{ c_1_ap_vld sc_out sc_logic 1 outvld 17 } 
	{ c_2 sc_out sc_lv 32 signal 18 } 
	{ c_2_ap_vld sc_out sc_logic 1 outvld 18 } 
	{ c_3 sc_out sc_lv 32 signal 19 } 
	{ c_3_ap_vld sc_out sc_logic 1 outvld 19 } 
	{ c_4 sc_out sc_lv 32 signal 20 } 
	{ c_4_ap_vld sc_out sc_logic 1 outvld 20 } 
	{ c_5 sc_out sc_lv 32 signal 21 } 
	{ c_5_ap_vld sc_out sc_logic 1 outvld 21 } 
	{ c_6 sc_out sc_lv 32 signal 22 } 
	{ c_6_ap_vld sc_out sc_logic 1 outvld 22 } 
	{ c_7 sc_out sc_lv 32 signal 23 } 
	{ c_7_ap_vld sc_out sc_logic 1 outvld 23 } 
	{ opcode sc_in sc_lv 22 signal 24 } 
	{ ap_return sc_out sc_lv 32 signal -1 } 
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
 	{ "name": "c_0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_0", "role": "default" }} , 
 	{ "name": "c_0_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_0", "role": "ap_vld" }} , 
 	{ "name": "c_1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_1", "role": "default" }} , 
 	{ "name": "c_1_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_1", "role": "ap_vld" }} , 
 	{ "name": "c_2", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_2", "role": "default" }} , 
 	{ "name": "c_2_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_2", "role": "ap_vld" }} , 
 	{ "name": "c_3", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_3", "role": "default" }} , 
 	{ "name": "c_3_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_3", "role": "ap_vld" }} , 
 	{ "name": "c_4", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_4", "role": "default" }} , 
 	{ "name": "c_4_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_4", "role": "ap_vld" }} , 
 	{ "name": "c_5", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_5", "role": "default" }} , 
 	{ "name": "c_5_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_5", "role": "ap_vld" }} , 
 	{ "name": "c_6", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_6", "role": "default" }} , 
 	{ "name": "c_6_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_6", "role": "ap_vld" }} , 
 	{ "name": "c_7", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "c_7", "role": "default" }} , 
 	{ "name": "c_7_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "c_7", "role": "ap_vld" }} , 
 	{ "name": "opcode", "direction": "in", "datatype": "sc_lv", "bitwidth":22, "type": "signal", "bundle":{"name": "opcode", "role": "default" }} , 
 	{ "name": "ap_return", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return", "role": "default" }}  ]}

set ArgLastReadFirstWriteLatency {
	qgpu_ga_engine_parallel {
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
		c_0 {Type O LastRead -1 FirstWrite 0}
		c_1 {Type O LastRead -1 FirstWrite 0}
		c_2 {Type O LastRead -1 FirstWrite 0}
		c_3 {Type O LastRead -1 FirstWrite 0}
		c_4 {Type O LastRead -1 FirstWrite 0}
		c_5 {Type O LastRead -1 FirstWrite 0}
		c_6 {Type O LastRead -1 FirstWrite 0}
		c_7 {Type O LastRead -1 FirstWrite 0}
		opcode {Type I LastRead 0 FirstWrite -1}
		aamf_bank_a {Type IO LastRead -1 FirstWrite -1}
		aamf_bank_b {Type IO LastRead -1 FirstWrite -1}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
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
		aamf_bank_b {Type O LastRead -1 FirstWrite 0}}
	qgpu_ga_engine_parallel_Pipeline_AAMF_FETCH {
		base_addr {Type I LastRead 0 FirstWrite -1}
		p_out {Type O LastRead -1 FirstWrite 0}
		p_out1 {Type O LastRead -1 FirstWrite 0}
		p_out2 {Type O LastRead -1 FirstWrite 0}
		p_out3 {Type O LastRead -1 FirstWrite 0}
		p_out4 {Type O LastRead -1 FirstWrite 0}
		p_out5 {Type O LastRead -1 FirstWrite 0}
		p_out6 {Type O LastRead -1 FirstWrite 0}
		p_out7 {Type O LastRead -1 FirstWrite 0}
		p_out8 {Type O LastRead -1 FirstWrite 0}
		p_out9 {Type O LastRead -1 FirstWrite 0}
		p_out10 {Type O LastRead -1 FirstWrite 0}
		p_out11 {Type O LastRead -1 FirstWrite 0}
		p_out12 {Type O LastRead -1 FirstWrite 0}
		p_out13 {Type O LastRead -1 FirstWrite 0}
		p_out14 {Type O LastRead -1 FirstWrite 0}
		p_out15 {Type O LastRead -1 FirstWrite 0}
		p_out16 {Type O LastRead -1 FirstWrite 0}
		aamf_bank_a {Type I LastRead 0 FirstWrite -1}
		aamf_bank_b {Type I LastRead 0 FirstWrite -1}}
	ga_op_rotor_sandwich {
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
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
	ga_op_inner_product {
		a_0_val1 {Type I LastRead 0 FirstWrite -1}
		a_1_val2 {Type I LastRead 0 FirstWrite -1}
		a_2_val3 {Type I LastRead 0 FirstWrite -1}
		a_3_val4 {Type I LastRead 0 FirstWrite -1}
		a_4_val5 {Type I LastRead 0 FirstWrite -1}
		a_5_val6 {Type I LastRead 0 FirstWrite -1}
		a_6_val7 {Type I LastRead 0 FirstWrite -1}
		a_7_val8 {Type I LastRead 0 FirstWrite -1}
		b_0_val9 {Type I LastRead 0 FirstWrite -1}
		b_1_val10 {Type I LastRead 0 FirstWrite -1}
		b_2_val11 {Type I LastRead 0 FirstWrite -1}
		b_3_val12 {Type I LastRead 0 FirstWrite -1}
		b_4_val13 {Type I LastRead 0 FirstWrite -1}
		b_5_val14 {Type I LastRead 0 FirstWrite -1}
		b_6_val15 {Type I LastRead 0 FirstWrite -1}
		b_7_val16 {Type I LastRead 0 FirstWrite -1}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
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
		overflow_flag_read {Type I LastRead 1 FirstWrite -1}}
	ga_op_wedge_product {
		a_0_val1 {Type I LastRead 0 FirstWrite -1}
		a_1_val2 {Type I LastRead 0 FirstWrite -1}
		a_2_val3 {Type I LastRead 0 FirstWrite -1}
		a_3_val4 {Type I LastRead 0 FirstWrite -1}
		a_4_val5 {Type I LastRead 0 FirstWrite -1}
		a_5_val6 {Type I LastRead 0 FirstWrite -1}
		a_6_val7 {Type I LastRead 0 FirstWrite -1}
		a_7_val8 {Type I LastRead 0 FirstWrite -1}
		b_0_val9 {Type I LastRead 0 FirstWrite -1}
		b_1_val10 {Type I LastRead 0 FirstWrite -1}
		b_2_val11 {Type I LastRead 0 FirstWrite -1}
		b_3_val12 {Type I LastRead 0 FirstWrite -1}
		b_4_val13 {Type I LastRead 0 FirstWrite -1}
		b_5_val14 {Type I LastRead 0 FirstWrite -1}
		b_6_val15 {Type I LastRead 0 FirstWrite -1}
		b_7_val16 {Type I LastRead 0 FirstWrite -1}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
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
		overflow_flag_read {Type I LastRead 1 FirstWrite -1}}
	ga_op_geometric_product {
		a_0_val1 {Type I LastRead 0 FirstWrite -1}
		a_1_val2 {Type I LastRead 0 FirstWrite -1}
		a_2_val3 {Type I LastRead 0 FirstWrite -1}
		a_3_val4 {Type I LastRead 0 FirstWrite -1}
		a_4_val5 {Type I LastRead 0 FirstWrite -1}
		a_5_val6 {Type I LastRead 0 FirstWrite -1}
		a_6_val7 {Type I LastRead 0 FirstWrite -1}
		a_7_val8 {Type I LastRead 0 FirstWrite -1}
		b_0_val9 {Type I LastRead 0 FirstWrite -1}
		b_1_val10 {Type I LastRead 0 FirstWrite -1}
		b_2_val11 {Type I LastRead 0 FirstWrite -1}
		b_3_val12 {Type I LastRead 0 FirstWrite -1}
		b_4_val13 {Type I LastRead 0 FirstWrite -1}
		b_5_val14 {Type I LastRead 0 FirstWrite -1}
		b_6_val15 {Type I LastRead 0 FirstWrite -1}
		b_7_val16 {Type I LastRead 0 FirstWrite -1}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
	ga_op_rotor_norm {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}}
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
		c_reg_7_0 {Type I LastRead 0 FirstWrite -1}}
	ga_op_clifford_conjugation {
		c_write {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		c_write_14 {Type I LastRead 0 FirstWrite -1}}
	ga_op_grade_involution {
		c_write {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		c_write_10 {Type I LastRead 0 FirstWrite -1}
		c_write_11 {Type I LastRead 0 FirstWrite -1}
		c_write_12 {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}}
	ga_op_reverse {
		c_write {Type I LastRead 0 FirstWrite -1}
		c_write_4 {Type I LastRead 0 FirstWrite -1}
		c_write_5 {Type I LastRead 0 FirstWrite -1}
		c_write_6 {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}
		overflow_read {Type I LastRead 0 FirstWrite -1}}
	ga_op_grade_project {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}
		target_grade {Type I LastRead 0 FirstWrite -1}}
	ga_op_scalar_mul {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 2 FirstWrite -1}
		a_2_val {Type I LastRead 4 FirstWrite -1}
		a_3_val {Type I LastRead 6 FirstWrite -1}
		a_4_val {Type I LastRead 8 FirstWrite -1}
		a_5_val {Type I LastRead 10 FirstWrite -1}
		a_6_val {Type I LastRead 12 FirstWrite -1}
		a_7_val {Type I LastRead 14 FirstWrite -1}
		scalar_val {Type I LastRead 0 FirstWrite -1}}
	rescale_and_saturate {
		sum_val {Type I LastRead 0 FirstWrite -1}
		overflow_flag_read {Type I LastRead 1 FirstWrite -1}}
	ga_op_subtraction {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 1 FirstWrite -1}
		a_5_val {Type I LastRead 1 FirstWrite -1}
		a_6_val {Type I LastRead 1 FirstWrite -1}
		a_7_val {Type I LastRead 1 FirstWrite -1}
		b_0_val {Type I LastRead 0 FirstWrite -1}
		b_1_val {Type I LastRead 0 FirstWrite -1}
		b_2_val {Type I LastRead 0 FirstWrite -1}
		b_3_val {Type I LastRead 0 FirstWrite -1}
		b_4_val {Type I LastRead 1 FirstWrite -1}
		b_5_val {Type I LastRead 1 FirstWrite -1}
		b_6_val {Type I LastRead 1 FirstWrite -1}
		b_7_val {Type I LastRead 1 FirstWrite -1}}
	ga_op_addition {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 1 FirstWrite -1}
		a_5_val {Type I LastRead 1 FirstWrite -1}
		a_6_val {Type I LastRead 1 FirstWrite -1}
		a_7_val {Type I LastRead 1 FirstWrite -1}
		b_0_val {Type I LastRead 0 FirstWrite -1}
		b_1_val {Type I LastRead 0 FirstWrite -1}
		b_2_val {Type I LastRead 0 FirstWrite -1}
		b_3_val {Type I LastRead 0 FirstWrite -1}
		b_4_val {Type I LastRead 1 FirstWrite -1}
		b_5_val {Type I LastRead 1 FirstWrite -1}
		b_6_val {Type I LastRead 1 FirstWrite -1}
		b_7_val {Type I LastRead 1 FirstWrite -1}}
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
	{"Name" : "Latency", "Min" : "36", "Max" : "141"}
	, {"Name" : "Interval", "Min" : "36", "Max" : "141"}
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
	b_0_val { ap_none {  { b_0_val in_data 0 32 } } }
	b_1_val { ap_none {  { b_1_val in_data 0 32 } } }
	b_2_val { ap_none {  { b_2_val in_data 0 32 } } }
	b_3_val { ap_none {  { b_3_val in_data 0 32 } } }
	b_4_val { ap_none {  { b_4_val in_data 0 32 } } }
	b_5_val { ap_none {  { b_5_val in_data 0 32 } } }
	b_6_val { ap_none {  { b_6_val in_data 0 32 } } }
	b_7_val { ap_none {  { b_7_val in_data 0 32 } } }
	c_0 { ap_vld {  { c_0 out_data 1 32 }  { c_0_ap_vld out_vld 1 1 } } }
	c_1 { ap_vld {  { c_1 out_data 1 32 }  { c_1_ap_vld out_vld 1 1 } } }
	c_2 { ap_vld {  { c_2 out_data 1 32 }  { c_2_ap_vld out_vld 1 1 } } }
	c_3 { ap_vld {  { c_3 out_data 1 32 }  { c_3_ap_vld out_vld 1 1 } } }
	c_4 { ap_vld {  { c_4 out_data 1 32 }  { c_4_ap_vld out_vld 1 1 } } }
	c_5 { ap_vld {  { c_5 out_data 1 32 }  { c_5_ap_vld out_vld 1 1 } } }
	c_6 { ap_vld {  { c_6 out_data 1 32 }  { c_6_ap_vld out_vld 1 1 } } }
	c_7 { ap_vld {  { c_7 out_data 1 32 }  { c_7_ap_vld out_vld 1 1 } } }
	opcode { ap_none {  { opcode in_data 0 22 } } }
}
