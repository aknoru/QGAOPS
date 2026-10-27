set moduleName ga_op_geometric_product
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
set C_modelName {ga_op_geometric_product}
set C_modelType { int 257 }
set ap_memory_interface_dict [dict create]
set C_modelArgList {
	{ a_0_val1 int 32 regular  }
	{ a_1_val2 int 32 regular  }
	{ a_2_val3 int 32 regular  }
	{ a_3_val4 int 32 regular  }
	{ a_4_val5 int 32 regular  }
	{ a_5_val6 int 32 regular  }
	{ a_6_val7 int 32 regular  }
	{ a_7_val8 int 32 regular  }
	{ b_0_val9 int 32 regular  }
	{ b_1_val10 int 32 regular  }
	{ b_2_val11 int 32 regular  }
	{ b_3_val12 int 32 regular  }
	{ b_4_val13 int 32 regular  }
	{ b_5_val14 int 32 regular  }
	{ b_6_val15 int 32 regular  }
	{ b_7_val16 int 32 regular  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "a_0_val1", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_1_val2", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_2_val3", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_3_val4", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_4_val5", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_5_val6", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_6_val7", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "a_7_val8", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_0_val9", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_1_val10", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_2_val11", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_3_val12", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_4_val13", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_5_val14", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_6_val15", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "b_7_val16", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "ap_return", "interface" : "wire", "bitwidth" : 257} ]}
# RTL Port declarations: 
set portNum 63
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ a_0_val1 sc_in sc_lv 32 signal 0 } 
	{ a_1_val2 sc_in sc_lv 32 signal 1 } 
	{ a_2_val3 sc_in sc_lv 32 signal 2 } 
	{ a_3_val4 sc_in sc_lv 32 signal 3 } 
	{ a_4_val5 sc_in sc_lv 32 signal 4 } 
	{ a_5_val6 sc_in sc_lv 32 signal 5 } 
	{ a_6_val7 sc_in sc_lv 32 signal 6 } 
	{ a_7_val8 sc_in sc_lv 32 signal 7 } 
	{ b_0_val9 sc_in sc_lv 32 signal 8 } 
	{ b_1_val10 sc_in sc_lv 32 signal 9 } 
	{ b_2_val11 sc_in sc_lv 32 signal 10 } 
	{ b_3_val12 sc_in sc_lv 32 signal 11 } 
	{ b_4_val13 sc_in sc_lv 32 signal 12 } 
	{ b_5_val14 sc_in sc_lv 32 signal 13 } 
	{ b_6_val15 sc_in sc_lv 32 signal 14 } 
	{ b_7_val16 sc_in sc_lv 32 signal 15 } 
	{ ap_return_0 sc_out sc_lv 32 signal -1 } 
	{ ap_return_1 sc_out sc_lv 32 signal -1 } 
	{ ap_return_2 sc_out sc_lv 32 signal -1 } 
	{ ap_return_3 sc_out sc_lv 32 signal -1 } 
	{ ap_return_4 sc_out sc_lv 32 signal -1 } 
	{ ap_return_5 sc_out sc_lv 32 signal -1 } 
	{ ap_return_6 sc_out sc_lv 32 signal -1 } 
	{ ap_return_7 sc_out sc_lv 32 signal -1 } 
	{ ap_return_8 sc_out sc_lv 1 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din1 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din2 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din3 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din4 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din5 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din6 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din7 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din8 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din9 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din10 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din11 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din12 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din13 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din14 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din15 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din16 sc_out sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din17 sc_out sc_lv 2 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_din18 sc_out sc_lv 1 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_opcode sc_out sc_lv 1 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_dout0_0 sc_in sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_dout0_1 sc_in sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_dout0_2 sc_in sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_dout0_3 sc_in sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_dout0_4 sc_in sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_dout0_5 sc_in sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_dout0_6 sc_in sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_dout0_7 sc_in sc_lv 32 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_dout0_8 sc_in sc_lv 1 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_start sc_out sc_logic 1 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_ready sc_in sc_logic 1 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_done sc_in sc_logic 1 signal -1 } 
	{ grp_compute_gp_core_fu_2391_p_idle sc_in sc_logic 1 signal -1 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "a_0_val1", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_0_val1", "role": "default" }} , 
 	{ "name": "a_1_val2", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_1_val2", "role": "default" }} , 
 	{ "name": "a_2_val3", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_2_val3", "role": "default" }} , 
 	{ "name": "a_3_val4", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_3_val4", "role": "default" }} , 
 	{ "name": "a_4_val5", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_4_val5", "role": "default" }} , 
 	{ "name": "a_5_val6", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_5_val6", "role": "default" }} , 
 	{ "name": "a_6_val7", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_6_val7", "role": "default" }} , 
 	{ "name": "a_7_val8", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "a_7_val8", "role": "default" }} , 
 	{ "name": "b_0_val9", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_0_val9", "role": "default" }} , 
 	{ "name": "b_1_val10", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_1_val10", "role": "default" }} , 
 	{ "name": "b_2_val11", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_2_val11", "role": "default" }} , 
 	{ "name": "b_3_val12", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_3_val12", "role": "default" }} , 
 	{ "name": "b_4_val13", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_4_val13", "role": "default" }} , 
 	{ "name": "b_5_val14", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_5_val14", "role": "default" }} , 
 	{ "name": "b_6_val15", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_6_val15", "role": "default" }} , 
 	{ "name": "b_7_val16", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "b_7_val16", "role": "default" }} , 
 	{ "name": "ap_return_0", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_0", "role": "default" }} , 
 	{ "name": "ap_return_1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_1", "role": "default" }} , 
 	{ "name": "ap_return_2", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_2", "role": "default" }} , 
 	{ "name": "ap_return_3", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_3", "role": "default" }} , 
 	{ "name": "ap_return_4", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_4", "role": "default" }} , 
 	{ "name": "ap_return_5", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_5", "role": "default" }} , 
 	{ "name": "ap_return_6", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_6", "role": "default" }} , 
 	{ "name": "ap_return_7", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "ap_return_7", "role": "default" }} , 
 	{ "name": "ap_return_8", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "ap_return_8", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din1", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din2", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din2", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din3", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din3", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din4", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din4", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din5", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din5", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din6", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din6", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din7", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din7", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din8", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din8", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din9", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din9", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din10", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din10", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din11", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din11", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din12", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din12", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din13", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din13", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din14", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din14", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din15", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din15", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din16", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din16", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din17", "direction": "out", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din17", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_din18", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_din18", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_opcode", "direction": "out", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_opcode", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_dout0_0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_dout0_0", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_dout0_1", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_dout0_1", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_dout0_2", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_dout0_2", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_dout0_3", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_dout0_3", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_dout0_4", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_dout0_4", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_dout0_5", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_dout0_5", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_dout0_6", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_dout0_6", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_dout0_7", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_dout0_7", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_dout0_8", "direction": "in", "datatype": "sc_lv", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_dout0_8", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_start", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_start", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_ready", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_ready", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_done", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_done", "role": "default" }} , 
 	{ "name": "grp_compute_gp_core_fu_2391_p_idle", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "grp_compute_gp_core_fu_2391_p_idle", "role": "default" }}  ]}

set ArgLastReadFirstWriteLatency {
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
		BASIS_MASKS {Type I LastRead -1 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "51", "Max" : "51"}
	, {"Name" : "Interval", "Min" : "51", "Max" : "51"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	a_0_val1 { ap_none {  { a_0_val1 in_data 0 32 } } }
	a_1_val2 { ap_none {  { a_1_val2 in_data 0 32 } } }
	a_2_val3 { ap_none {  { a_2_val3 in_data 0 32 } } }
	a_3_val4 { ap_none {  { a_3_val4 in_data 0 32 } } }
	a_4_val5 { ap_none {  { a_4_val5 in_data 0 32 } } }
	a_5_val6 { ap_none {  { a_5_val6 in_data 0 32 } } }
	a_6_val7 { ap_none {  { a_6_val7 in_data 0 32 } } }
	a_7_val8 { ap_none {  { a_7_val8 in_data 0 32 } } }
	b_0_val9 { ap_none {  { b_0_val9 in_data 0 32 } } }
	b_1_val10 { ap_none {  { b_1_val10 in_data 0 32 } } }
	b_2_val11 { ap_none {  { b_2_val11 in_data 0 32 } } }
	b_3_val12 { ap_none {  { b_3_val12 in_data 0 32 } } }
	b_4_val13 { ap_none {  { b_4_val13 in_data 0 32 } } }
	b_5_val14 { ap_none {  { b_5_val14 in_data 0 32 } } }
	b_6_val15 { ap_none {  { b_6_val15 in_data 0 32 } } }
	b_7_val16 { ap_none {  { b_7_val16 in_data 0 32 } } }
}
