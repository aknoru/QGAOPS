# Algebra-Aware Memory Fabric proposal

AAMF is a proposed buffering and scheduling organization, not a demonstrated
optimization. The reference baseline is direct operand/result buffering with
no reuse beyond one operation. AAMF will use operand slots, result slots,
ownership tags, and a scheduler that can retain operands across a batch when
dependencies permit.

Instrumentation must count DDR bytes, local-buffer reads/writes, slot hits,
stalls, backpressure, and arbitration decisions. Capacity, BRAM/register
usage, and arbitration policy are unmeasured design parameters. The
comparison must use identical operations, data, precision, batch, and
measurement boundaries; no traffic or throughput reduction is asserted.
