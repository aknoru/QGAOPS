# Stage 9 interface validation report

The proposed serializer uses a versioned 76-byte scalar request: a 12-byte
header and two 32-byte eight-coefficient operands. Test vectors are generated
by `scripts/generate_test_vectors.py`. Contract tests validate round trips,
operation identifiers, malformed lengths, version mismatches, and fixed-point
execution. These are software contract tests only; no AXI, DMA, HLS, RTL, or
physical-board behavior is claimed.
