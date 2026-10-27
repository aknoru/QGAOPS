# Research gap and hypotheses

Prior work establishes GA hardware compilation, native/configurable
coprocessors, application-specific datapaths, and the importance of HLS
resource-sharing choices. The supplied set does not establish a controlled
comparison on PYNQ-Z2 between a resource-shared sequential design and an
adaptive pipeline implementing the same Cl(3,0) contract, with AAMF isolated
as an ablation and transfer boundaries reported separately.

This motivates testable hypotheses, not a novelty claim:

- H1: Under equal arithmetic contract and workload, sharing reduces selected
  resource use but increases latency or reduces throughput; effect size is
  measured from synthesis and implementation reports.
- H2: An adaptive pipeline improves kernel throughput for sufficiently large
  batches, while transfer overhead can erase end-to-end gains for small batches.
- H3: An AAMF layout changes locality/buffering behavior measurably relative to
  a matched baseline; direction and magnitude are unknown before experiments.
- H4: Q16.16 passes the selected error criteria for bounded workloads only
  when intermediate saturation is absent or explicitly accounted for.

The contribution must therefore be framed as a reproducible evaluation and
design study unless later evidence supports a stronger claim.
