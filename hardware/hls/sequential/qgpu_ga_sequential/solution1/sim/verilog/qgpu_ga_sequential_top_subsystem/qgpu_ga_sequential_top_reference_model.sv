//==============================================================
//Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
//Tool Version Limit: 2025.11
//Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
//Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
//
//==============================================================

`ifndef QGPU_GA_SEQUENTIAL_TOP_REFERENCE_MODEL_SV
`define QGPU_GA_SEQUENTIAL_TOP_REFERENCE_MODEL_SV

class qgpu_ga_sequential_top_reference_model extends uvm_component;
`define TV_IN_a "../tv/cdatafile/c.qgpu_ga_sequential_top.autotvin_a.dat"
`define TV_OUT_a ""
`define TV_IN_b "../tv/cdatafile/c.qgpu_ga_sequential_top.autotvin_b.dat"
`define TV_OUT_b ""
`define TV_IN_c ""
`define TV_OUT_c "../tv/rtldatafile/rtl.qgpu_ga_sequential_top.autotvout_c.dat"
`define TV_IN_opcode "../tv/cdatafile/c.qgpu_ga_sequential_top.autotvin_opcode.dat"
`define TV_OUT_opcode ""
`define TV_IN_status ""
`define TV_OUT_status "../tv/rtldatafile/rtl.qgpu_ga_sequential_top.autotvout_status.dat"
    bit  read_data_finish_control;
    bit  write_data_finish_control;
    event allaxilite_read_data_finish;
    event allaxilite_read_one_transaction_finish;
    event allaxilite_write_data_finish;
    event allaxilite_write_one_transaction_finish;
    event write_start_finish;
    int trans_num_total = 285;
    int trans_num_idx;
    int ap_done_cnt=1;
    event dut2tb_ap_ready;
    event dut2tb_ap_done;
    event ap_ready_for_nexttrans;
    event ap_done_for_nexttrans;
    event finish;
    qgpu_ga_sequential_top_config qgpu_ga_sequential_top_cfg;
    virtual interface misc_interface misc_if;

    mem_model_pages#(32,8) mem_blk_pages_control_a;
    mem_model_pages#(32,8) mem_blk_pages_control_b;
    mem_model_pages#(32,8) mem_blk_pages_control_c;
    mem_model_pages#(32,8) mem_blk_pages_control_opcode;
    mem_model_pages#(32,8) mem_blk_pages_control_status;
    
    `uvm_component_utils_begin(qgpu_ga_sequential_top_reference_model)
        `uvm_field_int (trans_num_idx, UVM_DEFAULT)
    `uvm_component_utils_end

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        if(!uvm_config_db#(virtual misc_interface)::get(this, "", "misc_if", misc_if))
            `uvm_fatal(this.get_full_name(), "No misc_if from high level")
    endfunction

    function new (string name = "", uvm_component parent = null);
        super.new (name, parent);
        trans_num_idx= 0;
    endfunction

    virtual task run_phase(uvm_phase phase);
        string fpath[$];
