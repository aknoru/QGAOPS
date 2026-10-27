# Accumulator Bit-Width and Numerical Range Analysis

## 1. Executive Summary & Defect Resolution

### The Original Defect
In earlier documentation, it was stated:
> "Eight maximum positive signed 32-bit raw products may sum to $2^{65}$, so a signed 66-bit integer is used as the accumulator."

This claim is **mathematically defective as written**:
- In standard two's complement binary representation, an $N$-bit signed integer has a numerical range of $[-2^{N-1}, +2^{N-1}-1]$.
- For $N = 66$, the maximum representable positive value is $+2^{65}-1$.
- If eight product terms were each $+2^{62}$, their sum would be $8 \times 2^{62} = 2^{65}$.
- Because $2^{65} > 2^{65}-1$, an unconstrained sum of $2^{65}$ **overflows a signed 66-bit accumulator by exactly 1 count**.

### Resolution & Normative Standardization
This analysis performs a rigorous path-by-path derivation of every arithmetic stage in the QGAOPS-QGPU datapath.
1. In exact Euclidean $Cl(3,0)$, every output blade has at least two negative sign terms in its pairwise multiplication table. Because the maximum positive signed 32-bit integer is $+2^{31}-1$, the exact maximum positive sum achievable in $Cl(3,0)$ is $6 \times 2^{62} + 2 \times (2^{62}-2^{31}) = 2^{65} - 2^{32} = 36,893,488,143,124,135,936$.
2. While $2^{65} - 2^{32} < 2^{65}-1$ fits within 66 bits in pure algebra, in hardware implementations:
   - Partial accumulation steps in pipelined adder-trees can accumulate positive terms before subtracting negative terms, temporarily reaching higher intermediate positive values.
   - Robust hardware design must provide an **unconditional mathematical guarantee** that does not depend on basis blade permutations or operand sign distribution.
3. Therefore, the normative hardware datapath is formally standardized to **signed 67 bits** (`ap_int<67>`). A signed 67-bit integer has a range of $[-2^{66}, +2^{66}-1] \approx [-7.378 \times 10^{19}, +7.378 \times 10^{19}]$, providing complete, unconditional headroom over the theoretical $2^{65}$ worst-case bound.

---

## 2. Path-by-Path Datapath Derivation

```
Operand A (int32_t) ──┐
                      ├──► [ ap_int<64> Multiplier ] ──► [ ap_int<67> Accumulator ] ──► [ Rescale / Sat ] ──► Result C (int32_t)
Operand B (int32_t) ──┘                                                                        │
                                                                                               ▼
                                                                                       Status (Overflow Flag)
```

### Path 1: Raw Operands
- Format: Signed 32-bit Q16.16 (`ap_fixed<32,16>` / `int32_t`).
- Range: $[-2^{31}, 2^{31}-1] = [-2,147,483,648, +2,147,483,647]$.
- Scale: $2^{16} = 65,536$.
- Real Range: $[-32,768.0, +32,767.9999847...]$.

### Path 2: Single Product Terms (`prod_t`)
- Operation: $P = a_i \times b_j$.
- Worst-case positive product:
  $$(-2^{31}) \times (-2^{31}) = +2^{62} = 4,611,686,018,427,387,904$$
- Worst-case negative product:
  $$(-2^{31}) \times (+2^{31}-1) = -2^{62} + 2^{31} = -4,611,686,016,279,904,256$$
- **Minimum Bit Width**:
  - Range: $[-2^{62}+2^{31}, +2^{62}]$.
  - A signed 63-bit integer has maximum positive value $2^{62}-1$, which cannot represent $+2^{62}$.
  - A signed **64-bit integer** (`ap_int<64>` / `int64_t`) has range $[-2^{63}, +2^{63}-1]$ and represents $+2^{62}$ with complete safety.
  - **Rule**: Operands must be cast to `prod_t` (`ap_int<64>`) prior to multiplication to prevent accidental 32-bit truncation.

### Path 3: Geometric Product Accumulation (`accum_t`)
- Operation: $S_k = \sum_{m=0}^7 s_{k,m} \cdot a_{i(k,m)} \cdot b_{j(k,m)}$.
- **Unconstrained Upper Bound**:
  $$8 \times (+2^{62}) = 2^{65} = 36,893,488,147,419,103,232$$
