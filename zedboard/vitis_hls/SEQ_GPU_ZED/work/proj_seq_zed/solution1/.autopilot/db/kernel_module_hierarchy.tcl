set ModuleHierarchy {[{
"Name" : "seq_gpu", "RefName" : "seq_gpu","ID" : "0","Type" : "sequential",
"SubInsts" : [
	{"Name" : "grp_seq_op_rotor_norm_fu_214", "RefName" : "seq_op_rotor_norm","ID" : "1","Type" : "sequential",
		"SubInsts" : [
		{"Name" : "grp_seq_op_rotor_norm_Pipeline_NORM_LOOP_fu_88", "RefName" : "seq_op_rotor_norm_Pipeline_NORM_LOOP","ID" : "2","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "NORM_LOOP","RefName" : "NORM_LOOP","ID" : "3","Type" : "pipeline"},]},
		{"Name" : "grp_seq_op_rotor_norm_Pipeline_CLEAR_REMAINING_fu_95", "RefName" : "seq_op_rotor_norm_Pipeline_CLEAR_REMAINING","ID" : "4","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "CLEAR_REMAINING","RefName" : "CLEAR_REMAINING","ID" : "5","Type" : "pipeline"},]},]},
	{"Name" : "grp_seq_op_sandwich_fu_222", "RefName" : "seq_op_sandwich","ID" : "6","Type" : "sequential",
		"SubInsts" : [
		{"Name" : "grp_seq_product_core_fu_44", "RefName" : "seq_product_core","ID" : "7","Type" : "sequential",
			"SubInsts" : [
			{"Name" : "grp_seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP_fu_94", "RefName" : "seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP","ID" : "8","Type" : "sequential",
				"SubLoops" : [
				{"Name" : "OUTER_LOOP_INNER_LOOP","RefName" : "OUTER_LOOP_INNER_LOOP","ID" : "9","Type" : "pipeline"},]},
			{"Name" : "grp_seq_product_core_Pipeline_RESCALE_LOOP_fu_114", "RefName" : "seq_product_core_Pipeline_RESCALE_LOOP","ID" : "10","Type" : "sequential",
				"SubLoops" : [
				{"Name" : "RESCALE_LOOP","RefName" : "RESCALE_LOOP","ID" : "11","Type" : "pipeline"},]},]},
		{"Name" : "grp_seq_op_reverse_fu_61", "RefName" : "seq_op_reverse","ID" : "12","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "REVERSE_LOOP","RefName" : "REVERSE_LOOP","ID" : "13","Type" : "pipeline"},]},]},
	{"Name" : "grp_seq_op_clifford_conj_fu_234", "RefName" : "seq_op_clifford_conj","ID" : "14","Type" : "sequential",
		"SubLoops" : [
		{"Name" : "CONJ_LOOP","RefName" : "CONJ_LOOP","ID" : "15","Type" : "pipeline"},]},
	{"Name" : "grp_seq_op_grade_involution_fu_242", "RefName" : "seq_op_grade_involution","ID" : "16","Type" : "sequential",
		"SubLoops" : [
		{"Name" : "INVOLUTION_LOOP","RefName" : "INVOLUTION_LOOP","ID" : "17","Type" : "pipeline"},]},
	{"Name" : "grp_seq_op_reverse_fu_250", "RefName" : "seq_op_reverse","ID" : "18","Type" : "sequential",
		"SubLoops" : [
		{"Name" : "REVERSE_LOOP","RefName" : "REVERSE_LOOP","ID" : "19","Type" : "pipeline"},]},
	{"Name" : "grp_seq_op_sub_fu_260", "RefName" : "seq_op_sub","ID" : "20","Type" : "sequential",
		"SubLoops" : [
		{"Name" : "SUB_LOOP","RefName" : "SUB_LOOP","ID" : "21","Type" : "pipeline"},]},
	{"Name" : "grp_seq_op_add_fu_270", "RefName" : "seq_op_add","ID" : "22","Type" : "sequential",
		"SubLoops" : [
		{"Name" : "ADD_LOOP","RefName" : "ADD_LOOP","ID" : "23","Type" : "pipeline"},]},
	{"Name" : "grp_seq_product_core_fu_280", "RefName" : "seq_product_core","ID" : "24","Type" : "sequential",
		"SubInsts" : [
		{"Name" : "grp_seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP_fu_94", "RefName" : "seq_product_core_Pipeline_OUTER_LOOP_INNER_LOOP","ID" : "25","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "OUTER_LOOP_INNER_LOOP","RefName" : "OUTER_LOOP_INNER_LOOP","ID" : "26","Type" : "pipeline"},]},
		{"Name" : "grp_seq_product_core_Pipeline_RESCALE_LOOP_fu_114", "RefName" : "seq_product_core_Pipeline_RESCALE_LOOP","ID" : "27","Type" : "sequential",
			"SubLoops" : [
			{"Name" : "RESCALE_LOOP","RefName" : "RESCALE_LOOP","ID" : "28","Type" : "pipeline"},]},]},
	{"Name" : "grp_seq_gpu_Pipeline_CLEAR_ERR_fu_295", "RefName" : "seq_gpu_Pipeline_CLEAR_ERR","ID" : "29","Type" : "sequential",
		"SubLoops" : [
		{"Name" : "CLEAR_ERR","RefName" : "CLEAR_ERR","ID" : "30","Type" : "pipeline"},]},
	{"Name" : "grp_seq_op_grade_proj_fu_301", "RefName" : "seq_op_grade_proj","ID" : "31","Type" : "sequential",
		"SubLoops" : [
		{"Name" : "GRADE_LOOP","RefName" : "GRADE_LOOP","ID" : "32","Type" : "pipeline"},]},
	{"Name" : "grp_seq_op_scalar_mul_fu_311", "RefName" : "seq_op_scalar_mul","ID" : "33","Type" : "sequential",
		"SubLoops" : [
		{"Name" : "SCALAR_LOOP","RefName" : "SCALAR_LOOP","ID" : "34","Type" : "pipeline"},]},]
}]}