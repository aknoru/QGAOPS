# Operation Coverage and Basis Pair Multiplication Table

## 1. Cl(3,0) Basis Blade Multiplication Table (Cayley Table)

The table below shows the exact Euclidean Clifford product $e_L e_R$ for all 64 ordered basis pairs in $\text{Cl}(3,0)$.

| $e_L \backslash e_R$ | $1$ (0) | $e_1$ (1) | $e_2$ (2) | $e_3$ (3) | $e_{12}$ (4) | $e_{13}$ (5) | $e_{23}$ (6) | $e_{123}$ (7) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$1$ (0)** | $+1$ | $+e_1$ | $+e_2$ | $+e_3$ | $+e_{12}$ | $+e_{13}$ | $+e_{23}$ | $+e_{123}$ |
| **$e_1$ (1)** | $+e_1$ | $+1$ | $+e_{12}$ | $+e_{13}$ | $+e_2$ | $+e_3$ | $+e_{123}$ | $+e_{23}$ |
| **$e_2$ (2)** | $+e_2$ | $-e_{12}$ | $+1$ | $+e_{23}$ | $-e_1$ | $-e_{123}$ | $+e_3$ | $-e_{13}$ |
| **$e_3$ (3)** | $+e_3$ | $-e_{13}$ | $-e_{23}$ | $+1$ | $+e_{123}$ | $-e_1$ | $-e_2$ | $+e_{12}$ |
| **$e_{12}$ (4)** | $+e_{12}$ | $-e_2$ | $+e_1$ | $+e_{123}$ | $-1$ | $-e_{23}$ | $+e_{13}$ | $-e_3$ |
| **$e_{13}$ (5)** | $+e_{13}$ | $-e_3$ | $-e_{123}$ | $+e_1$ | $+e_{23}$ | $-1$ | $-e_{12}$ | $+e_2$ |
| **$e_{23}$ (6)** | $+e_{23}$ | $+e_{123}$ | $-e_3$ | $+e_2$ | $-e_{13}$ | $+e_{12}$ | $-1$ | $-e_1$ |
| **$e_{123}$ (7)**| $+e_{123}$| $+e_{23}$ | $-e_{13}$ | $+e_{12}$ | $-e_3$ | $+e_2$ | $-e_1$ | $-1$ |

---

## 2. Operation Coverage Matrix

| Opcode | Operation | Mathematical Formula | Test Vector IDs | Basis Coverage | Status Coverage |
|:---:|:---|:---|:---:|:---:|:---:|
| **0x01** | Geometric Product | $C = A B$ | #1 – #64, #260–#264 | 64/64 (100%) | `OK`, `OVERFLOW` |
| **0x02** | Wedge Product | $C = A \wedge B$ | #65 – #128, #265–#269 | 64/64 (100%) | `OK`, `OVERFLOW` |
| **0x03** | Hestenes Inner | $C = A \cdot B$ | #129 – #192, #270–#274 | 64/64 (100%) | `OK`, `OVERFLOW` |
| **0x04** | Addition | $C = A + B$ | #193 – #196, #275 | All 8 blades | `OK`, `OVERFLOW` |
| **0x05** | Subtraction | $C = A - B$ | #197 – #200, #276 | All 8 blades | `OK`, `OVERFLOW` |
| **0x06** | Scalar Multiplication | $C = B_0 \cdot A$ | #201 – #208, #277 | All 8 blades | `OK`, `OVERFLOW` |
| **0x07** | Grade Projection | $C = \langle A \rangle_k$ | #209 – #216, #278 | Grades 0, 1, 2, 3 | `OK` |
| **0x08** | Reversion | $C = \widetilde{A}$ | #217 – #224, #279 | All 8 blades | `OK` |
| **0x09** | Grade Involution | $C = \widehat{A}$ | #225 – #232, #280 | All 8 blades | `OK` |
| **0x0A** | Clifford Conjugation | $C = \overline{A}$ | #233 – #240, #281 | All 8 blades | `OK` |
| **0x0B** | Sandwich Product | $C = A B \widetilde{A}$ | #241 – #248, #282 | Rotations $90^\circ, 180^\circ$ | `OK`, `OVERFLOW` |
| **0x0C** | Rotor Norm | $C[0] = \sum a_k^2$ | #249 – #256, #283 | Unit rotors, scaled | `OK`, `OVERFLOW` |
| **N/A** | Numeric Corners | Rounding / Saturation | #257 – #259 | Saturation bounds | `OVERFLOW` |
| **Invalid**| Invalid Opcode | Opcode $> 12$ | #284, #285 | Error trap | `ERR_OP` |
