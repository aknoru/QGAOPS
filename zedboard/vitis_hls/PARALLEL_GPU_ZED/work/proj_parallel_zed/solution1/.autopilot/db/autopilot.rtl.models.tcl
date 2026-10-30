set SynModuleInfo {
  {SRCNAME parallel_op_rotor_norm MODELNAME parallel_op_rotor_norm RTLNAME parallel_gpu_parallel_op_rotor_norm
    SUBMODULES {
      {MODELNAME parallel_gpu_sparsemux_7_2_52_1_1 RTLNAME parallel_gpu_sparsemux_7_2_52_1_1 BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
    }
  }
  {SRCNAME parallel_product_core MODELNAME parallel_product_core RTLNAME parallel_gpu_parallel_product_core
    SUBMODULES {
      {MODELNAME parallel_gpu_sparsemux_7_2_52_1_1_x RTLNAME parallel_gpu_sparsemux_7_2_52_1_1_x BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
      {MODELNAME parallel_gpu_sparsemux_7_2_51_1_1 RTLNAME parallel_gpu_sparsemux_7_2_51_1_1 BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
    }
  }
  {SRCNAME parallel_op_reverse MODELNAME parallel_op_reverse RTLNAME parallel_gpu_parallel_op_reverse}
  {SRCNAME parallel_product_core.3 MODELNAME parallel_product_core_3 RTLNAME parallel_gpu_parallel_product_core_3}
  {SRCNAME parallel_op_sandwich MODELNAME parallel_op_sandwich RTLNAME parallel_gpu_parallel_op_sandwich
    SUBMODULES {
      {MODELNAME parallel_gpu_fifo_w32_d3_S RTLNAME parallel_gpu_fifo_w32_d3_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME temp_U}
      {MODELNAME parallel_gpu_fifo_w32_d3_S RTLNAME parallel_gpu_fifo_w32_d3_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME temp_1_U}
      {MODELNAME parallel_gpu_fifo_w32_d3_S RTLNAME parallel_gpu_fifo_w32_d3_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME temp_2_U}
      {MODELNAME parallel_gpu_fifo_w32_d3_S RTLNAME parallel_gpu_fifo_w32_d3_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME temp_3_U}
      {MODELNAME parallel_gpu_fifo_w32_d3_S RTLNAME parallel_gpu_fifo_w32_d3_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME temp_4_U}
      {MODELNAME parallel_gpu_fifo_w32_d3_S RTLNAME parallel_gpu_fifo_w32_d3_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME temp_5_U}
      {MODELNAME parallel_gpu_fifo_w32_d3_S RTLNAME parallel_gpu_fifo_w32_d3_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME temp_6_U}
      {MODELNAME parallel_gpu_fifo_w32_d3_S RTLNAME parallel_gpu_fifo_w32_d3_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME temp_7_U}
      {MODELNAME parallel_gpu_fifo_w1_d2_S RTLNAME parallel_gpu_fifo_w1_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME overflow_in_out_tmp_channel_U}
      {MODELNAME parallel_gpu_fifo_w32_d2_S RTLNAME parallel_gpu_fifo_w32_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME a_rev_U}
      {MODELNAME parallel_gpu_fifo_w32_d2_S RTLNAME parallel_gpu_fifo_w32_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME a_rev_1_U}
      {MODELNAME parallel_gpu_fifo_w32_d2_S RTLNAME parallel_gpu_fifo_w32_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME a_rev_2_U}
      {MODELNAME parallel_gpu_fifo_w32_d2_S RTLNAME parallel_gpu_fifo_w32_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME a_rev_3_U}
      {MODELNAME parallel_gpu_fifo_w32_d2_S RTLNAME parallel_gpu_fifo_w32_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME a_rev_4_U}
      {MODELNAME parallel_gpu_fifo_w32_d2_S RTLNAME parallel_gpu_fifo_w32_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME a_rev_5_U}
      {MODELNAME parallel_gpu_fifo_w32_d2_S RTLNAME parallel_gpu_fifo_w32_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME a_rev_6_U}
      {MODELNAME parallel_gpu_fifo_w32_d2_S RTLNAME parallel_gpu_fifo_w32_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME a_rev_7_U}
      {MODELNAME parallel_gpu_fifo_w1_d2_S RTLNAME parallel_gpu_fifo_w1_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME overflow_in_out_tmp1_channel_U}
    }
  }
  {SRCNAME parallel_op_clifford_conj MODELNAME parallel_op_clifford_conj RTLNAME parallel_gpu_parallel_op_clifford_conj}
  {SRCNAME parallel_op_grade_involution MODELNAME parallel_op_grade_involution RTLNAME parallel_gpu_parallel_op_grade_involution}
  {SRCNAME parallel_op_reverse.1 MODELNAME parallel_op_reverse_1 RTLNAME parallel_gpu_parallel_op_reverse_1}
  {SRCNAME parallel_op_grade_proj MODELNAME parallel_op_grade_proj RTLNAME parallel_gpu_parallel_op_grade_proj}
  {SRCNAME parallel_op_scalar_mul MODELNAME parallel_op_scalar_mul RTLNAME parallel_gpu_parallel_op_scalar_mul
    SUBMODULES {
      {MODELNAME parallel_gpu_sparsemux_7_2_49_1_1 RTLNAME parallel_gpu_sparsemux_7_2_49_1_1 BINDTYPE op TYPE sparsemux IMPL onehotencoding_realdef}
    }
  }
  {SRCNAME parallel_op_sub MODELNAME parallel_op_sub RTLNAME parallel_gpu_parallel_op_sub}
  {SRCNAME parallel_op_add MODELNAME parallel_op_add RTLNAME parallel_gpu_parallel_op_add}
  {SRCNAME parallel_product_core.2 MODELNAME parallel_product_core_2 RTLNAME parallel_gpu_parallel_product_core_2}
  {SRCNAME parallel_gpu MODELNAME parallel_gpu RTLNAME parallel_gpu IS_TOP 1
    SUBMODULES {
      {MODELNAME parallel_gpu_mul_32s_32s_64_2_1 RTLNAME parallel_gpu_mul_32s_32s_64_2_1 BINDTYPE op TYPE mul IMPL auto LATENCY 1 ALLOW_PRAGMA 1}
      {MODELNAME parallel_gpu_control_s_axi RTLNAME parallel_gpu_control_s_axi BINDTYPE interface TYPE interface_s_axilite}
    }
  }
}
