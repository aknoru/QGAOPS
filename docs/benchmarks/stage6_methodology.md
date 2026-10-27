# Stage 6 benchmark methodology

`software.benchmarks` generates deterministic scalar, basis, sparse, dense,
boundary, and random workloads from a versioned configuration and seed.
`scripts/run_benchmark.py` measures floating-point and fixed-point reference
batch execution with `perf_counter_ns`, warm-up, repeated samples, median,
mean, standard deviation, p95, and operations/second.

The measurement boundary is Python reference operation execution only.
Conversion, filesystem, dashboard, FPGA, DMA, and physical-board timings are
excluded. These are CPU software baselines and must not be presented as FPGA
performance.

Run:

```powershell
.\.venv\Scripts\python.exe scripts\run_benchmark.py
```
