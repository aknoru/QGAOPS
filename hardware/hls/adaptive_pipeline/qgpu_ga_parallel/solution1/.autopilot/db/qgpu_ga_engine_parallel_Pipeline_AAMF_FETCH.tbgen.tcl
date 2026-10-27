set moduleName qgpu_ga_engine_parallel_Pipeline_AAMF_FETCH
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
set C_modelName {qgpu_ga_engine_parallel_Pipeline_AAMF_FETCH}
set C_modelType { void 0 }
set ap_memory_interface_dict [dict create]
dict set ap_memory_interface_dict aamf_bank_a { MEM_WIDTH 32 MEM_SIZE 2048 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 1 }
dict set ap_memory_interface_dict aamf_bank_b { MEM_WIDTH 32 MEM_SIZE 2048 MASTER_TYPE BRAM_CTRL MEM_ADDRESS_MODE WORD_ADDRESS PACKAGE_IO port READ_LATENCY 1 }
set C_modelArgList {
	{ base_addr int 9 regular  }
	{ p_out int 32 regular {pointer 1}  }
	{ p_out1 int 32 regular {pointer 1}  }
	{ p_out2 int 32 regular {pointer 1}  }
	{ p_out3 int 32 regular {pointer 1}  }
	{ p_out4 int 32 regular {pointer 1}  }
	{ p_out5 int 32 regular {pointer 1}  }
	{ p_out6 int 32 regular {pointer 1}  }
	{ p_out7 int 32 regular {pointer 1}  }
	{ p_out8 int 32 regular {pointer 1}  }
	{ p_out9 int 32 regular {pointer 1}  }
	{ p_out10 int 32 regular {pointer 1}  }
	{ p_out11 int 32 regular {pointer 1}  }
	{ p_out12 int 32 regular {pointer 1}  }
	{ p_out13 int 32 regular {pointer 1}  }
	{ p_out14 int 32 regular {pointer 1}  }
	{ p_out15 int 32 regular {pointer 1}  }
	{ p_out16 int 32 regular {pointer 1}  }
	{ aamf_bank_a int 32 regular {array 512 { 1 3 } 1 1 } {global 0}  }
	{ aamf_bank_b int 32 regular {array 512 { 1 3 } 1 1 } {global 0}  }
}
set hasAXIMCache 0
set l_AXIML2Cache [list]
set AXIMCacheInstDict [dict create]
set C_modelArgMapList {[ 
	{ "Name" : "base_addr", "interface" : "wire", "bitwidth" : 9, "direction" : "READONLY"} , 
 	{ "Name" : "p_out", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out1", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out2", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out3", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out4", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out5", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out6", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out7", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out8", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out9", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out10", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out11", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out12", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out13", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out14", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out15", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "p_out16", "interface" : "wire", "bitwidth" : 32, "direction" : "WRITEONLY"} , 
 	{ "Name" : "aamf_bank_a", "interface" : "memory", "bitwidth" : 32, "direction" : "READONLY", "extern" : 0} , 
 	{ "Name" : "aamf_bank_b", "interface" : "memory", "bitwidth" : 32, "direction" : "READONLY", "extern" : 0} ]}
# RTL Port declarations: 
set portNum 47
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ base_addr sc_in sc_lv 9 signal 0 } 
	{ p_out sc_out sc_lv 32 signal 1 } 
	{ p_out_ap_vld sc_out sc_logic 1 outvld 1 } 
	{ p_out1 sc_out sc_lv 32 signal 2 } 
	{ p_out1_ap_vld sc_out sc_logic 1 outvld 2 } 
	{ p_out2 sc_out sc_lv 32 signal 3 } 
	{ p_out2_ap_vld sc_out sc_logic 1 outvld 3 } 
	{ p_out3 sc_out sc_lv 32 signal 4 } 
	{ p_out3_ap_vld sc_out sc_logic 1 outvld 4 } 
	{ p_out4 sc_out sc_lv 32 signal 5 } 
	{ p_out4_ap_vld sc_out sc_logic 1 outvld 5 } 
	{ p_out5 sc_out sc_lv 32 signal 6 } 
	{ p_out5_ap_vld sc_out sc_logic 1 outvld 6 } 
	{ p_out6 sc_out sc_lv 32 signal 7 } 
	{ p_out6_ap_vld sc_out sc_logic 1 outvld 7 } 
	{ p_out7 sc_out sc_lv 32 signal 8 } 
	{ p_out7_ap_vld sc_out sc_logic 1 outvld 8 } 
	{ p_out8 sc_out sc_lv 32 signal 9 } 
	{ p_out8_ap_vld sc_out sc_logic 1 outvld 9 } 
	{ p_out9 sc_out sc_lv 32 signal 10 } 
	{ p_out9_ap_vld sc_out sc_logic 1 outvld 10 } 
	{ p_out10 sc_out sc_lv 32 signal 11 } 
	{ p_out10_ap_vld sc_out sc_logic 1 outvld 11 } 
	{ p_out11 sc_out sc_lv 32 signal 12 } 
	{ p_out11_ap_vld sc_out sc_logic 1 outvld 12 } 
	{ p_out12 sc_out sc_lv 32 signal 13 } 
	{ p_out12_ap_vld sc_out sc_logic 1 outvld 13 } 
	{ p_out13 sc_out sc_lv 32 signal 14 } 
	{ p_out13_ap_vld sc_out sc_logic 1 outvld 14 } 
	{ p_out14 sc_out sc_lv 32 signal 15 } 
	{ p_out14_ap_vld sc_out sc_logic 1 outvld 15 } 
	{ p_out15 sc_out sc_lv 32 signal 16 } 
	{ p_out15_ap_vld sc_out sc_logic 1 outvld 16 } 
	{ p_out16 sc_out sc_lv 32 signal 17 } 
	{ p_out16_ap_vld sc_out sc_logic 1 outvld 17 } 
	{ aamf_bank_a_address0 sc_out sc_lv 9 signal 18 } 
	{ aamf_bank_a_ce0 sc_out sc_logic 1 signal 18 } 
	{ aamf_bank_a_q0 sc_in sc_lv 32 signal 18 } 
	{ aamf_bank_b_address0 sc_out sc_lv 9 signal 19 } 
	{ aamf_bank_b_ce0 sc_out sc_logic 1 signal 19 } 
	{ aamf_bank_b_q0 sc_in sc_lv 32 signal 19 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "base_addr", "direction": "in", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "base_addr", "role": "default" }} , 
 	{ "name": "p_out", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out", "role": "default" }} , 
 	{ "name": "p_out_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out", "role": "ap_vld" }} , 
 	{ "name": "p_out1", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out1", "role": "default" }} , 
 	{ "name": "p_out1_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out1", "role": "ap_vld" }} , 
 	{ "name": "p_out2", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out2", "role": "default" }} , 
 	{ "name": "p_out2_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out2", "role": "ap_vld" }} , 
 	{ "name": "p_out3", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out3", "role": "default" }} , 
 	{ "name": "p_out3_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out3", "role": "ap_vld" }} , 
 	{ "name": "p_out4", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out4", "role": "default" }} , 
 	{ "name": "p_out4_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out4", "role": "ap_vld" }} , 
 	{ "name": "p_out5", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out5", "role": "default" }} , 
 	{ "name": "p_out5_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out5", "role": "ap_vld" }} , 
 	{ "name": "p_out6", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out6", "role": "default" }} , 
 	{ "name": "p_out6_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out6", "role": "ap_vld" }} , 
 	{ "name": "p_out7", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out7", "role": "default" }} , 
 	{ "name": "p_out7_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out7", "role": "ap_vld" }} , 
 	{ "name": "p_out8", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out8", "role": "default" }} , 
 	{ "name": "p_out8_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out8", "role": "ap_vld" }} , 
 	{ "name": "p_out9", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out9", "role": "default" }} , 
 	{ "name": "p_out9_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out9", "role": "ap_vld" }} , 
 	{ "name": "p_out10", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out10", "role": "default" }} , 
 	{ "name": "p_out10_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out10", "role": "ap_vld" }} , 
 	{ "name": "p_out11", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out11", "role": "default" }} , 
 	{ "name": "p_out11_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out11", "role": "ap_vld" }} , 
 	{ "name": "p_out12", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out12", "role": "default" }} , 
 	{ "name": "p_out12_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out12", "role": "ap_vld" }} , 
 	{ "name": "p_out13", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out13", "role": "default" }} , 
 	{ "name": "p_out13_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out13", "role": "ap_vld" }} , 
 	{ "name": "p_out14", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out14", "role": "default" }} , 
 	{ "name": "p_out14_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out14", "role": "ap_vld" }} , 
 	{ "name": "p_out15", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out15", "role": "default" }} , 
 	{ "name": "p_out15_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out15", "role": "ap_vld" }} , 
 	{ "name": "p_out16", "direction": "out", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "p_out16", "role": "default" }} , 
 	{ "name": "p_out16_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "p_out16", "role": "ap_vld" }} , 
 	{ "name": "aamf_bank_a_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "aamf_bank_a", "role": "address0" }} , 
 	{ "name": "aamf_bank_a_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_bank_a", "role": "ce0" }} , 
 	{ "name": "aamf_bank_a_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "aamf_bank_a", "role": "q0" }} , 
 	{ "name": "aamf_bank_b_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "aamf_bank_b", "role": "address0" }} , 
 	{ "name": "aamf_bank_b_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "aamf_bank_b", "role": "ce0" }} , 
 	{ "name": "aamf_bank_b_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "aamf_bank_b", "role": "q0" }}  ]}

set ArgLastReadFirstWriteLatency {
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
		aamf_bank_b {Type I LastRead 0 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "10", "Max" : "10"}
	, {"Name" : "Interval", "Min" : "9", "Max" : "9"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
]}

set Spec2ImplPortList { 
	base_addr { ap_none {  { base_addr in_data 0 9 } } }
	p_out { ap_vld {  { p_out out_data 1 32 }  { p_out_ap_vld out_vld 1 1 } } }
	p_out1 { ap_vld {  { p_out1 out_data 1 32 }  { p_out1_ap_vld out_vld 1 1 } } }
	p_out2 { ap_vld {  { p_out2 out_data 1 32 }  { p_out2_ap_vld out_vld 1 1 } } }
	p_out3 { ap_vld {  { p_out3 out_data 1 32 }  { p_out3_ap_vld out_vld 1 1 } } }
	p_out4 { ap_vld {  { p_out4 out_data 1 32 }  { p_out4_ap_vld out_vld 1 1 } } }
	p_out5 { ap_vld {  { p_out5 out_data 1 32 }  { p_out5_ap_vld out_vld 1 1 } } }
	p_out6 { ap_vld {  { p_out6 out_data 1 32 }  { p_out6_ap_vld out_vld 1 1 } } }
	p_out7 { ap_vld {  { p_out7 out_data 1 32 }  { p_out7_ap_vld out_vld 1 1 } } }
	p_out8 { ap_vld {  { p_out8 out_data 1 32 }  { p_out8_ap_vld out_vld 1 1 } } }
	p_out9 { ap_vld {  { p_out9 out_data 1 32 }  { p_out9_ap_vld out_vld 1 1 } } }
	p_out10 { ap_vld {  { p_out10 out_data 1 32 }  { p_out10_ap_vld out_vld 1 1 } } }
	p_out11 { ap_vld {  { p_out11 out_data 1 32 }  { p_out11_ap_vld out_vld 1 1 } } }
	p_out12 { ap_vld {  { p_out12 out_data 1 32 }  { p_out12_ap_vld out_vld 1 1 } } }
	p_out13 { ap_vld {  { p_out13 out_data 1 32 }  { p_out13_ap_vld out_vld 1 1 } } }
	p_out14 { ap_vld {  { p_out14 out_data 1 32 }  { p_out14_ap_vld out_vld 1 1 } } }
	p_out15 { ap_vld {  { p_out15 out_data 1 32 }  { p_out15_ap_vld out_vld 1 1 } } }
	p_out16 { ap_vld {  { p_out16 out_data 1 32 }  { p_out16_ap_vld out_vld 1 1 } } }
	aamf_bank_a { ap_memory {  { aamf_bank_a_address0 mem_address 1 9 }  { aamf_bank_a_ce0 mem_ce 1 1 }  { aamf_bank_a_q0 mem_dout 0 32 } } }
	aamf_bank_b { ap_memory {  { aamf_bank_b_address0 mem_address 1 9 }  { aamf_bank_b_ce0 mem_ce 1 1 }  { aamf_bank_b_q0 mem_dout 0 32 } } }
}
