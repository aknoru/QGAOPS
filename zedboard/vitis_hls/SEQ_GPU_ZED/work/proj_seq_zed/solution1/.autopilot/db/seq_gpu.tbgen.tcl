set moduleName seq_gpu
set isTopModule 1
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
set cdfgNum 18
set C_modelName {seq_gpu}
set C_modelType { void 0 }
set ap_memory_interface_dict [dict create]
dict set ap_memory_interface_dict a { MEM_WIDTH 32 MEM_SIZE 32 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 1 }
dict set ap_memory_interface_dict b { MEM_WIDTH 32 MEM_SIZE 32 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 1 }
dict set ap_memory_interface_dict c { MEM_WIDTH 32 MEM_SIZE 32 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 1 }
set C_modelArgList {
	{ a int 32 regular {axi_slave 0}  }
	{ b int 32 regular {axi_slave 0}  }
	{ c int 32 regular {axi_slave 1}  }
	{ opcode int 32 regular {axi_slave 0}  }
	{ status int 32 regular {axi_slave 1}  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "a", "interface" : "axi_slave", "bundle":"control","type":"ap_memory","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":32}, "offset_end" : {"in":63}} , 
 	{ "Name" : "b", "interface" : "axi_slave", "bundle":"control","type":"ap_memory","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":64}, "offset_end" : {"in":95}} , 
 	{ "Name" : "c", "interface" : "axi_slave", "bundle":"control","type":"ap_memory","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":96}, "offset_end" : {"out":127}} , 
 	{ "Name" : "opcode", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":16}, "offset_end" : {"in":23}} , 
 	{ "Name" : "status", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":128}, "offset_end" : {"out":135}} ]}
# RTL Port declarations: 
set portNum 20
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst_n sc_in sc_logic 1 reset -1 active_low_sync } 
	{ s_axi_control_AWVALID sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_AWREADY sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_AWADDR sc_in sc_lv 8 signal -1 } 
	{ s_axi_control_WVALID sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_WREADY sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_WDATA sc_in sc_lv 32 signal -1 } 
	{ s_axi_control_WSTRB sc_in sc_lv 4 signal -1 } 
	{ s_axi_control_ARVALID sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_ARREADY sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_ARADDR sc_in sc_lv 8 signal -1 } 
	{ s_axi_control_RVALID sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_RREADY sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_RDATA sc_out sc_lv 32 signal -1 } 
	{ s_axi_control_RRESP sc_out sc_lv 2 signal -1 } 
	{ s_axi_control_BVALID sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_BREADY sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_BRESP sc_out sc_lv 2 signal -1 } 
	{ interrupt sc_out sc_logic 1 signal -1 } 
}
set NewPortList {[ 
	{ "name": "s_axi_control_AWADDR", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "control", "role": "AWADDR" },"address":[{"name":"seq_gpu","role":"start","value":"0","valid_bit":"0"},{"name":"seq_gpu","role":"continue","value":"0","valid_bit":"4"},{"name":"seq_gpu","role":"auto_start","value":"0","valid_bit":"7"},{"name":"opcode","role":"data","value":"16"},{"name":"a","role":"data","value":"32"},{"name":"b","role":"data","value":"64"}] },
	{ "name": "s_axi_control_AWVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "AWVALID" } },
	{ "name": "s_axi_control_AWREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "AWREADY" } },
	{ "name": "s_axi_control_WVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "WVALID" } },
	{ "name": "s_axi_control_WREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "WREADY" } },
	{ "name": "s_axi_control_WDATA", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "control", "role": "WDATA" } },
	{ "name": "s_axi_control_WSTRB", "direction": "in", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "control", "role": "WSTRB" } },
	{ "name": "s_axi_control_ARADDR", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "control", "role": "ARADDR" },"address":[{"name":"seq_gpu","role":"start","value":"0","valid_bit":"0"},{"name":"seq_gpu","role":"done","value":"0","valid_bit":"1"},{"name":"seq_gpu","role":"idle","value":"0","valid_bit":"2"},{"name":"seq_gpu","role":"ready","value":"0","valid_bit":"3"},{"name":"seq_gpu","role":"auto_start","value":"0","valid_bit":"7"},{"name":"c","role":"data","value":"96"},{"name":"status","role":"data","value":"128"}, {"name":"status","role":"valid","value":"132","valid_bit":"0"}] },
	{ "name": "s_axi_control_ARVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "ARVALID" } },
	{ "name": "s_axi_control_ARREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "ARREADY" } },
	{ "name": "s_axi_control_RVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "RVALID" } },
	{ "name": "s_axi_control_RREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "RREADY" } },
	{ "name": "s_axi_control_RDATA", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "control", "role": "RDATA" } },
	{ "name": "s_axi_control_RRESP", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "control", "role": "RRESP" } },
	{ "name": "s_axi_control_BVALID", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "BVALID" } },
	{ "name": "s_axi_control_BREADY", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "BREADY" } },
	{ "name": "s_axi_control_BRESP", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "control", "role": "BRESP" } },
	{ "name": "interrupt", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "interrupt" } }, 
 	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst_n", "role": "default" }}  ]}

