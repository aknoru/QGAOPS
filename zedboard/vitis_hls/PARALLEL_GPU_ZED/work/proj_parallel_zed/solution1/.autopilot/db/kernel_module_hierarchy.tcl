set ModuleHierarchy {[{
"Name" : "parallel_gpu", "RefName" : "parallel_gpu","ID" : "0","Type" : "sequential",
"SubInsts" : [
	{"Name" : "grp_parallel_op_rotor_norm_fu_433", "RefName" : "parallel_op_rotor_norm","ID" : "1","Type" : "pipeline"},
	{"Name" : "grp_parallel_op_sandwich_fu_445", "RefName" : "parallel_op_sandwich","ID" : "2","Type" : "dataflow",
		"SubInsts" : [
		{"Name" : "parallel_product_core_U0", "RefName" : "parallel_product_core","ID" : "3","Type" : "pipeline"},
		{"Name" : "parallel_op_reverse_U0", "RefName" : "parallel_op_reverse","ID" : "4","Type" : "pipeline"},
		{"Name" : "parallel_product_core_3_U0", "RefName" : "parallel_product_core_3","ID" : "5","Type" : "pipeline"},]},
	{"Name" : "call_ret7_parallel_op_clifford_conj_fu_483", "RefName" : "parallel_op_clifford_conj","ID" : "6","Type" : "pipeline"},
	{"Name" : "call_ret6_parallel_op_grade_involution_fu_495", "RefName" : "parallel_op_grade_involution","ID" : "7","Type" : "pipeline"},
	{"Name" : "call_ret5_parallel_op_reverse_1_fu_507", "RefName" : "parallel_op_reverse_1","ID" : "8","Type" : "pipeline"},
	{"Name" : "call_ret4_parallel_op_grade_proj_fu_519", "RefName" : "parallel_op_grade_proj","ID" : "9","Type" : "pipeline"},
	{"Name" : "grp_parallel_op_scalar_mul_fu_532", "RefName" : "parallel_op_scalar_mul","ID" : "10","Type" : "pipeline"},
	{"Name" : "grp_parallel_op_sub_fu_545", "RefName" : "parallel_op_sub","ID" : "11","Type" : "pipeline"},
	{"Name" : "grp_parallel_op_add_fu_565", "RefName" : "parallel_op_add","ID" : "12","Type" : "pipeline"},
	{"Name" : "grp_parallel_product_core_2_fu_585", "RefName" : "parallel_product_core_2","ID" : "13","Type" : "pipeline"},]
}]}