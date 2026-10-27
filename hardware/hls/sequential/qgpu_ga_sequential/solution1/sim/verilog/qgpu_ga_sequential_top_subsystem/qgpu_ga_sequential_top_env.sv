//==============================================================
//Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2025.2 (64-bit)
//Tool Version Limit: 2025.11
//Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
//Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
//
//==============================================================
`ifndef QGPU_GA_SEQUENTIAL_TOP_ENV__SV                                                                                   
    `define QGPU_GA_SEQUENTIAL_TOP_ENV__SV                                                                               
                                                                                                                    
                                                                                                                    
    class qgpu_ga_sequential_top_env extends uvm_env;                                                                          
                                                                                                                    
        qgpu_ga_sequential_top_virtual_sequencer qgpu_ga_sequential_top_virtual_sqr;                                                      
        qgpu_ga_sequential_top_config qgpu_ga_sequential_top_cfg;                                                                         
                                                                                                                    
        axi_pkg::axi_env#(8,4,4,3,1) axi_lite_control;
                                                                                                                    
        qgpu_ga_sequential_top_reference_model   refm;                                                                         
                                                                                                                    
        qgpu_ga_sequential_top_subsystem_monitor subsys_mon;                                                                   
                                                                                                                    
        `uvm_component_utils_begin(qgpu_ga_sequential_top_env)                                                                 
        `uvm_field_object (refm, UVM_DEFAULT | UVM_REFERENCE)                                                       
        `uvm_field_object (qgpu_ga_sequential_top_virtual_sqr, UVM_DEFAULT | UVM_REFERENCE)                                    
        `uvm_field_object (qgpu_ga_sequential_top_cfg        , UVM_DEFAULT)                                                    
        `uvm_component_utils_end                                                                                    
                                                                                                                    
        function new (string name = "qgpu_ga_sequential_top_env", uvm_component parent = null);                              
            super.new(name, parent);                                                                                
        endfunction                                                                                                 
                                                                                                                    
        extern virtual function void build_phase(uvm_phase phase);                                                  
        extern virtual function void connect_phase(uvm_phase phase);                                                
        extern virtual task          run_phase(uvm_phase phase);                                                    
                                                                                                                    
    endclass                                                                                                        
                                                                                                                    
    function void qgpu_ga_sequential_top_env::build_phase(uvm_phase phase);                                                    
        super.build_phase(phase);                                                                                   
        qgpu_ga_sequential_top_cfg = qgpu_ga_sequential_top_config::type_id::create("qgpu_ga_sequential_top_cfg", this);                           
                                                                                                                    

        qgpu_ga_sequential_top_cfg.control_cfg.set_default();
        qgpu_ga_sequential_top_cfg.control_cfg.drv_type = axi_pkg::MASTER;
        qgpu_ga_sequential_top_cfg.control_cfg.reset_level = axi_pkg::RESET_LEVEL_LOW;
        uvm_config_db#(axi_pkg::axi_cfg)::set(this, "axi_lite_control*", "cfg", qgpu_ga_sequential_top_cfg.control_cfg);
        axi_lite_control = axi_pkg::axi_env#(8,4,4,3,1)::type_id::create("axi_lite_control", this);



        refm = qgpu_ga_sequential_top_reference_model::type_id::create("refm", this);


        uvm_config_db#(qgpu_ga_sequential_top_reference_model)::set(this, "*", "refm", refm);


        `uvm_info(this.get_full_name(), "set reference model by uvm_config_db", UVM_LOW)


        subsys_mon = qgpu_ga_sequential_top_subsystem_monitor::type_id::create("subsys_mon", this);


        qgpu_ga_sequential_top_virtual_sqr = qgpu_ga_sequential_top_virtual_sequencer::type_id::create("qgpu_ga_sequential_top_virtual_sqr", this);
        `uvm_info(this.get_full_name(), "build_phase done", UVM_LOW)
    endfunction


    function void qgpu_ga_sequential_top_env::connect_phase(uvm_phase phase);
        super.connect_phase(phase);


        if(qgpu_ga_sequential_top_cfg.control_cfg.drv_type==axi_pkg::MASTER ||qgpu_ga_sequential_top_cfg.control_cfg.drv_type==axi_pkg::SLAVE)
            qgpu_ga_sequential_top_virtual_sqr.control_sqr = axi_lite_control.vsqr;
        axi_lite_control.item_wtr_port.connect(subsys_mon.control_wtr_imp);
        axi_lite_control.item_rtr_port.connect(subsys_mon.control_rtr_imp);
        refm.qgpu_ga_sequential_top_cfg = qgpu_ga_sequential_top_cfg;
        `uvm_info(this.get_full_name(), "connect phase done", UVM_LOW)
    endfunction


    task qgpu_ga_sequential_top_env::run_phase(uvm_phase phase);
        `uvm_info(this.get_full_name(), "qgpu_ga_sequential_top_env is running", UVM_LOW)
    endtask


`endif
