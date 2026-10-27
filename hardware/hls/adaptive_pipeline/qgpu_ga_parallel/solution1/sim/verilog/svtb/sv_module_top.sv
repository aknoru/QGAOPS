//==============================================================
//Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
//Tool Version Limit: 2025.11
//Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
//Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
//
//==============================================================

`ifndef SV_MODULE_TOP_SV
`define SV_MODULE_TOP_SV


`timescale 1ns/1ps


`include "uvm_macros.svh"
import uvm_pkg::*;
import file_agent_pkg::*;
import qgpu_ga_parallel_top_subsystem_pkg::*;
`include "qgpu_ga_parallel_top_subsys_test_sequence_lib.sv"
`include "qgpu_ga_parallel_top_test_lib.sv"


module sv_module_top;


    misc_interface              misc_if ( .clock(apatb_qgpu_ga_parallel_top_top.AESL_clock), .reset(apatb_qgpu_ga_parallel_top_top.AESL_reset) );
    assign misc_if.dut2tb_ap_ready = apatb_qgpu_ga_parallel_top_top.AESL_inst_qgpu_ga_parallel_top.ap_ready;
    assign misc_if.dut2tb_ap_done_kernel = apatb_qgpu_ga_parallel_top_top.AESL_inst_qgpu_ga_parallel_top.ap_done;
    initial begin
        uvm_config_db #(virtual misc_interface)::set(null, "uvm_test_top.top_env.*", "misc_if", misc_if);
    end


    axi_if #(9,4,4,3,1)  axi_control_if (.clk  (apatb_qgpu_ga_parallel_top_top.AESL_clock), .rst(apatb_qgpu_ga_parallel_top_top.AESL_reset));
    assign apatb_qgpu_ga_parallel_top_top.control_AWADDR = axi_control_if.AWADDR;
    assign apatb_qgpu_ga_parallel_top_top.control_AWVALID = axi_control_if.AWVALID;
    assign axi_control_if.AWREADY = apatb_qgpu_ga_parallel_top_top.control_AWREADY;
    assign apatb_qgpu_ga_parallel_top_top.control_WVALID = axi_control_if.WVALID;
    assign axi_control_if.WREADY = apatb_qgpu_ga_parallel_top_top.control_WREADY;
    assign apatb_qgpu_ga_parallel_top_top.control_WDATA = axi_control_if.WDATA;
    assign apatb_qgpu_ga_parallel_top_top.control_WSTRB = axi_control_if.WSTRB;
    assign apatb_qgpu_ga_parallel_top_top.control_ARADDR = axi_control_if.ARADDR;
    assign apatb_qgpu_ga_parallel_top_top.control_ARVALID = axi_control_if.ARVALID;
    assign axi_control_if.ARREADY = apatb_qgpu_ga_parallel_top_top.control_ARREADY;
    assign axi_control_if.RVALID = apatb_qgpu_ga_parallel_top_top.control_RVALID;
    assign apatb_qgpu_ga_parallel_top_top.control_RREADY = axi_control_if.RREADY;
    assign axi_control_if.RDATA = apatb_qgpu_ga_parallel_top_top.control_RDATA;
    assign axi_control_if.RRESP = apatb_qgpu_ga_parallel_top_top.control_RRESP;
    assign axi_control_if.BVALID = apatb_qgpu_ga_parallel_top_top.control_BVALID;
    assign apatb_qgpu_ga_parallel_top_top.control_BREADY = axi_control_if.BREADY;
    assign axi_control_if.BRESP = apatb_qgpu_ga_parallel_top_top.control_BRESP;
    assign axi_control_if.BID = 0;
    assign axi_control_if.RID = 0;
    assign axi_control_if.RLAST = 1;
    initial begin
        uvm_config_db #( virtual axi_if#(9,4,4,3,1) )::set(null, "uvm_test_top.top_env.axi_lite_control.*", "vif", axi_control_if);
    end


    initial begin
        run_test();
    end
endmodule
`endif
