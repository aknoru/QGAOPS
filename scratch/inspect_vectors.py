import re
from collections import Counter

with open('HW/hls/common/tests/test_vectors.h') as f:
    text = f.read()

# Match entries: { id, "CATEGORY", op_id, "op_name", {a}, {b}, {exp}, status, "desc" }
pattern = re.compile(r'\{\s*(\d+),\s*"([^"]+)",\s*(\d+),\s*"([^"]+)"')
matches = pattern.findall(text)

print(f"Total test vectors in test_vectors.h: {len(matches)}")
print("Categories:", Counter(m[1] for m in matches))
print("Operations:", Counter(m[3] for m in matches))

with open('HW/hls/common/tests/quantum_test_vectors.h') as f:
    q_text = f.read()

q_matches = re.findall(r'\{\s*"([^"]+)",\s*"([^"]+)",\s*([A-Z0-9_]+)', q_text)
print(f"Total quantum test vectors: {len(q_matches)}")
for q in q_matches:
    print(f"  {q[0]}: {q[2]}")
