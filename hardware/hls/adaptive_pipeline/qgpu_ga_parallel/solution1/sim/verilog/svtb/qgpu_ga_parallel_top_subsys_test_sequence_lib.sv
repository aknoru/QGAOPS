//==============================================================
//Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
//Tool Version Limit: 2025.11
//Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
//Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
//
//==============================================================
`ifndef QGPU_GA_PARALLEL_TOP_SUBSYS_TEST_SEQUENCE_LIB__SV                                              
    `define QGPU_GA_PARALLEL_TOP_SUBSYS_TEST_SEQUENCE_LIB__SV                                          
                                                                                                    
                                                                                                    
    `include "uvm_macros.svh"                                                                     
                                                                                                    
    class qgpu_ga_parallel_top_subsys_test_sequence_lib extends uvm_sequence;                                
                                                                                                    
        function new (string name = "qgpu_ga_parallel_top_subsys_test_sequence_lib");                      
            super.new(name);                                                                        
            `uvm_info(this.get_full_name(), "new is called", UVM_LOW)                             
        endfunction                                                                                 
                                                                                                    
        `uvm_object_utils(qgpu_ga_parallel_top_subsys_test_sequence_lib)                                     
        `uvm_declare_p_sequencer(qgpu_ga_parallel_top_virtual_sequencer)                                     
                                                                                                    
        virtual task body();                                                                        
            uvm_phase starting_phase;                                                               
            virtual interface misc_interface misc_if;                                               
            qgpu_ga_parallel_top_reference_model refm;                                                       
                                                                                                    
            axi_pkg::axi_busdatas_master_sequence#(9, 32) axi_master_wr_control_seq;
            axi_pkg::axi_busdatas_master_sequence#(9, 32) axi_master_rd_control_seq;
            axi_pkg::axi_busdatas_master_sequence#(9, 32) axi_master_poll_control_seq;

            if (!uvm_config_db#(qgpu_ga_parallel_top_reference_model)::get(p_sequencer,"", "refm", refm))
                `uvm_fatal(this.get_full_name(), "No reference model")
            `uvm_info(this.get_full_name(), "get reference model by uvm_config_db", UVM_LOW)

            `uvm_info(this.get_full_name(), "body is called", UVM_LOW)
            starting_phase = this.get_starting_phase();
            if (starting_phase != null) begin
                `uvm_info(this.get_full_name(), "starting_phase not null", UVM_LOW)
                starting_phase.raise_objection(this);
            end
            else
                `uvm_info(this.get_full_name(), "starting_phase null" , UVM_LOW)

            misc_if = refm.misc_if;


            //phase_done.set_drain_time(this, 0ns);
            wait(refm.misc_if.reset === 1);
            ->refm.misc_if.initialed_evt;

            fork
                begin
                    fork
                        begin
                            int control_page_idx_bak;
                            `uvm_create_on(axi_master_wr_control_seq, p_sequencer.control_sqr);
                            axi_master_wr_control_seq.misc_if = refm.misc_if;
                            axi_master_wr_control_seq.ap_done    = refm.ap_done_for_nexttrans   ;
                            axi_master_wr_control_seq.ap_ready   = refm.ap_ready_for_nexttrans  ;
                            axi_master_wr_control_seq.finish     = refm.finish ;
                            axi_master_wr_control_seq.isusr_delay = axi_pkg::NO_DELAY;
                            for(int i=0; i<285; i++) begin
                                logic[63:0] data64bit_a_0[$];
                                logic[32-1:0] databusbit_a_0[$];
                                logic[63:0] data64bit_a_1[$];
                                logic[32-1:0] databusbit_a_1[$];
                                logic[63:0] data64bit_a_2[$];
                                logic[32-1:0] databusbit_a_2[$];
                                logic[63:0] data64bit_a_3[$];
                                logic[32-1:0] databusbit_a_3[$];
                                logic[63:0] data64bit_a_4[$];
                                logic[32-1:0] databusbit_a_4[$];
                                logic[63:0] data64bit_a_5[$];
                                logic[32-1:0] databusbit_a_5[$];
                                logic[63:0] data64bit_a_6[$];
                                logic[32-1:0] databusbit_a_6[$];
                                logic[63:0] data64bit_a_7[$];
                                logic[32-1:0] databusbit_a_7[$];
                                logic[63:0] data64bit_b_0[$];
                                logic[32-1:0] databusbit_b_0[$];
                                logic[63:0] data64bit_b_1[$];
                                logic[32-1:0] databusbit_b_1[$];
                                logic[63:0] data64bit_b_2[$];
                                logic[32-1:0] databusbit_b_2[$];
                                logic[63:0] data64bit_b_3[$];
                                logic[32-1:0] databusbit_b_3[$];
                                logic[63:0] data64bit_b_4[$];
                                logic[32-1:0] databusbit_b_4[$];
                                logic[63:0] data64bit_b_5[$];
                                logic[32-1:0] databusbit_b_5[$];
                                logic[63:0] data64bit_b_6[$];
                                logic[32-1:0] databusbit_b_6[$];
                                logic[63:0] data64bit_b_7[$];
                                logic[32-1:0] databusbit_b_7[$];
                                logic[63:0] data64bit_opcode[$];
                                logic[32-1:0] databusbit_opcode[$];
                                data64bit_a_0.delete(); databusbit_a_0.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_a_0.tobusdata(data64bit_a_0, refm.mem_blk_pages_control_a_0.rd_page_idx, 32);
                                foreach(data64bit_a_0[s]) databusbit_a_0[s]=data64bit_a_0[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_a_0, 0, 16, 1);
                                data64bit_a_1.delete(); databusbit_a_1.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_a_1.tobusdata(data64bit_a_1, refm.mem_blk_pages_control_a_1.rd_page_idx, 32);
                                foreach(data64bit_a_1[s]) databusbit_a_1[s]=data64bit_a_1[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_a_1, 0, 24, 1);
                                data64bit_a_2.delete(); databusbit_a_2.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_a_2.tobusdata(data64bit_a_2, refm.mem_blk_pages_control_a_2.rd_page_idx, 32);
                                foreach(data64bit_a_2[s]) databusbit_a_2[s]=data64bit_a_2[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_a_2, 0, 32, 1);
                                data64bit_a_3.delete(); databusbit_a_3.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_a_3.tobusdata(data64bit_a_3, refm.mem_blk_pages_control_a_3.rd_page_idx, 32);
                                foreach(data64bit_a_3[s]) databusbit_a_3[s]=data64bit_a_3[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_a_3, 0, 40, 1);
                                data64bit_a_4.delete(); databusbit_a_4.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_a_4.tobusdata(data64bit_a_4, refm.mem_blk_pages_control_a_4.rd_page_idx, 32);
                                foreach(data64bit_a_4[s]) databusbit_a_4[s]=data64bit_a_4[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_a_4, 0, 48, 1);
                                data64bit_a_5.delete(); databusbit_a_5.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_a_5.tobusdata(data64bit_a_5, refm.mem_blk_pages_control_a_5.rd_page_idx, 32);
                                foreach(data64bit_a_5[s]) databusbit_a_5[s]=data64bit_a_5[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_a_5, 0, 56, 1);
                                data64bit_a_6.delete(); databusbit_a_6.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_a_6.tobusdata(data64bit_a_6, refm.mem_blk_pages_control_a_6.rd_page_idx, 32);
                                foreach(data64bit_a_6[s]) databusbit_a_6[s]=data64bit_a_6[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_a_6, 0, 64, 1);
                                data64bit_a_7.delete(); databusbit_a_7.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_a_7.tobusdata(data64bit_a_7, refm.mem_blk_pages_control_a_7.rd_page_idx, 32);
                                foreach(data64bit_a_7[s]) databusbit_a_7[s]=data64bit_a_7[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_a_7, 0, 72, 1);
                                data64bit_b_0.delete(); databusbit_b_0.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_b_0.tobusdata(data64bit_b_0, refm.mem_blk_pages_control_b_0.rd_page_idx, 32);
                                foreach(data64bit_b_0[s]) databusbit_b_0[s]=data64bit_b_0[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_b_0, 0, 80, 1);
                                data64bit_b_1.delete(); databusbit_b_1.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_b_1.tobusdata(data64bit_b_1, refm.mem_blk_pages_control_b_1.rd_page_idx, 32);
                                foreach(data64bit_b_1[s]) databusbit_b_1[s]=data64bit_b_1[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_b_1, 0, 88, 1);
                                data64bit_b_2.delete(); databusbit_b_2.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_b_2.tobusdata(data64bit_b_2, refm.mem_blk_pages_control_b_2.rd_page_idx, 32);
                                foreach(data64bit_b_2[s]) databusbit_b_2[s]=data64bit_b_2[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_b_2, 0, 96, 1);
                                data64bit_b_3.delete(); databusbit_b_3.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_b_3.tobusdata(data64bit_b_3, refm.mem_blk_pages_control_b_3.rd_page_idx, 32);
                                foreach(data64bit_b_3[s]) databusbit_b_3[s]=data64bit_b_3[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_b_3, 0, 104, 1);
                                data64bit_b_4.delete(); databusbit_b_4.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_b_4.tobusdata(data64bit_b_4, refm.mem_blk_pages_control_b_4.rd_page_idx, 32);
                                foreach(data64bit_b_4[s]) databusbit_b_4[s]=data64bit_b_4[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_b_4, 0, 112, 1);
                                data64bit_b_5.delete(); databusbit_b_5.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_b_5.tobusdata(data64bit_b_5, refm.mem_blk_pages_control_b_5.rd_page_idx, 32);
                                foreach(data64bit_b_5[s]) databusbit_b_5[s]=data64bit_b_5[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_b_5, 0, 120, 1);
                                data64bit_b_6.delete(); databusbit_b_6.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_b_6.tobusdata(data64bit_b_6, refm.mem_blk_pages_control_b_6.rd_page_idx, 32);
                                foreach(data64bit_b_6[s]) databusbit_b_6[s]=data64bit_b_6[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_b_6, 0, 128, 1);
                                data64bit_b_7.delete(); databusbit_b_7.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_b_7.tobusdata(data64bit_b_7, refm.mem_blk_pages_control_b_7.rd_page_idx, 32);
                                foreach(data64bit_b_7[s]) databusbit_b_7[s]=data64bit_b_7[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_b_7, 0, 136, 1);
                                data64bit_opcode.delete(); databusbit_opcode.delete();
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=0;
                                refm.mem_blk_pages_control_opcode.tobusdata(data64bit_opcode, refm.mem_blk_pages_control_opcode.rd_page_idx, 32);
                                foreach(data64bit_opcode[s]) databusbit_opcode[s]=data64bit_opcode[s][32-1:0];
                                axi_master_wr_control_seq.StableAxiliteNoUpdate=1;
                                axi_master_wr_control_seq.datamerge_inavg(databusbit_opcode, 0, 272, 1);
                                `uvm_send(axi_master_wr_control_seq);
                                refm.write_data_finish_control = 1;
                                `uvm_info("control data writting thread", $sformatf("%0dth(total 285): waiting for all write data finish event",i), UVM_LOW)
                                wait(refm.allaxilite_write_data_finish.triggered);
                                refm.write_data_finish_control = 0;
                                fork
                                    begin // configure start to enable DUT
                                        axi_master_wr_control_seq.wr_addr_data.push_back( (1<<0)+(0<<32) );
                                        `uvm_info("control start dut by axilite", $sformatf("%0dth(total 285): begin to set start bit",i), UVM_LOW)
                                        `uvm_send(axi_master_wr_control_seq);
                                    end
                                    begin
                                        `uvm_info("control wait for ap_ready for next trans", $sformatf("%0dth(total 285): begin to wait",i), UVM_LOW)
                                        wait(refm.dut2tb_ap_ready.triggered);
                                        wait(refm.ap_done_for_nexttrans.triggered);
                                        #0.01; //make sure mem incr_rd_page_idx is called first
                                    end
                                join
                            end
                        end
                        begin
                            for(int j=0; j<285; j=j+refm.ap_done_cnt) begin
                                wait(misc_if.dut2tb_ap_done_kernel == 1);
                                `uvm_info("test finish control", $sformatf("ap_done of kernel is triggered"), UVM_LOW)
                                @(posedge misc_if.clock);
                                fork
                                    forever begin
                                        `uvm_create_on(axi_master_poll_control_seq, p_sequencer.control_sqr);
                                        axi_master_poll_control_seq.isusr_delay = axi_pkg::NO_DELAY;
                                        axi_master_poll_control_seq.misc_if = refm.misc_if;
                                        axi_master_poll_control_seq.rd_addr.push_back(0);
                                        `uvm_send(axi_master_poll_control_seq)
                                        repeat(2) @(posedge misc_if.clock);
                                    end
                                    begin
                                        `uvm_info("test finish control", $sformatf("%0dth(total 285) ap_done_for_nexttrans begin to wait",j), UVM_LOW)
                                        @refm.dut2tb_ap_done;
                                    end
                                join_any
                                disable fork;
                                wait(refm.ap_ready_for_nexttrans.triggered);
                            end
                        end
                        begin
                            `uvm_create_on(axi_master_rd_control_seq, p_sequencer.control_sqr)
                            axi_master_rd_control_seq.misc_if = refm.misc_if;
                            axi_master_rd_control_seq.ap_done    = refm.ap_done_for_nexttrans   ;
                            axi_master_rd_control_seq.ap_ready   = refm.ap_ready_for_nexttrans  ;
                            axi_master_rd_control_seq.finish     = refm.finish ;
                            axi_master_rd_control_seq.isusr_delay = axi_pkg::NO_DELAY;
                            for(int j=0; j<285; j=j+refm.ap_done_cnt) begin
                                logic[32-1:0] databusbit[$];
                                @refm.dut2tb_ap_done;
                                axi_master_rd_control_seq.datamerge_inavg(databusbit, (1*32+32-1)/32, 144, 0);
                                axi_master_rd_control_seq.datamerge_inavg(databusbit, (1*32+32-1)/32, 160, 0);
                                axi_master_rd_control_seq.datamerge_inavg(databusbit, (1*32+32-1)/32, 176, 0);
                                axi_master_rd_control_seq.datamerge_inavg(databusbit, (1*32+32-1)/32, 192, 0);
                                axi_master_rd_control_seq.datamerge_inavg(databusbit, (1*32+32-1)/32, 208, 0);
                                axi_master_rd_control_seq.datamerge_inavg(databusbit, (1*32+32-1)/32, 224, 0);
                                axi_master_rd_control_seq.datamerge_inavg(databusbit, (1*32+32-1)/32, 240, 0);
                                axi_master_rd_control_seq.datamerge_inavg(databusbit, (1*32+32-1)/32, 256, 0);
                                axi_master_rd_control_seq.datamerge_inavg(databusbit, (1*32+32-1)/32, 280, 0);
                                    `uvm_info("axilite data read", $sformatf("%0dth(total 285) data read sequence is started",j), UVM_LOW)
                                `uvm_send(axi_master_rd_control_seq);
                                @(posedge refm.misc_if.clock); //wait address 2 rdata rsp done
                                @(posedge refm.misc_if.clock);
                                refm.read_data_finish_control = 1;
                                wait(refm.allaxilite_read_data_finish.triggered);
                            end
                        end
                    join
                end

                begin
                    for(int j=0; j<285; j=j+refm.ap_done_cnt) @refm.ap_done_for_nexttrans;
                    `uvm_info(this.get_full_name(), "autotb finished", UVM_LOW)
                    -> refm.finish;
                    refm.misc_if.finished = 1;
                    @(posedge refm.misc_if.clock);
                    refm.misc_if.finished = 0;
                    @(posedge refm.misc_if.clock);
                    -> refm.misc_if.finished_evt;
                end
            join_any
            repeat(5) @(posedge refm.misc_if.clock); //5 cycles delay for finish stuff. 5 is haphazard value

            p_sequencer.control_sqr.stop_sequences();
            disable fork;
                                                                                                    
            starting_phase.drop_objection(this);                                                    
                                                                                                    
        endtask                                                                                     
    endclass                                                                                        
                                                                                                    
`endif                                                                                              
