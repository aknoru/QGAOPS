//==============================================================
//Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
//Tool Version Limit: 2025.11
//Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
//Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
//
//==============================================================
`timescale 1ns/1ps 

`ifndef QGPU_GA_SEQUENTIAL_TOP_SUBSYSTEM_PKG__SV          
    `define QGPU_GA_SEQUENTIAL_TOP_SUBSYSTEM_PKG__SV      
                                                     
    package qgpu_ga_sequential_top_subsystem_pkg;               
                                                     
        import uvm_pkg::*;                           
        import file_agent_pkg::*;                    
        import axi_pkg::*;
                                                     
        `include "uvm_macros.svh"                  
                                                     
        `include "qgpu_ga_sequential_top_config.sv"           
        `include "qgpu_ga_sequential_top_reference_model.sv"  
        `include "qgpu_ga_sequential_top_scoreboard.sv"       
        `include "qgpu_ga_sequential_top_subsystem_monitor.sv"
        `include "qgpu_ga_sequential_top_virtual_sequencer.sv"
        `include "qgpu_ga_sequential_top_pkg_sequence_lib.sv" 
        `include "qgpu_ga_sequential_top_env.sv"              
                                                     
    endpackage                                       
                                                     
`endif                                               
