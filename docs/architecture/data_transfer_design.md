# Proposed bulk data-transfer design

Two candidates remain under evaluation:

1. AXI DMA with streaming operand/result channels: explicit ownership,
   descriptors, backpressure, and completion/error handling.
2. AXI memory-mapped buffering: simpler control but potentially greater PS/PL
   coupling and memory-traffic sensitivity.

The control path is AXI4-Lite; bulk data is not assumed to travel over the
control bus. Future PYNQ software must allocate physically suitable buffers,
flush/invalidate caches according to the actual platform API, and verify
completion before reuse. No cache coherency or DMA behavior is claimed.

Stage 10 must select a path using measured buffer capacity, transfer size,
latency, error recovery, and tool-support evidence.
