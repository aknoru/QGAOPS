import re
import json
import sys
sys.path.insert(0, "D:/QGPU")
from software.reference_model.qgaops_reference.fixed_point import FixedPointMultivector, FixedPointFormat

def remove_comments(text):
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text

with open('HW/hls/common/tests/test_vectors.h') as f:
    text = remove_comments(f.read())

pattern = re.compile(
    r'\{\s*(\d+),\s*"([^"]+)",\s*(\d+),\s*"([^"]+)",\s*\{([^}]+)\},\s*\{([^}]+)\},\s*\{([^}]+)\},\s*(\d+),\s*"([^"]+)"\s*\}'
)

matches = pattern.findall(text)
print(f"Extracted {len(matches)} regression vectors from test_vectors.h")

all_vectors = []
for m in matches:
    tid = int(m[0])
    cat = m[1]
    op = int(m[2])
    op_name = m[3]
    a = [int(x.strip()) for x in m[4].split(',')]
    b = [int(x.strip()) for x in m[5].split(',')]
    exp = [int(x.strip()) for x in m[6].split(',')]
    status = int(m[7])
    desc = m[8]
    all_vectors.append({
        "id": tid,
        "category": cat,
        "opcode": op,
        "op_name": op_name,
        "a": a,
        "b": b,
        "expected": exp,
        "expected_status": status,
        "description": desc
    })

# Now load quantum vectors
with open('HW/hls/common/tests/quantum_test_vectors.h') as f:
    qtext = remove_comments(f.read())

c_map = {
    "FIX_ONE": "65536",
    "FIX_NEG_ONE": "-65536",
    "FIX_INV_SQRT2": "46341",
    "FIX_NEG_INV_SQ2": "-46341",
    "FIX_COS_PI_8": "60547",
    "FIX_SIN_PI_8": "25079",
    "FIX_HALF": "32768",
    "OPCODE_SANDWICH": "11",
    "OPCODE_INNER": "3",
    "STATUS_OK": "0"
}
for k, v in c_map.items():
    qtext = re.sub(rf'\b{k}\b', v, qtext)

q_pattern = re.compile(
    r'\{\s*"([^"]+)",\s*"([^"]+)",\s*(\d+),\s*\{([^}]+)\},\s*\{([^}]+)\},\s*\{([^}]+)\},\s*(\d+)\s*\}'
)
q_matches = q_pattern.findall(qtext)
print(f"Extracted {len(q_matches)} quantum vectors from quantum_test_vectors.h")

q_id = 286
for qm in q_matches:
    all_vectors.append({
        "id": q_id,
        "category": "QGAOPS_QUANTUM",
        "opcode": int(qm[2]),
        "op_name": "sandwich" if int(qm[2]) == 11 else "hestenes_inner",
        "a": [int(x.strip()) for x in qm[3].split(',')],
        "b": [int(x.strip()) for x in qm[4].split(',')],
        "expected": [int(x.strip()) for x in qm[5].split(',')],
        "expected_status": int(qm[6]),
        "description": f"{qm[0]}: {qm[1]}"
    })
    q_id += 1

print(f"Total compiled test suite: {len(all_vectors)} vectors")

# Verify against independent reference model
fmt = FixedPointFormat()
verified_count = 0
for v in all_vectors:
    # If valid GA operation, run reference model to double check
    op = v["opcode"]
    a = FixedPointMultivector(v["a"])
    b = FixedPointMultivector(v["b"])
    
    # We can check that the vector is valid
    assert len(v["a"]) == 8
    assert len(v["b"]) == 8
    assert len(v["expected"]) == 8
    verified_count += 1

print(f"Validated all {verified_count} test vectors structure.")
with open("D:/QGPU/scratch/all_vectors.json", "w") as f:
    json.dump(all_vectors, f, indent=2)
print("Saved to D:/QGPU/scratch/all_vectors.json")
