//==============================================================
//Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
//Tool Version Limit: 2025.11
//Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
//Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
//
//==============================================================

`ifndef QGPU_GA_PARALLEL_TOP_REFERENCE_MODEL_SV
`define QGPU_GA_PARALLEL_TOP_REFERENCE_MODEL_SV

class qgpu_ga_parallel_top_reference_model extends uvm_component;
`define TV_IN_a_0 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_a_0.dat"
`define TV_OUT_a_0 ""
`define TV_IN_a_1 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_a_1.dat"
`define TV_OUT_a_1 ""
`define TV_IN_a_2 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_a_2.dat"
`define TV_OUT_a_2 ""
`define TV_IN_a_3 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_a_3.dat"
`define TV_OUT_a_3 ""
`define TV_IN_a_4 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_a_4.dat"
`define TV_OUT_a_4 ""
`define TV_IN_a_5 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_a_5.dat"
`define TV_OUT_a_5 ""
`define TV_IN_a_6 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_a_6.dat"
`define TV_OUT_a_6 ""
`define TV_IN_a_7 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_a_7.dat"
`define TV_OUT_a_7 ""
`define TV_IN_b_0 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_b_0.dat"
`define TV_OUT_b_0 ""
`define TV_IN_b_1 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_b_1.dat"
`define TV_OUT_b_1 ""
`define TV_IN_b_2 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_b_2.dat"
`define TV_OUT_b_2 ""
`define TV_IN_b_3 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_b_3.dat"
`define TV_OUT_b_3 ""
`define TV_IN_b_4 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_b_4.dat"
`define TV_OUT_b_4 ""
`define TV_IN_b_5 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_b_5.dat"
`define TV_OUT_b_5 ""
`define TV_IN_b_6 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_b_6.dat"
`define TV_OUT_b_6 ""
`define TV_IN_b_7 "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_b_7.dat"
`define TV_OUT_b_7 ""
`define TV_IN_c_0 ""
`define TV_OUT_c_0 "../tv/rtldatafile/rtl.qgpu_ga_parallel_top.autotvout_c_0.dat"
`define TV_IN_c_1 ""
`define TV_OUT_c_1 "../tv/rtldatafile/rtl.qgpu_ga_parallel_top.autotvout_c_1.dat"
`define TV_IN_c_2 ""
`define TV_OUT_c_2 "../tv/rtldatafile/rtl.qgpu_ga_parallel_top.autotvout_c_2.dat"
`define TV_IN_c_3 ""
`define TV_OUT_c_3 "../tv/rtldatafile/rtl.qgpu_ga_parallel_top.autotvout_c_3.dat"
`define TV_IN_c_4 ""
`define TV_OUT_c_4 "../tv/rtldatafile/rtl.qgpu_ga_parallel_top.autotvout_c_4.dat"
`define TV_IN_c_5 ""
`define TV_OUT_c_5 "../tv/rtldatafile/rtl.qgpu_ga_parallel_top.autotvout_c_5.dat"
`define TV_IN_c_6 ""
`define TV_OUT_c_6 "../tv/rtldatafile/rtl.qgpu_ga_parallel_top.autotvout_c_6.dat"
`define TV_IN_c_7 ""
`define TV_OUT_c_7 "../tv/rtldatafile/rtl.qgpu_ga_parallel_top.autotvout_c_7.dat"
`define TV_IN_opcode "../tv/cdatafile/c.qgpu_ga_parallel_top.autotvin_opcode.dat"
`define TV_OUT_opcode ""
`define TV_IN_status ""
`define TV_OUT_status "../tv/rtldatafile/rtl.qgpu_ga_parallel_top.autotvout_status.dat"
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
    qgpu_ga_parallel_top_config qgpu_ga_parallel_top_cfg;
    virtual interface misc_interface misc_if;

    mem_model_pages#(32,8) mem_blk_pages_control_a_0;
    mem_model_pages#(32,8) mem_blk_pages_control_a_1;
    mem_model_pages#(32,8) mem_blk_pages_control_a_2;
    mem_model_pages#(32,8) mem_blk_pages_control_a_3;
    mem_model_pages#(32,8) mem_blk_pages_control_a_4;
    mem_model_pages#(32,8) mem_blk_pages_control_a_5;
    mem_model_pages#(32,8) mem_blk_pages_control_a_6;
    mem_model_pages#(32,8) mem_blk_pages_control_a_7;
    mem_model_pages#(32,8) mem_blk_pages_control_b_0;
    mem_model_pages#(32,8) mem_blk_pages_control_b_1;
    mem_model_pages#(32,8) mem_blk_pages_control_b_2;
    mem_model_pages#(32,8) mem_blk_pages_control_b_3;
    mem_model_pages#(32,8) mem_blk_pages_control_b_4;
    mem_model_pages#(32,8) mem_blk_pages_control_b_5;
    mem_model_pages#(32,8) mem_blk_pages_control_b_6;
    mem_model_pages#(32,8) mem_blk_pages_control_b_7;
    mem_model_pages#(32,8) mem_blk_pages_control_c_0;
    mem_model_pages#(32,8) mem_blk_pages_control_c_1;
    mem_model_pages#(32,8) mem_blk_pages_control_c_2;
    mem_model_pages#(32,8) mem_blk_pages_control_c_3;
    mem_model_pages#(32,8) mem_blk_pages_control_c_4;
    mem_model_pages#(32,8) mem_blk_pages_control_c_5;
    mem_model_pages#(32,8) mem_blk_pages_control_c_6;
    mem_model_pages#(32,8) mem_blk_pages_control_c_7;
    mem_model_pages#(32,8) mem_blk_pages_control_opcode;
    mem_model_pages#(32,8) mem_blk_pages_control_status;
    
    `uvm_component_utils_begin(qgpu_ga_parallel_top_reference_model)
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

        fpath.push_back(`TV_IN_a_0);
        mem_blk_pages_control_a_0 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_a_0");
        mem_blk_pages_control_a_0.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 16);
        fpath.delete;


        fpath.push_back(`TV_IN_a_1);
        mem_blk_pages_control_a_1 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_a_1");
        mem_blk_pages_control_a_1.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 24);
        fpath.delete;


        fpath.push_back(`TV_IN_a_2);
        mem_blk_pages_control_a_2 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_a_2");
        mem_blk_pages_control_a_2.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 32);
        fpath.delete;


        fpath.push_back(`TV_IN_a_3);
        mem_blk_pages_control_a_3 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_a_3");
        mem_blk_pages_control_a_3.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 40);
        fpath.delete;


        fpath.push_back(`TV_IN_a_4);
        mem_blk_pages_control_a_4 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_a_4");
        mem_blk_pages_control_a_4.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 48);
        fpath.delete;


        fpath.push_back(`TV_IN_a_5);
        mem_blk_pages_control_a_5 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_a_5");
        mem_blk_pages_control_a_5.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 56);
        fpath.delete;


        fpath.push_back(`TV_IN_a_6);
        mem_blk_pages_control_a_6 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_a_6");
        mem_blk_pages_control_a_6.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 64);
        fpath.delete;


        fpath.push_back(`TV_IN_a_7);
        mem_blk_pages_control_a_7 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_a_7");
        mem_blk_pages_control_a_7.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 72);
        fpath.delete;


        fpath.push_back(`TV_IN_b_0);
        mem_blk_pages_control_b_0 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_b_0");
        mem_blk_pages_control_b_0.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 80);
        fpath.delete;


        fpath.push_back(`TV_IN_b_1);
        mem_blk_pages_control_b_1 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_b_1");
        mem_blk_pages_control_b_1.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 88);
        fpath.delete;


        fpath.push_back(`TV_IN_b_2);
        mem_blk_pages_control_b_2 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_b_2");
        mem_blk_pages_control_b_2.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 96);
        fpath.delete;


        fpath.push_back(`TV_IN_b_3);
        mem_blk_pages_control_b_3 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_b_3");
        mem_blk_pages_control_b_3.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 104);
        fpath.delete;


        fpath.push_back(`TV_IN_b_4);
        mem_blk_pages_control_b_4 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_b_4");
        mem_blk_pages_control_b_4.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 112);
        fpath.delete;


        fpath.push_back(`TV_IN_b_5);
        mem_blk_pages_control_b_5 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_b_5");
        mem_blk_pages_control_b_5.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 120);
        fpath.delete;


        fpath.push_back(`TV_IN_b_6);
        mem_blk_pages_control_b_6 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_b_6");
        mem_blk_pages_control_b_6.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 128);
        fpath.delete;


        fpath.push_back(`TV_IN_b_7);
        mem_blk_pages_control_b_7 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_b_7");
        mem_blk_pages_control_b_7.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 136);
        fpath.delete;


        mem_blk_pages_control_c_0 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_c_0");
        mem_blk_pages_control_c_0.init_pages(trans_num_total, 1*((32+7)/8), 144);
        mem_blk_pages_control_c_0.tvoutdump_atinit(`TV_OUT_c_0);


        mem_blk_pages_control_c_1 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_c_1");
        mem_blk_pages_control_c_1.init_pages(trans_num_total, 1*((32+7)/8), 160);
        mem_blk_pages_control_c_1.tvoutdump_atinit(`TV_OUT_c_1);


        mem_blk_pages_control_c_2 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_c_2");
        mem_blk_pages_control_c_2.init_pages(trans_num_total, 1*((32+7)/8), 176);
        mem_blk_pages_control_c_2.tvoutdump_atinit(`TV_OUT_c_2);


        mem_blk_pages_control_c_3 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_c_3");
        mem_blk_pages_control_c_3.init_pages(trans_num_total, 1*((32+7)/8), 192);
        mem_blk_pages_control_c_3.tvoutdump_atinit(`TV_OUT_c_3);


        mem_blk_pages_control_c_4 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_c_4");
        mem_blk_pages_control_c_4.init_pages(trans_num_total, 1*((32+7)/8), 208);
        mem_blk_pages_control_c_4.tvoutdump_atinit(`TV_OUT_c_4);


        mem_blk_pages_control_c_5 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_c_5");
        mem_blk_pages_control_c_5.init_pages(trans_num_total, 1*((32+7)/8), 224);
        mem_blk_pages_control_c_5.tvoutdump_atinit(`TV_OUT_c_5);


        mem_blk_pages_control_c_6 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_c_6");
        mem_blk_pages_control_c_6.init_pages(trans_num_total, 1*((32+7)/8), 240);
        mem_blk_pages_control_c_6.tvoutdump_atinit(`TV_OUT_c_6);


        mem_blk_pages_control_c_7 = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_c_7");
        mem_blk_pages_control_c_7.init_pages(trans_num_total, 1*((32+7)/8), 256);
        mem_blk_pages_control_c_7.tvoutdump_atinit(`TV_OUT_c_7);


        fpath.push_back(`TV_IN_opcode);
        mem_blk_pages_control_opcode = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_opcode");
        mem_blk_pages_control_opcode.tvinload_pagechk_atinit(fpath, 1*((32+7)/8), 0, 272);
        fpath.delete;


        mem_blk_pages_control_status = mem_model_pages#(32,8)::type_id::create("mem_blk_pages_control_status");
        mem_blk_pages_control_status.init_pages(trans_num_total, 1*((32+7)/8), 280);
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
            mem_blk_pages_control_c_0.write_elems_frontpage(tr.data, tr.byte_addr);
            mem_blk_pages_control_c_1.write_elems_frontpage(tr.data, tr.byte_addr);
            mem_blk_pages_control_c_2.write_elems_frontpage(tr.data, tr.byte_addr);
            mem_blk_pages_control_c_3.write_elems_frontpage(tr.data, tr.byte_addr);
            mem_blk_pages_control_c_4.write_elems_frontpage(tr.data, tr.byte_addr);
            mem_blk_pages_control_c_5.write_elems_frontpage(tr.data, tr.byte_addr);
            mem_blk_pages_control_c_6.write_elems_frontpage(tr.data, tr.byte_addr);
            mem_blk_pages_control_c_7.write_elems_frontpage(tr.data, tr.byte_addr);
            mem_blk_pages_control_status.write_elems_frontpage(tr.data, tr.byte_addr);
        end
    endfunction
endclass
`endif
