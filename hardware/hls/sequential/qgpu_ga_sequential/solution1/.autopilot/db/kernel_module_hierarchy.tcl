set ModuleHierarchy {[{
"Name" : "qgpu_ga_sequential_top", "RefName" : "qgpu_ga_sequential_top","ID" : "0","Type" : "sequential",
"SubInsts" : [
	{"Name" : "grp_qgpu_ga_engine_shared_fu_79", "RefName" : "qgpu_ga_engine_shared","ID" : "1","Type" : "sequential",
		"SubInsts" : [
		{"Name" : "grp_qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_287_1_fu_247", "RefName" : "qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_287_1","ID" : "2","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_287_1","RefName" : "VITIS_LOOP_287_1","ID" : "3","Type" : "pipeline"},]},
		{"Name" : "grp_qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_297_2_fu_260", "RefName" : "qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_297_2","ID" : "4","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_297_2","RefName" : "VITIS_LOOP_297_2","ID" : "5","Type" : "pipeline"},]},
		{"Name" : "grp_ga_seq_op_rotor_norm_fu_272", "RefName" : "ga_seq_op_rotor_norm","ID" : "6","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_ga_seq_op_rotor_norm_Pipeline_VITIS_LOOP_255_1_fu_68", "RefName" : "ga_seq_op_rotor_norm_Pipeline_VITIS_LOOP_255_1","ID" : "7","Type" : "sequential",
				"SubLoops" : [
				{"Name" : "VITIS_LOOP_255_1","RefName" : "VITIS_LOOP_255_1","ID" : "8","Type" : "pipeline"},]},
			{"Name" : "grp_ga_seq_op_rotor_norm_Pipeline_VITIS_LOOP_260_2_fu_75", "RefName" : "ga_seq_op_rotor_norm_Pipeline_VITIS_LOOP_260_2","ID" : "9","Type" : "sequential",
				"SubLoops" : [
				{"Name" : "VITIS_LOOP_260_2","RefName" : "VITIS_LOOP_260_2","ID" : "10","Type" : "pipeline"},]},]},
		{"Name" : "grp_ga_seq_op_rotor_sandwich_fu_278", "RefName" : "ga_seq_op_rotor_sandwich","ID" : "11","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_compute_gp_seq_core_fu_26", "RefName" : "compute_gp_seq_core","ID" : "12","Type" : "sequential",
				"SubInsts" : [
				{"Name" : "grp_compute_gp_seq_core_Pipeline_SHARED_OUTER_LOOP_SHARED_INNER_LOOP_fu_74", "RefName" : "compute_gp_seq_core_Pipeline_SHARED_OUTER_LOOP_SHARED_INNER_LOOP","ID" : "13","Type" : "sequential",
					"SubLoops" : [
					{"Name" : "SHARED_OUTER_LOOP_SHARED_INNER_LOOP","RefName" : "SHARED_OUTER_LOOP_SHARED_INNER_LOOP","ID" : "14","Type" : "pipeline"},]},
				{"Name" : "grp_compute_gp_seq_core_Pipeline_RESCALE_LOOP_fu_94", "RefName" : "compute_gp_seq_core_Pipeline_RESCALE_LOOP","ID" : "15","Type" : "sequential",
					"SubLoops" : [
					{"Name" : "RESCALE_LOOP","RefName" : "RESCALE_LOOP","ID" : "16","Type" : "pipeline"},]},]},
			{"Name" : "grp_ga_seq_op_reverse_fu_43", "RefName" : "ga_seq_op_reverse","ID" : "17","Type" : "sequential",
				"SubLoops" : [
				{"Name" : "VITIS_LOOP_189_1","RefName" : "VITIS_LOOP_189_1","ID" : "18","Type" : "pipeline"},]},]},
		{"Name" : "grp_ga_seq_op_clifford_conjugation_fu_287", "RefName" : "ga_seq_op_clifford_conjugation","ID" : "19","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_219_1","RefName" : "VITIS_LOOP_219_1","ID" : "20","Type" : "pipeline"},]},
		{"Name" : "grp_ga_seq_op_grade_involution_fu_293", "RefName" : "ga_seq_op_grade_involution","ID" : "21","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_204_1","RefName" : "VITIS_LOOP_204_1","ID" : "22","Type" : "pipeline"},]},
		{"Name" : "grp_ga_seq_op_reverse_fu_299", "RefName" : "ga_seq_op_reverse","ID" : "23","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_189_1","RefName" : "VITIS_LOOP_189_1","ID" : "24","Type" : "pipeline"},]},
		{"Name" : "grp_ga_seq_op_grade_project_fu_307", "RefName" : "ga_seq_op_grade_project","ID" : "25","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_ga_seq_op_grade_project_Pipeline_VITIS_LOOP_173_1_fu_41", "RefName" : "ga_seq_op_grade_project_Pipeline_VITIS_LOOP_173_1","ID" : "26","Type" : "sequential",
				"SubLoops" : [
				{"Name" : "VITIS_LOOP_173_1","RefName" : "VITIS_LOOP_173_1","ID" : "27","Type" : "pipeline"},]},
			{"Name" : "grp_ga_seq_op_grade_project_Pipeline_VITIS_LOOP_177_2_fu_47", "RefName" : "ga_seq_op_grade_project_Pipeline_VITIS_LOOP_177_2","ID" : "28","Type" : "sequential",
				"SubLoops" : [
				{"Name" : "VITIS_LOOP_177_2","RefName" : "VITIS_LOOP_177_2","ID" : "29","Type" : "pipeline"},]},]},
		{"Name" : "grp_ga_seq_op_scalar_mul_fu_314", "RefName" : "ga_seq_op_scalar_mul","ID" : "30","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_158_1","RefName" : "VITIS_LOOP_158_1","ID" : "31","Type" : "pipeline"},]},
		{"Name" : "grp_ga_seq_op_subtraction_fu_322", "RefName" : "ga_seq_op_subtraction","ID" : "32","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_146_1","RefName" : "VITIS_LOOP_146_1","ID" : "33","Type" : "pipeline"},]},
		{"Name" : "grp_ga_seq_op_addition_fu_329", "RefName" : "ga_seq_op_addition","ID" : "34","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_134_1","RefName" : "VITIS_LOOP_134_1","ID" : "35","Type" : "pipeline"},]},
		{"Name" : "grp_ga_seq_op_inner_product_fu_336", "RefName" : "ga_seq_op_inner_product","ID" : "36","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_compute_gp_seq_core_fu_14", "RefName" : "compute_gp_seq_core","ID" : "37","Type" : "sequential",
				"SubInsts" : [
				{"Name" : "grp_compute_gp_seq_core_Pipeline_SHARED_OUTER_LOOP_SHARED_INNER_LOOP_fu_74", "RefName" : "compute_gp_seq_core_Pipeline_SHARED_OUTER_LOOP_SHARED_INNER_LOOP","ID" : "38","Type" : "sequential",
					"SubLoops" : [
					{"Name" : "SHARED_OUTER_LOOP_SHARED_INNER_LOOP","RefName" : "SHARED_OUTER_LOOP_SHARED_INNER_LOOP","ID" : "39","Type" : "pipeline"},]},
				{"Name" : "grp_compute_gp_seq_core_Pipeline_RESCALE_LOOP_fu_94", "RefName" : "compute_gp_seq_core_Pipeline_RESCALE_LOOP","ID" : "40","Type" : "sequential",
					"SubLoops" : [
					{"Name" : "RESCALE_LOOP","RefName" : "RESCALE_LOOP","ID" : "41","Type" : "pipeline"},]},]},]},
		{"Name" : "grp_ga_seq_op_wedge_product_fu_345", "RefName" : "ga_seq_op_wedge_product","ID" : "42","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_compute_gp_seq_core_fu_14", "RefName" : "compute_gp_seq_core","ID" : "43","Type" : "sequential",
				"SubInsts" : [
				{"Name" : "grp_compute_gp_seq_core_Pipeline_SHARED_OUTER_LOOP_SHARED_INNER_LOOP_fu_74", "RefName" : "compute_gp_seq_core_Pipeline_SHARED_OUTER_LOOP_SHARED_INNER_LOOP","ID" : "44","Type" : "sequential",
					"SubLoops" : [
					{"Name" : "SHARED_OUTER_LOOP_SHARED_INNER_LOOP","RefName" : "SHARED_OUTER_LOOP_SHARED_INNER_LOOP","ID" : "45","Type" : "pipeline"},]},
				{"Name" : "grp_compute_gp_seq_core_Pipeline_RESCALE_LOOP_fu_94", "RefName" : "compute_gp_seq_core_Pipeline_RESCALE_LOOP","ID" : "46","Type" : "sequential",
					"SubLoops" : [
					{"Name" : "RESCALE_LOOP","RefName" : "RESCALE_LOOP","ID" : "47","Type" : "pipeline"},]},]},]},
		{"Name" : "grp_ga_seq_op_geometric_product_fu_354", "RefName" : "ga_seq_op_geometric_product","ID" : "48","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_compute_gp_seq_core_fu_14", "RefName" : "compute_gp_seq_core","ID" : "49","Type" : "sequential",
				"SubInsts" : [
				{"Name" : "grp_compute_gp_seq_core_Pipeline_SHARED_OUTER_LOOP_SHARED_INNER_LOOP_fu_74", "RefName" : "compute_gp_seq_core_Pipeline_SHARED_OUTER_LOOP_SHARED_INNER_LOOP","ID" : "50","Type" : "sequential",
					"SubLoops" : [
					{"Name" : "SHARED_OUTER_LOOP_SHARED_INNER_LOOP","RefName" : "SHARED_OUTER_LOOP_SHARED_INNER_LOOP","ID" : "51","Type" : "pipeline"},]},
				{"Name" : "grp_compute_gp_seq_core_Pipeline_RESCALE_LOOP_fu_94", "RefName" : "compute_gp_seq_core_Pipeline_RESCALE_LOOP","ID" : "52","Type" : "sequential",
					"SubLoops" : [
					{"Name" : "RESCALE_LOOP","RefName" : "RESCALE_LOOP","ID" : "53","Type" : "pipeline"},]},]},]},
		{"Name" : "grp_qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_361_3_fu_363", "RefName" : "qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_361_3","ID" : "54","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_361_3","RefName" : "VITIS_LOOP_361_3","ID" : "55","Type" : "pipeline"},]},
		{"Name" : "grp_qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_368_4_fu_368", "RefName" : "qgpu_ga_engine_shared_Pipeline_VITIS_LOOP_368_4","ID" : "56","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "VITIS_LOOP_368_4","RefName" : "VITIS_LOOP_368_4","ID" : "57","Type" : "pipeline"},]},]},]
}]}