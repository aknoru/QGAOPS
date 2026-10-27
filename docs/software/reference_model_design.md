# Reference-model design

The Stage 4 oracle is split into two independently implemented arithmetic
paths. `qgaops_reference.algebra` stores eight finite Python floats and
computes products using the documented basis-mask sign rule. The fixed-point
module stores eight signed integers and uses Q16.16 integer products, explicit
round-to-nearest-even rescaling, and saturation flags. They share only
immutable basis metadata and the mathematical sign metadata, not arithmetic
results or conversion code.

The floating model supports addition, subtraction, negation, scalar scaling,
geometric product, wedge, Hestenes inner product, grade projection, reverse,
grade involution, and Clifford conjugation. The fixed model supports the same
core operations with deterministic integer arithmetic.

The fixed model uses arbitrary-precision Python accumulation after each
individual product. This is deliberate oracle behavior because the prior
specification did not select a bounded hardware accumulator width. Stage 5
must choose and verify that width from worst-case bounds.

Tests use an independently written sign oracle and exhaustive 8x8 basis-pair
coverage for geometric, wedge, and Hestenes products. Randomized algebraic
tests use seed `20261026`; they supplement, rather than replace, exhaustive
cases.