set ArgLastReadFirstWriteLatency {
	seq_gpu {
		a {Type I LastRead 2 FirstWrite -1}
		b {Type I LastRead 2 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 0}
		opcode {Type I LastRead 0 FirstWrite -1}
		status {Type O LastRead -1 FirstWrite 2}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
	seq_op_rotor_norm {
		a {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 0}}
	seq_op_rotor_norm_Pipeline_NORM_LOOP {
		a {Type I LastRead 0 FirstWrite -1}
		sum_sq_out {Type O LastRead -1 FirstWrite 2}}
	seq_op_rotor_norm_Pipeline_CLEAR_REMAINING {
		c {Type O LastRead -1 FirstWrite 0}}
	seq_op_sandwich {
		a {Type I LastRead 2 FirstWrite -1}
		b {Type I LastRead 2 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
	seq_product_core {
		a {Type I LastRead 2 FirstWrite -1}
		b {Type I LastRead 2 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}
		opcode {Type I LastRead 0 FirstWrite -1}
		overflow_read {Type I LastRead 4 FirstWrite -1}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
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
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
	seq_product_core_Pipeline_RESCALE_LOOP {
		accum_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_1_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_2_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_3_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_4_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_5_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_6_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_7_load_reload {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}
		write_flag_0_out {Type O LastRead -1 FirstWrite 1}
		overflow_0_out {Type O LastRead -1 FirstWrite 1}}
	seq_op_reverse {
		a {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}
		overflow_read {Type I LastRead 0 FirstWrite -1}}
	seq_op_clifford_conj {
		a {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}}
	seq_op_grade_involution {
		a {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}}
	seq_op_reverse {
		a {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}
		overflow_read {Type I LastRead 0 FirstWrite -1}}
	seq_op_sub {
		a {Type I LastRead 0 FirstWrite -1}
		b {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}}
	seq_op_add {
		a {Type I LastRead 0 FirstWrite -1}
		b {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}}
	seq_product_core {
		a {Type I LastRead 2 FirstWrite -1}
		b {Type I LastRead 2 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}
		opcode {Type I LastRead 0 FirstWrite -1}
		overflow_read {Type I LastRead 4 FirstWrite -1}
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
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
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}
	seq_product_core_Pipeline_RESCALE_LOOP {
		accum_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_1_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_2_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_3_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_4_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_5_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_6_load_reload {Type I LastRead 0 FirstWrite -1}
		accum_7_load_reload {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}
		write_flag_0_out {Type O LastRead -1 FirstWrite 1}
		overflow_0_out {Type O LastRead -1 FirstWrite 1}}
	seq_gpu_Pipeline_CLEAR_ERR {
		c {Type O LastRead -1 FirstWrite 0}}
	seq_op_grade_proj {
		a {Type I LastRead 0 FirstWrite -1}
		grade_target {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 1}}
	seq_op_scalar_mul {
		a {Type I LastRead 0 FirstWrite -1}
		scalar_val {Type I LastRead 0 FirstWrite -1}
		c {Type O LastRead -1 FirstWrite 4}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "12", "Max" : "188"}
	, {"Name" : "Interval", "Min" : "13", "Max" : "189"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
}

set maxi_interface_dict [dict create]

# RTL port scheduling information:
set fifoSchedulingInfoList { 
}

# RTL bus port read request latency information:
set busReadReqLatencyList { 
}

# RTL bus port write response latency information:
set busWriteResLatencyList { 
}

# RTL array port load latency information:
set memoryLoadLatencyList { 
}
