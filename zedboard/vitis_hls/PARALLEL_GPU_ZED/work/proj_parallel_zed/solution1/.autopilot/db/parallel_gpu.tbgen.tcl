set moduleName parallel_gpu
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
set cdfgNum 16
set C_modelName {parallel_gpu}
set C_modelType { void 0 }
set ap_memory_interface_dict [dict create]
set C_modelArgList {
	{ a_0 int 32 regular {axi_slave 0}  }
	{ a_1 int 32 regular {axi_slave 0}  }
	{ a_2 int 32 regular {axi_slave 0}  }
	{ a_3 int 32 regular {axi_slave 0}  }
	{ a_4 int 32 regular {axi_slave 0}  }
	{ a_5 int 32 regular {axi_slave 0}  }
	{ a_6 int 32 regular {axi_slave 0}  }
	{ a_7 int 32 regular {axi_slave 0}  }
	{ b_0 int 32 regular {axi_slave 0}  }
	{ b_1 int 32 regular {axi_slave 0}  }
	{ b_2 int 32 regular {axi_slave 0}  }
	{ b_3 int 32 regular {axi_slave 0}  }
	{ b_4 int 32 regular {axi_slave 0}  }
	{ b_5 int 32 regular {axi_slave 0}  }
	{ b_6 int 32 regular {axi_slave 0}  }
	{ b_7 int 32 regular {axi_slave 0}  }
	{ c_0 int 32 regular {axi_slave 1}  }
	{ c_1 int 32 regular {axi_slave 1}  }
	{ c_2 int 32 regular {axi_slave 1}  }
	{ c_3 int 32 regular {axi_slave 1}  }
	{ c_4 int 32 regular {axi_slave 1}  }
	{ c_5 int 32 regular {axi_slave 1}  }
	{ c_6 int 32 regular {axi_slave 1}  }
	{ c_7 int 32 regular {axi_slave 1}  }
	{ opcode int 32 regular {axi_slave 0}  }
	{ status int 32 regular {axi_slave 1}  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "a_0", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":16}, "offset_end" : {"in":23}} , 
 	{ "Name" : "a_1", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":24}, "offset_end" : {"in":31}} , 
 	{ "Name" : "a_2", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":32}, "offset_end" : {"in":39}} , 
 	{ "Name" : "a_3", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":40}, "offset_end" : {"in":47}} , 
 	{ "Name" : "a_4", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":48}, "offset_end" : {"in":55}} , 
 	{ "Name" : "a_5", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":56}, "offset_end" : {"in":63}} , 
 	{ "Name" : "a_6", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":64}, "offset_end" : {"in":71}} , 
 	{ "Name" : "a_7", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":72}, "offset_end" : {"in":79}} , 
 	{ "Name" : "b_0", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":80}, "offset_end" : {"in":87}} , 
 	{ "Name" : "b_1", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":88}, "offset_end" : {"in":95}} , 
 	{ "Name" : "b_2", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":96}, "offset_end" : {"in":103}} , 
 	{ "Name" : "b_3", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":104}, "offset_end" : {"in":111}} , 
 	{ "Name" : "b_4", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":112}, "offset_end" : {"in":119}} , 
 	{ "Name" : "b_5", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":120}, "offset_end" : {"in":127}} , 
 	{ "Name" : "b_6", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":128}, "offset_end" : {"in":135}} , 
 	{ "Name" : "b_7", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":136}, "offset_end" : {"in":143}} , 
 	{ "Name" : "c_0", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":144}, "offset_end" : {"out":151}} , 
 	{ "Name" : "c_1", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":160}, "offset_end" : {"out":167}} , 
 	{ "Name" : "c_2", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":176}, "offset_end" : {"out":183}} , 
 	{ "Name" : "c_3", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":192}, "offset_end" : {"out":199}} , 
 	{ "Name" : "c_4", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":208}, "offset_end" : {"out":215}} , 
 	{ "Name" : "c_5", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":224}, "offset_end" : {"out":231}} , 
 	{ "Name" : "c_6", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":240}, "offset_end" : {"out":247}} , 
 	{ "Name" : "c_7", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":256}, "offset_end" : {"out":263}} , 
 	{ "Name" : "opcode", "interface" : "axi_slave", "bundle":"control","type":"ap_none","bitwidth" : 32, "direction" : "READONLY", "offset" : {"in":272}, "offset_end" : {"in":279}} , 
 	{ "Name" : "status", "interface" : "axi_slave", "bundle":"control","type":"ap_vld","bitwidth" : 32, "direction" : "WRITEONLY", "offset" : {"out":280}, "offset_end" : {"out":287}} ]}
# RTL Port declarations: 
set portNum 20
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst_n sc_in sc_logic 1 reset -1 active_low_sync } 
	{ s_axi_control_AWVALID sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_AWREADY sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_AWADDR sc_in sc_lv 9 signal -1 } 
	{ s_axi_control_WVALID sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_WREADY sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_WDATA sc_in sc_lv 32 signal -1 } 
	{ s_axi_control_WSTRB sc_in sc_lv 4 signal -1 } 
	{ s_axi_control_ARVALID sc_in sc_logic 1 signal -1 } 
	{ s_axi_control_ARREADY sc_out sc_logic 1 signal -1 } 
	{ s_axi_control_ARADDR sc_in sc_lv 9 signal -1 } 
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
	{ "name": "s_axi_control_AWADDR", "direction": "in", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "control", "role": "AWADDR" },"address":[{"name":"parallel_gpu","role":"start","value":"0","valid_bit":"0"},{"name":"parallel_gpu","role":"continue","value":"0","valid_bit":"4"},{"name":"parallel_gpu","role":"auto_start","value":"0","valid_bit":"7"},{"name":"a_0","role":"data","value":"16"},{"name":"a_1","role":"data","value":"24"},{"name":"a_2","role":"data","value":"32"},{"name":"a_3","role":"data","value":"40"},{"name":"a_4","role":"data","value":"48"},{"name":"a_5","role":"data","value":"56"},{"name":"a_6","role":"data","value":"64"},{"name":"a_7","role":"data","value":"72"},{"name":"b_0","role":"data","value":"80"},{"name":"b_1","role":"data","value":"88"},{"name":"b_2","role":"data","value":"96"},{"name":"b_3","role":"data","value":"104"},{"name":"b_4","role":"data","value":"112"},{"name":"b_5","role":"data","value":"120"},{"name":"b_6","role":"data","value":"128"},{"name":"b_7","role":"data","value":"136"},{"name":"opcode","role":"data","value":"272"}] },
	{ "name": "s_axi_control_AWVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "AWVALID" } },
	{ "name": "s_axi_control_AWREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "AWREADY" } },
	{ "name": "s_axi_control_WVALID", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "WVALID" } },
	{ "name": "s_axi_control_WREADY", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "control", "role": "WREADY" } },
	{ "name": "s_axi_control_WDATA", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "control", "role": "WDATA" } },
	{ "name": "s_axi_control_WSTRB", "direction": "in", "datatype": "sc_lv", "bitwidth":4, "type": "signal", "bundle":{"name": "control", "role": "WSTRB" } },
	{ "name": "s_axi_control_ARADDR", "direction": "in", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "control", "role": "ARADDR" },"address":[{"name":"parallel_gpu","role":"start","value":"0","valid_bit":"0"},{"name":"parallel_gpu","role":"done","value":"0","valid_bit":"1"},{"name":"parallel_gpu","role":"idle","value":"0","valid_bit":"2"},{"name":"parallel_gpu","role":"ready","value":"0","valid_bit":"3"},{"name":"parallel_gpu","role":"auto_start","value":"0","valid_bit":"7"},{"name":"c_0","role":"data","value":"144"}, {"name":"c_0","role":"valid","value":"148","valid_bit":"0"},{"name":"c_1","role":"data","value":"160"}, {"name":"c_1","role":"valid","value":"164","valid_bit":"0"},{"name":"c_2","role":"data","value":"176"}, {"name":"c_2","role":"valid","value":"180","valid_bit":"0"},{"name":"c_3","role":"data","value":"192"}, {"name":"c_3","role":"valid","value":"196","valid_bit":"0"},{"name":"c_4","role":"data","value":"208"}, {"name":"c_4","role":"valid","value":"212","valid_bit":"0"},{"name":"c_5","role":"data","value":"224"}, {"name":"c_5","role":"valid","value":"228","valid_bit":"0"},{"name":"c_6","role":"data","value":"240"}, {"name":"c_6","role":"valid","value":"244","valid_bit":"0"},{"name":"c_7","role":"data","value":"256"}, {"name":"c_7","role":"valid","value":"260","valid_bit":"0"},{"name":"status","role":"data","value":"280"}, {"name":"status","role":"valid","value":"284","valid_bit":"0"}] },
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
	parallel_gpu {
		a_0 {Type I LastRead 0 FirstWrite -1}
		a_1 {Type I LastRead 0 FirstWrite -1}
		a_2 {Type I LastRead 0 FirstWrite -1}
		a_3 {Type I LastRead 0 FirstWrite -1}
		a_4 {Type I LastRead 0 FirstWrite -1}
		a_5 {Type I LastRead 0 FirstWrite -1}
		a_6 {Type I LastRead 0 FirstWrite -1}
		a_7 {Type I LastRead 0 FirstWrite -1}
		b_0 {Type I LastRead 0 FirstWrite -1}
		b_1 {Type I LastRead 0 FirstWrite -1}
		b_2 {Type I LastRead 0 FirstWrite -1}
		b_3 {Type I LastRead 0 FirstWrite -1}
		b_4 {Type I LastRead 0 FirstWrite -1}
		b_5 {Type I LastRead 0 FirstWrite -1}
		b_6 {Type I LastRead 0 FirstWrite -1}
		b_7 {Type I LastRead 0 FirstWrite -1}
		c_0 {Type O LastRead -1 FirstWrite 0}
		c_1 {Type O LastRead -1 FirstWrite 0}
		c_2 {Type O LastRead -1 FirstWrite 0}
		c_3 {Type O LastRead -1 FirstWrite 0}
		c_4 {Type O LastRead -1 FirstWrite 0}
		c_5 {Type O LastRead -1 FirstWrite 0}
		c_6 {Type O LastRead -1 FirstWrite 0}
		c_7 {Type O LastRead -1 FirstWrite 0}
		opcode {Type I LastRead 0 FirstWrite -1}
		status {Type O LastRead -1 FirstWrite 13}}
	parallel_op_rotor_norm {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}}
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
		overflow_out {Type O LastRead -1 FirstWrite 9}}
	parallel_op_clifford_conj {
		c_write {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		c_write_20 {Type I LastRead 0 FirstWrite -1}}
	parallel_op_grade_involution {
		c_write {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		c_write_16 {Type I LastRead 0 FirstWrite -1}
		c_write_17 {Type I LastRead 0 FirstWrite -1}
		c_write_18 {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}}
	parallel_op_reverse_1 {
		c_write {Type I LastRead 0 FirstWrite -1}
		c_write_4 {Type I LastRead 0 FirstWrite -1}
		c_write_5 {Type I LastRead 0 FirstWrite -1}
		c_write_6 {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}}
	parallel_op_grade_proj {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}
		grade_target {Type I LastRead 0 FirstWrite -1}}
	parallel_op_scalar_mul {
		a_0_val {Type I LastRead 0 FirstWrite -1}
		a_1_val {Type I LastRead 0 FirstWrite -1}
		a_2_val {Type I LastRead 0 FirstWrite -1}
		a_3_val {Type I LastRead 0 FirstWrite -1}
		a_4_val {Type I LastRead 0 FirstWrite -1}
		a_5_val {Type I LastRead 0 FirstWrite -1}
		a_6_val {Type I LastRead 0 FirstWrite -1}
		a_7_val {Type I LastRead 0 FirstWrite -1}
		scalar_val {Type I LastRead 0 FirstWrite -1}}
	parallel_op_sub {
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
		b_7_val {Type I LastRead 0 FirstWrite -1}}
	parallel_op_add {
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
		b_7_val {Type I LastRead 0 FirstWrite -1}}
	parallel_product_core_2 {
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
		opcode {Type I LastRead 0 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "1", "Max" : "32"}
	, {"Name" : "Interval", "Min" : "2", "Max" : "33"}
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
