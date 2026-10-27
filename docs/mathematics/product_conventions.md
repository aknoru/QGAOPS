# Product conventions

All operations are coefficient-vector operations over the basis table. The
geometric product is the primitive operation; outer product and Hestenes
inner product are grade-filtered variants. Grade-zero inputs obey the same
rules: `a·B` keeps grade `grade(B)` and `B·a` is zero under the selected left
contraction definition when `B` has positive grade. This asymmetry is
intentional and must be tested.

The reverse, grade involution, and Clifford conjugation factors are:

| grade r | reverse | involution | conjugation |
|---:|---:|---:|---:|
| 0 | + | + | + |
| 1 | + | - | - |
| 2 | - | + | - |
| 3 | - | - | + |

No duality or division operation is part of the initial hardware contract.
If introduced later, pseudoscalar invertibility and zero norm behavior must be
specified before implementation.
