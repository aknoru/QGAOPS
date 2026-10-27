# Cl(3,0) mathematical contract

## Basis and masks

The ordered basis is

`0:1, 1:e1, 2:e2, 3:e3, 4:e12, 5:e13, 6:e23, 7:e123`.

Blade `e_S` is represented by a three-bit mask whose bit `i` indicates `e_i`.
The coefficient vector is `A[0..7]`; mask values are respectively
`0,1,2,4,3,5,6,7`. Grade is `popcount(mask)`.

## Metric and blade product

The metric is diagonal Euclidean: `e_i e_i = +1`, and distinct basis vectors
anticommute. For masks `a,b`, the product mask is `a xor b`. The sign is
`(-1)^N`, where `N` is the number of pairs `(i,j)` with bit `i` set in `a`,
bit `j` set in `b`, and `i > j`, using index order `e1,e2,e3`. Thus
`e12 e1 = -e2`, `e1 e12 = e2`, and `e123^2 = -1`.

For general multivectors, `AB = sum_{a,b} A[a]B[b] blade(a)blade(b)`.
This finite sum is the normative geometric product.

## Operations

Addition, subtraction, and scalar multiplication are coefficient-wise.
The outer product is `A ^ B = sum <A[a]B[b] blade(a)blade(b)>_{grade(a)+grade(b)}`,
so terms with overlapping masks vanish. Grade projection keeps only a chosen
grade. Reverse multiplies a grade-r blade by `(-1)^(r(r-1)/2)`.
Grade involution multiplies grade-r terms by `(-1)^r`. Clifford conjugation
is their composition, with factor `(-1)^(r(r+1)/2)`.

For homogeneous `A_r,B_s`, the Hestenes inner product is
`A_r · B_s = <A_r B_s>_{s-r}` when `r <= s`, and zero otherwise. For
inhomogeneous inputs it is extended bilinearly over homogeneous components.
This is the selected left contraction convention; right contraction is not
silently substituted.

The pseudoscalar is `I=e123`, `I^2=-1`; duality, when later required, is
defined as right multiplication by `I^{-1}=-I`, with the exact operation
recorded in the call contract.

## Algebraic validation

Independent checks must cover basis products, bilinearity, associativity of
the geometric product, `A^~~=A`, involution composition, grade projection
idempotence, `A^B=B^A` for the outer product up to the expected graded sign,
and `A^B=0` for overlapping basis masks. Floating-point reference checks use
exact symbolic signs before numerical tolerance is applied.
