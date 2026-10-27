# Fixed-point specification

The initial format is signed 32-bit Q16.16: one sign/integer field plus
16 fractional bits, with representable decoded range
`[-32768, 32767.9999847412109375]`. Encoding rounds a real value to the
nearest integer multiple of `2^-16`; ties use round-to-nearest-even.

Each coefficient is encoded independently. Each coefficient product is a signed 64-bit product before rescaling. The
Stage 4 Python reference uses an arbitrary-precision accumulator for the sum
of all contributing products, so no intermediate overflow is silently lost.
Future hardware must select a bounded accumulator width by worst-case analysis
and prove that it preserves this behavior. Narrowing
uses the selected rounding rule, then saturates to the Q16.16 endpoints.
Saturation sets an overflow flag; it is never silent. Invalid operation,
protocol, and arithmetic status bits are distinct.

For a floating reference `x` and decoded fixed result `y`, report absolute
error `|x-y|`, relative error `|x-y|/max(|x|,epsilon)`, maximum coefficient
error, RMS coefficient error, saturation count, and operation-level pass/fail.
Initial acceptance is proposed as `<= 1.5 ulp` for values without
intermediate saturation; workload-specific tolerances must be approved after
range characterization.

Conversion tests must include zero, signed values, half-ulp ties, endpoints,
out-of-range values, and products whose intermediate is wider than 32 bits.
