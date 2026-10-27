//==============================================================
//Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
//Tool Version Limit: 2025.11
//Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
//Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
//
//==============================================================
`ifndef QGPU_GA_PARALLEL_TOP_SCOREBOARD__SV                                                       
    `define QGPU_GA_PARALLEL_TOP_SCOREBOARD__SV                                                   
                                                                                               
                                                                                               
    class qgpu_ga_parallel_top_scoreboard extends uvm_component;                                        
                                                                                               
        qgpu_ga_parallel_top_reference_model refm;                                                      
                                                                                               
                                                                                               
        `uvm_component_utils_begin(qgpu_ga_parallel_top_scoreboard)                                     
        `uvm_field_object(refm  , UVM_DEFAULT)                                                 
        `uvm_component_utils_end                                                               
                                                                                               
        virtual function void build_phase(uvm_phase phase);                                    
            if (!uvm_config_db #(qgpu_ga_parallel_top_reference_model)::get(this, "", "refm", refm))
                `uvm_fatal(this.get_full_name(), "No refm from high level")                  
            `uvm_info(this.get_full_name(), "get reference model by uvm_config_db", UVM_MEDIUM) 
                                                                                               
        endfunction                                                                            
                                                                                               
        function new (string name = "", uvm_component parent = null);                        
            super.new(name, parent);                                                           
        endfunction                                                                            
                                                                                               
        virtual task run_phase(uvm_phase phase);                                               

            fork                                                                               
                forever begin
                    @refm.allaxilite_write_data_finish;
                    `uvm_info(this.get_full_name(), "receive allaxilite_write_finish axilite write_mem_page_process", UVM_LOW)
                    void'(refm.mem_blk_pages_control_a_0.pages.pop_front());
                    void'(refm.mem_blk_pages_control_a_1.pages.pop_front());
                    void'(refm.mem_blk_pages_control_a_2.pages.pop_front());
                    void'(refm.mem_blk_pages_control_a_3.pages.pop_front());
                    void'(refm.mem_blk_pages_control_a_4.pages.pop_front());
                    void'(refm.mem_blk_pages_control_a_5.pages.pop_front());
                    void'(refm.mem_blk_pages_control_a_6.pages.pop_front());
                    void'(refm.mem_blk_pages_control_a_7.pages.pop_front());
                    void'(refm.mem_blk_pages_control_b_0.pages.pop_front());
                    void'(refm.mem_blk_pages_control_b_1.pages.pop_front());
                    void'(refm.mem_blk_pages_control_b_2.pages.pop_front());
                    void'(refm.mem_blk_pages_control_b_3.pages.pop_front());
                    void'(refm.mem_blk_pages_control_b_4.pages.pop_front());
                    void'(refm.mem_blk_pages_control_b_5.pages.pop_front());
                    void'(refm.mem_blk_pages_control_b_6.pages.pop_front());
                    void'(refm.mem_blk_pages_control_b_7.pages.pop_front());
                    void'(refm.mem_blk_pages_control_opcode.pages.pop_front());
                end
                forever begin
                    @refm.allaxilite_read_data_finish;
                    `uvm_info(this.get_full_name(), "receive allaxilite_read_finish axilite_read_mem_page_process", UVM_LOW)
                    refm.mem_blk_pages_control_c_0.tvout_dump_frontpage(1);
                    refm.mem_blk_pages_control_c_1.tvout_dump_frontpage(1);
                    refm.mem_blk_pages_control_c_2.tvout_dump_frontpage(1);
                    refm.mem_blk_pages_control_c_3.tvout_dump_frontpage(1);
                    refm.mem_blk_pages_control_c_4.tvout_dump_frontpage(1);
                    refm.mem_blk_pages_control_c_5.tvout_dump_frontpage(1);
                    refm.mem_blk_pages_control_c_6.tvout_dump_frontpage(1);
                    refm.mem_blk_pages_control_c_7.tvout_dump_frontpage(1);
                    refm.mem_blk_pages_control_status.tvout_dump_frontpage(1);
                end
                                                                                               
                forever begin
                    @refm.dut2tb_ap_done;
                    `uvm_info(this.get_full_name(), "receive dut2tb_ap_done and do axim dump", UVM_LOW)
                end                                                                            
                begin                                                                          
                    @refm.finish;                                                              
                    `uvm_info(this.get_full_name(), "receive FINISH", UVM_LOW)               
                end                                                                            
            join                                                                               
        endtask                                                                                
                                                                                               
        virtual function void write_axi_wtr_control(axi_pkg::axi_transfer tr);
        endfunction

        virtual function void write_axi_rtr_control(axi_pkg::axi_transfer tr);
        endfunction

    endclass                                                                                   
                                                                                               
`endif                                                                                         
