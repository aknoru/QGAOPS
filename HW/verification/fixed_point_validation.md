# Fixed-Point Numerical Verification and Proof of Wordlengths

## 1. Mathematical Representation and Dynamic Range

The accelerator uses signed 32-bit fixed-point numbers in two's complement format ($Q16.16$):
* **Total Width**: $W = 32\text{ bits}$
* **Integer Bits**: $I = 16\text{ bits}$ (including 1 sign bit)
* **Fractional Bits**: $F = 16\text{ bits}$
* **Scale Factor**: $S = 2^{16} = 65536$
* **Representation Interval**:
  $$\text{Value} \in \left[ \frac{-2^{31}}{2^{16}}, \frac{2^{31}-1}{2^{16}} \right] = [-32768.0, +32767.99998474121]$$
* **Quantization Step (LSB)**:
  $$\Delta = 2^{-16} \approx 1.5258789 \times 10^{-5}$$

---

## 2. Proof of 67-Bit Accumulator Sufficiency

### Theorem
*An accumulator bit-width of 67 signed bits is strictly necessary and sufficient to accumulate the sum of 8 bilinear products of signed 32-bit Q16.16 multivector coefficients without intermediate overflow.*

### Mathematical Proof
1. **Single Product Range**:
   Let $a, b \in [-2^{31}, 2^{31}-1]$.
   The maximum magnitude of a single product $P = a \times b$ occurs when $a = -2^{31}$ and $b = -2^{31}$:
   $$P_{\max} = (-2^{31}) \times (-2^{31}) = +2^{62}$$
   In two's complement, representing $+2^{62}$ requires at least 64 signed bits ($[-2^{63}, 2^{63}-1]$).
2. **Sum of 8 Terms**:
   In Euclidean $\text{Cl}(3,0)$, each output blade $c_k$ is the sum of at most 8 product terms:
   $$S = \sum_{i=1}^8 \pm P_i$$
   The worst-case theoretical maximum magnitude is:
   $$|S|_{\max} \le 8 \times P_{\max} = 8 \times 2^{62} = 2^3 \times 2^{62} = 2^{65}$$
3. **Bit-Width Requirement**:
   To represent a signed two's complement value in $[-2^{65}, +2^{65}]$, the minimum number of signed bits $N$ must satisfy:
   $$2^{N-1} - 1 \ge 2^{65} \implies 2^{N-1} > 2^{65} \implies N - 1 \ge 66 \implies N \ge 67\text{ bits}$$
4. **Conclusion**:
   An accumulator width of exactly **67 signed bits (`ap_int<67>`)** guarantees that intermediate overflow is mathematically impossible prior to the rescaling and saturation stage. $\blacksquare$

---

## 3. Rescaling: Round-to-Nearest-Even (Banker's Rounding)

To convert an accumulated sum $S$ from $Q32.32$ scaling back to $Q16.16$, the hardware shifts the value right by 16 bits ($S / 65536$).

Standard truncation or truncation-towards-zero introduces a negative DC bias in multi-stage cascade operations (such as rotor sandwich products $A B \widetilde{A}$). The QGAOPS hardware implements **Round-to-Nearest-Even**:
Let $S = q \cdot 65536 + r$, where $q = \lfloor S / 65536 \rfloor$ and $r \in [0, 65535]$:
$$\text{Rounded}(S) = \begin{cases}
q & \text{if } r < 32768 \\
q + 1 & \text{if } r > 32768 \\
q & \text{if } r = 32768 \text{ and } q \text{ is even} \\
q + 1 & \text{if } r = 32768 \text{ and } q \text{ is odd}
\end{cases}$$

This guarantees zero statistical drift across long sequence rotations.

---

## 4. Saturation Limiter and Overflow Flag

If the rounded quotient exceeds the representable 32-bit range:
$$\text{Saturated}(X) = \begin{cases}
+2147483647 & \text{if } X > 2147483647 \quad (\text{Status} \leftarrow \text{STATUS\_OVERFLOW}) \\
-2147483648 & \text{if } X < -2147483648 \quad (\text{Status} \leftarrow \text{STATUS\_OVERFLOW}) \\
X & \text{otherwise}
\end{cases}$$
