# Worked examples

With coefficient vectors in the specified order:

1. `e1 e2 = e12`, while `e2 e1 = -e12`.
2. `(1+e1)(1+e2) = 1+e1+e2+e12`.
3. `e12 ^ e1 = 0` because the masks overlap.
4. `e1 ^ e23 = e123`; `e23 ^ e1 = e123` because grades 1 and 2 commute
   under the graded outer-product sign `(-1)^(1*2)`.
5. `reverse(e12)=-e12`, `involution(e12)=e12`, and
   `conjugation(e12)=-e12`.
6. Under the selected left Hestenes contraction,
   `e1 · e12 = e2` (grade `2-1=1`), while `e12 · e1 = 0`.

These examples are intentionally small enough to reproduce by hand and form
the seed cases for the future independent software reference.
