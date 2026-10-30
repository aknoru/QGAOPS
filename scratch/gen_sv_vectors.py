import json

with open("D:/QGPU/scratch/all_vectors.json") as f:
    vectors = json.load(f)

print(f"Loaded {len(vectors)} vectors")

out_file = "D:/QGPU/HW/vivado/verification/src/test_vectors_data.svh"

def format_val(val):
    if val < 0:
        return f"-32'sd{abs(val)}"
    else:
        return f"32'sd{val}"

with open(out_file, "w") as f:
    f.write("// Auto-generated SystemVerilog test vector definitions\n")
    f.write("`ifndef TEST_VECTORS_DATA_SVH\n`define TEST_VECTORS_DATA_SVH\n\n")
    f.write("typedef struct {\n")
    f.write("    int test_id;\n")
    f.write("    string category;\n")
    f.write("    int opcode;\n")
    f.write("    string op_name;\n")
    f.write("    int a[8];\n")
    f.write("    int b[8];\n")
    f.write("    int expected[8];\n")
    f.write("    int expected_status;\n")
    f.write("    string description;\n")
    f.write("} test_case_t;\n\n")
    f.write(f"localparam int TOTAL_TESTS = {len(vectors)};\n\n")
    f.write("function automatic void init_test_vectors(output test_case_t tests[TOTAL_TESTS]);\n")
    for i, v in enumerate(vectors):
        a_str = "'{" + ", ".join(format_val(val) for val in v["a"]) + "}"
        b_str = "'{" + ", ".join(format_val(val) for val in v["b"]) + "}"
        exp_str = "'{" + ", ".join(format_val(val) for val in v["expected"]) + "}"
        desc = v["description"].replace('"', '\\"').replace('\n', ' ')
        f.write(f"    tests[{i}].test_id = {v['id']};\n")
        f.write(f"    tests[{i}].category = \"{v['category']}\";\n")
        f.write(f"    tests[{i}].opcode = {v['opcode']};\n")
        f.write(f"    tests[{i}].op_name = \"{v['op_name']}\";\n")
        f.write(f"    tests[{i}].a = {a_str};\n")
        f.write(f"    tests[{i}].b = {b_str};\n")
        f.write(f"    tests[{i}].expected = {exp_str};\n")
        f.write(f"    tests[{i}].expected_status = {v['expected_status']};\n")
        f.write(f"    tests[{i}].description = \"{desc}\";\n")
    f.write("endfunction\n\n")
    f.write("`endif // TEST_VECTORS_DATA_SVH\n")

print(f"Generated {out_file} successfully.")
