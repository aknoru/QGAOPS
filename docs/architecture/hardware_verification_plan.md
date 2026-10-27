# Hardware contract verification plan

Before hardware implementation, software tests validate serialization,
deserialization, coefficient ordering, operation IDs, length/version checks,
Q16.16 bounds, and expected fixed-point results. Stage 10 will add HLS
co-simulation and interface timing tests. Later board tests must separately
report PS preparation, transfer, kernel, result transfer, and end-to-end
timings. This contract simulator is not an AXI or FPGA simulator.
