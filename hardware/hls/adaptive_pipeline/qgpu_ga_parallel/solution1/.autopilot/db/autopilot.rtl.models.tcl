set SynModuleInfo {
  {SRCNAME qgpu_ga_engine_parallel_Pipeline_AAMF_STAGE_IN MODELNAME qgpu_ga_engine_parallel_Pipeline_AAMF_STAGE_IN RTLNAME qgpu_ga_parallel_top_qgpu_ga_engine_parallel_Pipeline_AAMF_STAGE_IN
    SUBMODULES {
      {MODELNAME qgpu_ga_parallel_top_sparsemux_17_3_32_1_1 RTLNAME qgpu_ga_parallel_top_sparsemux_17_3_32_1_1 BINDTYPE op TYPE sparsemux IMPL compactencoding_dontcare}
      {MODELNAME qgpu_ga_parallel_top_flow_control_loop_pipe_sequential_init RTLNAME qgpu_ga_parallel_top_flow_control_loop_pipe_sequential_init BINDTYPE interface TYPE internal_upc_flow_control INSTNAME qgpu_ga_parallel_top_flow_control_loop_pipe_sequential_init_U}
    }
  }
  {SRCNAME qgpu_ga_engine_parallel_Pipeline_AAMF_FETCH MODELNAME qgpu_ga_engine_parallel_Pipeline_AAMF_FETCH RTLNAME qgpu_ga_parallel_top_qgpu_ga_engine_parallel_Pipeline_AAMF_FETCH}
  {SRCNAME ga_op_rotor_norm MODELNAME ga_op_rotor_norm RTLNAME qgpu_ga_parallel_top_ga_op_rotor_norm
    SUBMODULES {
      {MODELNAME qgpu_ga_parallel_top_mul_32s_32s_64_2_1 RTLNAME qgpu_ga_parallel_top_mul_32s_32s_64_2_1 BINDTYPE op TYPE mul IMPL auto LATENCY 1 ALLOW_PRAGMA 1}
      {MODELNAME qgpu_ga_parallel_top_sparsemux_7_2_52_1_1 RTLNAME qgpu_ga_parallel_top_sparsemux_7_2_52_1_1 BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
    }
  }
  {SRCNAME blade_product_sign MODELNAME blade_product_sign RTLNAME qgpu_ga_parallel_top_blade_product_sign}
  {SRCNAME rescale_and_saturate MODELNAME rescale_and_saturate RTLNAME qgpu_ga_parallel_top_rescale_and_saturate
    SUBMODULES {
      {MODELNAME qgpu_ga_parallel_top_sparsemux_7_2_52_1_1_x RTLNAME qgpu_ga_parallel_top_sparsemux_7_2_52_1_1_x BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
    }
  }
  {SRCNAME compute_gp_core MODELNAME compute_gp_core RTLNAME qgpu_ga_parallel_top_compute_gp_core
    SUBMODULES {
      {MODELNAME qgpu_ga_parallel_top_sparsemux_17_3_2_1_1 RTLNAME qgpu_ga_parallel_top_sparsemux_17_3_2_1_1 BINDTYPE op TYPE sparsemux IMPL compactencoding_dontcare}
      {MODELNAME qgpu_ga_parallel_top_sparsemux_5_8_3_1_1 RTLNAME qgpu_ga_parallel_top_sparsemux_5_8_3_1_1 BINDTYPE op TYPE sparsemux IMPL compactencoding_realdef}
      {MODELNAME qgpu_ga_parallel_top_sparsemux_17_3_67_1_1 RTLNAME qgpu_ga_parallel_top_sparsemux_17_3_67_1_1 BINDTYPE op TYPE sparsemux IMPL compactencoding_dontcare}
      {MODELNAME qgpu_ga_parallel_top_compute_gp_core_BASIS_MASKS_ROM_AUTO_1R RTLNAME qgpu_ga_parallel_top_compute_gp_core_BASIS_MASKS_ROM_AUTO_1R BINDTYPE storage TYPE rom IMPL auto LATENCY 2 ALLOW_PRAGMA 1}
    }
  }
  {SRCNAME ga_op_reverse MODELNAME ga_op_reverse RTLNAME qgpu_ga_parallel_top_ga_op_reverse}
  {SRCNAME ga_op_rotor_sandwich MODELNAME ga_op_rotor_sandwich RTLNAME qgpu_ga_parallel_top_ga_op_rotor_sandwich}
  {SRCNAME ga_op_clifford_conjugation MODELNAME ga_op_clifford_conjugation RTLNAME qgpu_ga_parallel_top_ga_op_clifford_conjugation}
  {SRCNAME ga_op_grade_involution MODELNAME ga_op_grade_involution RTLNAME qgpu_ga_parallel_top_ga_op_grade_involution}
  {SRCNAME ga_op_grade_project MODELNAME ga_op_grade_project RTLNAME qgpu_ga_parallel_top_ga_op_grade_project}
  {SRCNAME ga_op_scalar_mul MODELNAME ga_op_scalar_mul RTLNAME qgpu_ga_parallel_top_ga_op_scalar_mul}
  {SRCNAME ga_op_subtraction MODELNAME ga_op_subtraction RTLNAME qgpu_ga_parallel_top_ga_op_subtraction}
  {SRCNAME ga_op_addition MODELNAME ga_op_addition RTLNAME qgpu_ga_parallel_top_ga_op_addition}
  {SRCNAME ga_op_inner_product MODELNAME ga_op_inner_product RTLNAME qgpu_ga_parallel_top_ga_op_inner_product}
  {SRCNAME ga_op_wedge_product MODELNAME ga_op_wedge_product RTLNAME qgpu_ga_parallel_top_ga_op_wedge_product}
  {SRCNAME ga_op_geometric_product MODELNAME ga_op_geometric_product RTLNAME qgpu_ga_parallel_top_ga_op_geometric_product}
  {SRCNAME qgpu_ga_engine_parallel_Pipeline_AAMF_COMMIT_OUT MODELNAME qgpu_ga_engine_parallel_Pipeline_AAMF_COMMIT_OUT RTLNAME qgpu_ga_parallel_top_qgpu_ga_engine_parallel_Pipeline_AAMF_COMMIT_OUT}
  {SRCNAME qgpu_ga_engine_parallel MODELNAME qgpu_ga_engine_parallel RTLNAME qgpu_ga_parallel_top_qgpu_ga_engine_parallel
    SUBMODULES {
      {MODELNAME qgpu_ga_parallel_top_qgpu_ga_engine_parallel_aamf_bank_a_RAM_2P_BRAM_1R1W RTLNAME qgpu_ga_parallel_top_qgpu_ga_engine_parallel_aamf_bank_a_RAM_2P_BRAM_1R1W BINDTYPE storage TYPE ram_2p IMPL bram LATENCY 2 ALLOW_PRAGMA 1}
    }
  }
  {SRCNAME qgpu_ga_parallel_top MODELNAME qgpu_ga_parallel_top RTLNAME qgpu_ga_parallel_top IS_TOP 1
    SUBMODULES {
      {MODELNAME qgpu_ga_parallel_top_control_s_axi RTLNAME qgpu_ga_parallel_top_control_s_axi BINDTYPE interface TYPE interface_s_axilite}
    }
  }
}
