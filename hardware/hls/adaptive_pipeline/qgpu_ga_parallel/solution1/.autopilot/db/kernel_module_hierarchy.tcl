set ModuleHierarchy {[{
"Name" : "qgpu_ga_parallel_top", "RefName" : "qgpu_ga_parallel_top","ID" : "0","Type" : "sequential",
"SubInsts" : [
	{"Name" : "grp_qgpu_ga_engine_parallel_fu_247", "RefName" : "qgpu_ga_engine_parallel","ID" : "1","Type" : "sequential",
		"SubInsts" : [
		{"Name" : "grp_qgpu_ga_engine_parallel_Pipeline_AAMF_STAGE_IN_fu_686", "RefName" : "qgpu_ga_engine_parallel_Pipeline_AAMF_STAGE_IN","ID" : "2","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "AAMF_STAGE_IN","RefName" : "AAMF_STAGE_IN","ID" : "3","Type" : "pipeline"},]},
		{"Name" : "grp_qgpu_ga_engine_parallel_Pipeline_AAMF_FETCH_fu_727", "RefName" : "qgpu_ga_engine_parallel_Pipeline_AAMF_FETCH","ID" : "4","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "AAMF_FETCH","RefName" : "AAMF_FETCH","ID" : "5","Type" : "pipeline"},]},
		{"Name" : "grp_ga_op_rotor_sandwich_fu_753", "RefName" : "ga_op_rotor_sandwich","ID" : "6","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "compute_gp_core", "RefName" : "compute_gp_core","ID" : "7","Type" : "sequential",
				"SubInsts" : [
				{"Name" : "grp_rescale_and_saturate_fu_357", "RefName" : "rescale_and_saturate","ID" : "8","Type" : "sequential"},],
				"SubLoops" : [
				{"Name" : "PARALLEL_OUTER_LOOP","RefName" : "PARALLEL_OUTER_LOOP","ID" : "9","Type" : "pipeline",
				"SubInsts" : [
				{"Name" : "sign_blade_product_sign_fu_301", "RefName" : "blade_product_sign","ID" : "10","Type" : "pipeline"},
				{"Name" : "sign_1_blade_product_sign_fu_308", "RefName" : "blade_product_sign","ID" : "11","Type" : "pipeline"},
				{"Name" : "sign_2_blade_product_sign_fu_315", "RefName" : "blade_product_sign","ID" : "12","Type" : "pipeline"},
				{"Name" : "sign_3_blade_product_sign_fu_322", "RefName" : "blade_product_sign","ID" : "13","Type" : "pipeline"},
				{"Name" : "sign_4_blade_product_sign_fu_329", "RefName" : "blade_product_sign","ID" : "14","Type" : "pipeline"},
				{"Name" : "sign_5_blade_product_sign_fu_336", "RefName" : "blade_product_sign","ID" : "15","Type" : "pipeline"},
				{"Name" : "sign_6_blade_product_sign_fu_343", "RefName" : "blade_product_sign","ID" : "16","Type" : "pipeline"},
				{"Name" : "sign_7_blade_product_sign_fu_350", "RefName" : "blade_product_sign","ID" : "17","Type" : "pipeline"},]},]},
			{"Name" : "ga_op_reverse", "RefName" : "ga_op_reverse","ID" : "18","Type" : "sequential"},]},
		{"Name" : "grp_ga_op_inner_product_fu_775", "RefName" : "ga_op_inner_product","ID" : "19","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_compute_gp_core_fu_138", "RefName" : "compute_gp_core","ID" : "20","Type" : "sequential",
				"SubInsts" : [
				{"Name" : "grp_rescale_and_saturate_fu_357", "RefName" : "rescale_and_saturate","ID" : "21","Type" : "sequential"},],
				"SubLoops" : [
				{"Name" : "PARALLEL_OUTER_LOOP","RefName" : "PARALLEL_OUTER_LOOP","ID" : "22","Type" : "pipeline",
				"SubInsts" : [
				{"Name" : "sign_blade_product_sign_fu_301", "RefName" : "blade_product_sign","ID" : "23","Type" : "pipeline"},
				{"Name" : "sign_1_blade_product_sign_fu_308", "RefName" : "blade_product_sign","ID" : "24","Type" : "pipeline"},
				{"Name" : "sign_2_blade_product_sign_fu_315", "RefName" : "blade_product_sign","ID" : "25","Type" : "pipeline"},
				{"Name" : "sign_3_blade_product_sign_fu_322", "RefName" : "blade_product_sign","ID" : "26","Type" : "pipeline"},
				{"Name" : "sign_4_blade_product_sign_fu_329", "RefName" : "blade_product_sign","ID" : "27","Type" : "pipeline"},
				{"Name" : "sign_5_blade_product_sign_fu_336", "RefName" : "blade_product_sign","ID" : "28","Type" : "pipeline"},
				{"Name" : "sign_6_blade_product_sign_fu_343", "RefName" : "blade_product_sign","ID" : "29","Type" : "pipeline"},
				{"Name" : "sign_7_blade_product_sign_fu_350", "RefName" : "blade_product_sign","ID" : "30","Type" : "pipeline"},]},]},]},
		{"Name" : "grp_ga_op_wedge_product_fu_797", "RefName" : "ga_op_wedge_product","ID" : "31","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_compute_gp_core_fu_138", "RefName" : "compute_gp_core","ID" : "32","Type" : "sequential",
				"SubInsts" : [
				{"Name" : "grp_rescale_and_saturate_fu_357", "RefName" : "rescale_and_saturate","ID" : "33","Type" : "sequential"},],
				"SubLoops" : [
				{"Name" : "PARALLEL_OUTER_LOOP","RefName" : "PARALLEL_OUTER_LOOP","ID" : "34","Type" : "pipeline",
				"SubInsts" : [
				{"Name" : "sign_blade_product_sign_fu_301", "RefName" : "blade_product_sign","ID" : "35","Type" : "pipeline"},
				{"Name" : "sign_1_blade_product_sign_fu_308", "RefName" : "blade_product_sign","ID" : "36","Type" : "pipeline"},
				{"Name" : "sign_2_blade_product_sign_fu_315", "RefName" : "blade_product_sign","ID" : "37","Type" : "pipeline"},
				{"Name" : "sign_3_blade_product_sign_fu_322", "RefName" : "blade_product_sign","ID" : "38","Type" : "pipeline"},
				{"Name" : "sign_4_blade_product_sign_fu_329", "RefName" : "blade_product_sign","ID" : "39","Type" : "pipeline"},
				{"Name" : "sign_5_blade_product_sign_fu_336", "RefName" : "blade_product_sign","ID" : "40","Type" : "pipeline"},
				{"Name" : "sign_6_blade_product_sign_fu_343", "RefName" : "blade_product_sign","ID" : "41","Type" : "pipeline"},
				{"Name" : "sign_7_blade_product_sign_fu_350", "RefName" : "blade_product_sign","ID" : "42","Type" : "pipeline"},]},]},]},
		{"Name" : "grp_ga_op_geometric_product_fu_819", "RefName" : "ga_op_geometric_product","ID" : "43","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "compute_gp_core", "RefName" : "compute_gp_core","ID" : "44","Type" : "sequential",
				"SubInsts" : [
				{"Name" : "grp_rescale_and_saturate_fu_357", "RefName" : "rescale_and_saturate","ID" : "45","Type" : "sequential"},],
				"SubLoops" : [
				{"Name" : "PARALLEL_OUTER_LOOP","RefName" : "PARALLEL_OUTER_LOOP","ID" : "46","Type" : "pipeline",
				"SubInsts" : [
				{"Name" : "sign_blade_product_sign_fu_301", "RefName" : "blade_product_sign","ID" : "47","Type" : "pipeline"},
				{"Name" : "sign_1_blade_product_sign_fu_308", "RefName" : "blade_product_sign","ID" : "48","Type" : "pipeline"},
				{"Name" : "sign_2_blade_product_sign_fu_315", "RefName" : "blade_product_sign","ID" : "49","Type" : "pipeline"},
				{"Name" : "sign_3_blade_product_sign_fu_322", "RefName" : "blade_product_sign","ID" : "50","Type" : "pipeline"},
				{"Name" : "sign_4_blade_product_sign_fu_329", "RefName" : "blade_product_sign","ID" : "51","Type" : "pipeline"},
				{"Name" : "sign_5_blade_product_sign_fu_336", "RefName" : "blade_product_sign","ID" : "52","Type" : "pipeline"},
				{"Name" : "sign_6_blade_product_sign_fu_343", "RefName" : "blade_product_sign","ID" : "53","Type" : "pipeline"},
				{"Name" : "sign_7_blade_product_sign_fu_350", "RefName" : "blade_product_sign","ID" : "54","Type" : "pipeline"},]},]},]},
		{"Name" : "grp_ga_op_rotor_norm_fu_841", "RefName" : "ga_op_rotor_norm","ID" : "55","Type" : "sequential"},
		{"Name" : "grp_qgpu_ga_engine_parallel_Pipeline_AAMF_COMMIT_OUT_fu_853", "RefName" : "qgpu_ga_engine_parallel_Pipeline_AAMF_COMMIT_OUT","ID" : "56","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "AAMF_COMMIT_OUT","RefName" : "AAMF_COMMIT_OUT","ID" : "57","Type" : "pipeline"},]},
		{"Name" : "call_ret9_ga_op_clifford_conjugation_fu_889", "RefName" : "ga_op_clifford_conjugation","ID" : "58","Type" : "sequential"},
		{"Name" : "call_ret8_ga_op_grade_involution_fu_901", "RefName" : "ga_op_grade_involution","ID" : "59","Type" : "sequential"},
		{"Name" : "call_ret7_ga_op_reverse_fu_913", "RefName" : "ga_op_reverse","ID" : "60","Type" : "sequential"},
		{"Name" : "call_ret6_ga_op_grade_project_fu_927", "RefName" : "ga_op_grade_project","ID" : "61","Type" : "sequential"},
		{"Name" : "grp_ga_op_scalar_mul_fu_940", "RefName" : "ga_op_scalar_mul","ID" : "62","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_rescale_and_saturate_fu_80", "RefName" : "rescale_and_saturate","ID" : "63","Type" : "sequential"},]},
		{"Name" : "grp_ga_op_subtraction_fu_953", "RefName" : "ga_op_subtraction","ID" : "64","Type" : "sequential"},
		{"Name" : "grp_ga_op_addition_fu_973", "RefName" : "ga_op_addition","ID" : "65","Type" : "sequential"},]},]
}]}