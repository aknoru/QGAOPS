set SynModuleInfo {
  {SRCNAME seq_op_rotor_norm_Pipeline_NORM_LOOP MODELNAME seq_op_rotor_norm_Pipeline_NORM_LOOP RTLNAME seq_gpu_seq_op_rotor_norm_Pipeline_NORM_LOOP
    SUBMODULES {
      {MODELNAME seq_gpu_flow_control_loop_pipe_sequential_init RTLNAME seq_gpu_flow_control_loop_pipe_sequential_init BINDTYPE interface TYPE internal_upc_flow_control INSTNAME seq_gpu_flow_control_loop_pipe_sequential_init_U}
    }
  }
  {SRCNAME seq_op_rotor_norm_Pipeline_CLEAR_REMAINING MODELNAME seq_op_rotor_norm_Pipeline_CLEAR_REMAINING RTLNAME seq_gpu_seq_op_rotor_norm_Pipeline_CLEAR_REMAINING}
  {SRCNAME seq_op_rotor_norm MODELNAME seq_op_rotor_norm RTLNAME seq_gpu_seq_op_rotor_norm
    SUBMODULES {
      {MODELNAME seq_gpu_sparsemux_7_2_52_1_1 RTLNAME seq_gpu_sparsemux_7_2_52_1_1 BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
    }
  }
  {SRCNAME seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP MODELNAME seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP RTLNAME seq_gpu_seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP
    SUBMODULES {
      {MODELNAME seq_gpu_sparsemux_17_3_2_1_1 RTLNAME seq_gpu_sparsemux_17_3_2_1_1 BINDTYPE op TYPE sparsemux IMPL compactencoding_dontcare}
      {MODELNAME seq_gpu_sparsemux_7_2_3_1_1 RTLNAME seq_gpu_sparsemux_7_2_3_1_1 BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
      {MODELNAME seq_gpu_sparsemux_5_8_3_1_1 RTLNAME seq_gpu_sparsemux_5_8_3_1_1 BINDTYPE op TYPE sparsemux IMPL compactencoding_realdef}
      {MODELNAME seq_gpu_sparsemux_17_3_67_1_1 RTLNAME seq_gpu_sparsemux_17_3_67_1_1 BINDTYPE op TYPE sparsemux IMPL compactencoding_dontcare}
      {MODELNAME seq_gpu_seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP_BASIS_MASKS_ROM_AUTO_1R RTLNAME seq_gpu_seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP_BASIS_MASKS_ROM_AUTO_1R BINDTYPE storage TYPE rom IMPL auto LATENCY 2 ALLOW_PRAGMA 1}
    }
  }
  {SRCNAME seq_product_core_Pipeline_RESCALE_LOOP MODELNAME seq_product_core_Pipeline_RESCALE_LOOP RTLNAME seq_gpu_seq_product_core_Pipeline_RESCALE_LOOP
    SUBMODULES {
      {MODELNAME seq_gpu_sparsemux_7_2_52_1_1_x RTLNAME seq_gpu_sparsemux_7_2_52_1_1_x BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
    }
  }
  {SRCNAME seq_product_core MODELNAME seq_product_core RTLNAME seq_gpu_seq_product_core}
  {SRCNAME seq_op_reverse MODELNAME seq_op_reverse RTLNAME seq_gpu_seq_op_reverse}
  {SRCNAME seq_op_sandwich MODELNAME seq_op_sandwich RTLNAME seq_gpu_seq_op_sandwich
    SUBMODULES {
      {MODELNAME seq_gpu_seq_op_sandwich_temp_RAM_1P_AUTO_1R1W RTLNAME seq_gpu_seq_op_sandwich_temp_RAM_1P_AUTO_1R1W BINDTYPE storage TYPE ram_1p IMPL auto LATENCY 2 ALLOW_PRAGMA 1}
    }
  }
  {SRCNAME seq_op_clifford_conj MODELNAME seq_op_clifford_conj RTLNAME seq_gpu_seq_op_clifford_conj}
  {SRCNAME seq_op_grade_involution MODELNAME seq_op_grade_involution RTLNAME seq_gpu_seq_op_grade_involution
    SUBMODULES {
      {MODELNAME seq_gpu_sparsemux_17_3_1_1_1 RTLNAME seq_gpu_sparsemux_17_3_1_1_1 BINDTYPE op TYPE sparsemux IMPL compactencoding_dontcare}
    }
  }
  {SRCNAME seq_op_grade_proj MODELNAME seq_op_grade_proj RTLNAME seq_gpu_seq_op_grade_proj}
  {SRCNAME seq_op_scalar_mul MODELNAME seq_op_scalar_mul RTLNAME seq_gpu_seq_op_scalar_mul
    SUBMODULES {
      {MODELNAME seq_gpu_sparsemux_7_2_49_1_1 RTLNAME seq_gpu_sparsemux_7_2_49_1_1 BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
    }
  }
  {SRCNAME seq_op_sub MODELNAME seq_op_sub RTLNAME seq_gpu_seq_op_sub}
  {SRCNAME seq_op_add MODELNAME seq_op_add RTLNAME seq_gpu_seq_op_add}
  {SRCNAME seq_gpu_Pipeline_CLEAR_ERR MODELNAME seq_gpu_Pipeline_CLEAR_ERR RTLNAME seq_gpu_seq_gpu_Pipeline_CLEAR_ERR}
  {SRCNAME seq_gpu MODELNAME seq_gpu RTLNAME seq_gpu IS_TOP 1
    SUBMODULES {
      {MODELNAME seq_gpu_mul_32s_32s_64_2_1 RTLNAME seq_gpu_mul_32s_32s_64_2_1 BINDTYPE op TYPE mul IMPL auto LATENCY 1 ALLOW_PRAGMA 1}
      {MODELNAME seq_gpu_control_s_axi RTLNAME seq_gpu_control_s_axi BINDTYPE interface TYPE interface_s_axilite}
    }
  }
}