- Width Requirement:
  - $\text{Range required} \supseteq [-2^{65}, +2^{65}]$.
  - Signed 66-bit max: $2^{65}-1 = 36,893,488,147,419,103,231$ (insufficient by 1 count for unconstrained $2^{65}$).
  - Signed **67-bit max**: $2^{66}-1 = 73,786,976,294,838,206,463$ (**provably safe with $2\times$ headroom**).

### Path 4: Wedge Product Accumulation
- In the wedge product ($A \wedge B$), terms with overlapping vector components ($mask_a \cap mask_b \neq 0$) evaluate to zero:
  - Blade 0 (scalar): 1 term $\to$ max magnitude $2^{62}$ (requires 64 bits).
  - Blades 1, 2, 3 ($e_1, e_2, e_3$): 2 terms $\to$ max magnitude $2 \times 2^{62} = 2^{63}$ (requires 65 bits).
  - Blades 4, 5, 6 ($e_{12}, e_{13}, e_{23}$): 4 terms $\to$ max magnitude $4 \times 2^{62} = 2^{64}$ (requires 66 bits).
  - Blade 7 ($e_{123}$): 8 terms $\to$ max magnitude $8 \times 2^{62} = 2^{65}$ (requires 67 bits unconstrained).
- **Minimum Safe Unified Width**: **67 bits**.

### Path 5: Hestenes Inner Product Accumulation
- In the Hestenes inner product ($A \cdot B$), non-grade-lowering terms are discarded:
  - Blade 0 (scalar): 8 terms $\to$ max magnitude $8 \times 2^{62} = 2^{65}$ (requires 67 bits unconstrained).
  - Blades 1, 2, 3 ($e_1, e_2, e_3$): 4 terms $\to$ max magnitude $4 \times 2^{62} = 2^{64}$ (requires 66 bits).
  - Blades 4, 5, 6 ($e_{12}, e_{13}, e_{23}$): 2 terms $\to$ max magnitude $2 \times 2^{62} = 2^{63}$ (requires 65 bits).
  - Blade 7 ($e_{123}$): 1 term $\to$ max magnitude $2^{62}$ (requires 64 bits).
- **Minimum Safe Unified Width**: **67 bits**.

### Path 6: Addition and Subtraction (`add_accum_t`)
- Operation: $S_k = a_k \pm b_k$.
- Worst-case addition: $(-2^{31}) + (-2^{31}) = -2^{32}$.
- Worst-case subtraction: $(-2^{31}) - (+2^{31}-1) = -2^{32} + 1$.
- Range: $[-2^{32}, +2^{32}-2]$.
- **Minimum Safe Width**: Signed **33 bits** (`ap_int<33>`).
- Direct 32-bit addition without widening causes undefined two's complement overflow. A 33-bit intermediate allows exact overflow detection before clamping to $[-2^{31}, 2^{31}-1]$.

### Path 7: Rescaling and Rounding
- Formula: $Q = \lfloor S_k / 65536 \rfloor, \quad R = S_k \ \& \ 0\text{xFFFF}$.
- Round-to-Nearest-Even:
  - If $R < 32768$: $rounded = Q$.
  - If $R > 32768$: $rounded = Q + 1$.
  - If $R == 32768$ (exact half tie): $rounded = (Q \ \& \ 1 == 0) \ ? \ Q : Q + 1$.
- Saturation: Clamps to $[Q16\_MIN, Q16\_MAX]$ with sticky overflow flag.

---

## 3. Normative Width Specification Table

| Datapath Stage | Signal / Variable Name | Width (Bits) | Representation | Justification |
| :--- | :--- | :---: | :--- | :--- |
| **Operands** | `a[k]`, `b[k]` | 32 | `int32_t` / `ap_fixed<32,16>` | Standard signed Q16.16 storage format |
| **Multiplication** | `prod_t p` | 64 | `int64_t` / `ap_int<64>` | Holds $(-2^{31}) \times (-2^{31}) = +2^{62}$ without truncation |
| **GA Accumulation** | `accum_t accum[k]` | **67** | `__int128_t` / `ap_int<67>` | Unconditional guarantee for $8 \times 2^{62} = 2^{65} \le 2^{66}-1$ |
| **Add/Sub Accum** | `add_accum_t sum` | 33 | `int64_t` / `ap_int<33>` | Holds $(-2^{31}) + (-2^{31}) = -2^{32}$ before saturation |
| **Result** | `c[k]` | 32 | `int32_t` / `ap_fixed<32,16>` | Rescaled and saturated Q16.16 output |
| **Status** | `status` | 32 | `uint32_t` | Bit 0: Overflow sticky flag; Bit 1: Invalid opcode |
