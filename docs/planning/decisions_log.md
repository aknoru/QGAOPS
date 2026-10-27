# Decisions and unresolved items

## Selected decisions

1. Use Euclidean Cl(3,0) with `e_i^2=+1`.
2. Use basis masks and the fixed coefficient order in the master prompt.
3. Use the Hestenes inner product `sum_{k=0}^min(r,s) <A_r B_s>_{s-r}` for
   homogeneous grades, extended bilinearly.
4. Start evaluation with signed Q16.16 and round-to-nearest-even with
   saturation plus an explicit overflow flag.
5. Treat AAMF and both hardware variants as proposed until measured.
6. Stage 4 uses arbitrary-precision Python accumulation for fixed-point sums
   of signed 64-bit products. This is a reference-model decision; hardware
   accumulator width remains a Stage 5 design decision.
7. Stage 5 proposes a signed 66-bit raw accumulator for the current
   eight-term-per-output Cl(3,0) bound; Stage 10 must verify it in HLS.
8. Stages 6–8 use standard-library JSON/HTTP components because optional
   scientific/web dependencies are not installed; camera and public dataset
   support remain optional.

## Unresolved decisions

- Obtain the three named project documents absent from the workspace.
- Decide the final DMA versus memory-mapped/streaming interface after bandwidth
  analysis.
- Confirm whether the benchmark requires scalar, vector, rotor, or mixed
  multivector distributions.
- Establish workload-derived fixed-point range and whether wider intermediates
  are required.
- Define the exact AAMF storage layout and arbitration policy.
- Select the final clock and Vivado/Vitis tool versions.