misc_if.dut2tb_ap_done = 0;

        fpath.push_back(`TV_IN_a);
        mem_blk_pages_control_a = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_a");
        mem_blk_pages_control_a.set_binary(1);
        mem_blk_pages_control_a.tvinload_pagechk_atinit(fpath, 8*((32+7)/8), 0, 32);
        fpath.delete;


        fpath.push_back(`TV_IN_b);
        mem_blk_pages_control_b = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_b");
        mem_blk_pages_control_b.set_binary(1);
        mem_blk_pages_control_b.tvinload_pagechk_atinit(fpath, 8*((32+7)/8), 0, 64);
        fpath.delete;


        mem_blk_pages_control_c = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_c");
        mem_blk_pages_control_c.set_binary(1);
        mem_blk_pages_control_c.init_pages(trans_num_total, 8*((32+7)/8), 96);
        mem_blk_pages_control_c.tvoutdump_atinit(`TV_OUT_c);


        fpath.push_back(`TV_IN_opcode);
        mem_blk_pages_control_opcode = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_opcode");
        mem_blk_pages_control_opcode.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 16);
        fpath.delete;


        mem_blk_pages_control_status = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_status");
        mem_blk_pages_control_status.init_pages(trans_num_total, 1*((32+7)/8), 128);
        mem_blk_pages_control_status.tvoutdump_atinit(`TV_OUT_status);

        fork
            forever begin
                wait(write_data_finish_control);
                `uvm_info("", "trigger_allaxilite_data_write_finish", UVM_LOW)
                @(posedge misc_if.clock);
                write_data_finish_control = 0;
                -> allaxilite_write_data_finish;
            end
            forever begin
                wait(read_data_finish_control);
                `uvm_info("", "trigger_allaxilite_data_read_finish", UVM_LOW)
                @(posedge misc_if.clock);
                read_data_finish_control = 0;
                -> allaxilite_read_data_finish;
            end
            forever begin
                //this is non-pipeline case
                forever begin
                    @(negedge misc_if.clock);
                    if(misc_if.dut2tb_ap_done===1) break;
                end
                @(posedge misc_if.clock);
                @allaxilite_read_data_finish;
                @(posedge misc_if.clock);
                @allaxilite_write_data_finish;
                @(posedge misc_if.clock);
                -> ap_ready_for_nexttrans;
                `uvm_info(this.get_full_name(), "trigger event ap_ready_for_nexttrans", UVM_LOW)
                fork
                    begin
                        misc_if.ap_ready_for_nexttrans = 1;
                        @(posedge misc_if.clock);
                        misc_if.ap_ready_for_nexttrans = 0;
                    end
                join_none
            end
            forever begin
                forever begin
                    @(negedge misc_if.clock);
                    if(misc_if.dut2tb_ap_done===1) break;
                end
                @(posedge misc_if.clock);
                fork
                    begin
                        @(negedge misc_if.clock);
                        -> misc_if.dut2tb_ap_done_evt;
                        #0;
                        -> misc_if.dut2tb_ap_ready_evt;
                    end
                join_none
                @allaxilite_read_data_finish;
                @(posedge misc_if.clock);
                -> ap_done_for_nexttrans;
                `uvm_info(this.get_full_name(), "trigger event ap_done_for_nexttrans", UVM_LOW)
                fork
                    begin
                        misc_if.ap_done_for_nexttrans = 1;
                        @(posedge misc_if.clock);
                        misc_if.ap_done_for_nexttrans = 0;
                    end
                join_none
            end

            forever begin
                forever begin
                    @(negedge misc_if.clock);
                    if (misc_if.dut2tb_ap_ready === 1)   break;
                end
                @(posedge misc_if.clock);
                `uvm_info(this.get_full_name(), "trigger event DUT2TB_AP_READY", UVM_LOW)
                -> dut2tb_ap_ready;
                 misc_if.tb2dut_ap_start = 0;
            end
            forever begin
                forever begin
                    @(negedge misc_if.clock);
                    if (misc_if.dut2tb_ap_done_kernel === 1)   break;
                end
                @(posedge misc_if.clock);
                fork
                    begin
                        @(negedge misc_if.clock);
                        `uvm_info(this.get_full_name(), "trigger event dut2tb_ap_done_kernel_evt", UVM_LOW)
                        -> misc_if.dut2tb_ap_done_kernel_evt;
                    end
                join_none
            end
        join
    endtask

    virtual function void write_axi_wtr_control(axi_pkg::axi_transfer tr);
        if(tr.addr == 0 && tr.len == 0 && tr.data[0][0]==1) begin //addr 0 and bit 0 are parameter
            -> write_start_finish;
            misc_if.tb2dut_ap_start = 1;
        end
    endfunction
    virtual function void write_axi_rtr_control(axi_pkg::axi_transfer tr);
            `uvm_info("receive axi read data", tr.sprint(), UVM_HIGH)
        if(tr.addr == 0 && tr.len == 0) begin
            if(tr.data[0][1]==1) begin  //bit 1 is parameter
                `uvm_info("status polling", "ap_done is polled", UVM_LOW);
                fork
                    begin
                        misc_if.dut2tb_ap_done = 1;
                        @(posedge misc_if.clock);
                        #0;
                        misc_if.dut2tb_ap_done = 0;
                        misc_if.tb2dut_ap_continue = 0;
                        -> dut2tb_ap_done;
                    end
                join_none
            end
            begin
                misc_if.dut2tb_ap_idle = tr.data[0][2];
            end
        end else begin
            mem_blk_pages_control_c.write_elems_frontpage(tr.data, tr.byte_addr);
            mem_blk_pages_control_status.write_elems_frontpage(tr.data, tr.byte_addr);
        end
    endfunction
endclass
`endif
