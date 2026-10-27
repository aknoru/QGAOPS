"""Benchmark CLI entry point — python -m software.benchmarks"""
from software.benchmarks.workloads import WorkloadConfig
from software.benchmarks.runner import run, write_result
from pathlib import Path
import sys

def main():
    ops   = ["geometric_product", "wedge", "hestenes_inner", "add", "subtract"]
    dists = ["dense", "sparse", "boundary"]
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 128
    reps  = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    out_dir = Path("results/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Running {len(ops)*len(dists)} benchmark configs ({count} pairs × {reps} reps)...")
    for op in ops:
        for dist in dists:
            cfg = WorkloadConfig(operation=op, count=count, seed=20261026, distribution=dist)
            result = run(cfg, repetitions=reps, warmup=1)
            out = out_dir / f"bench_{op}_{dist}.json"
            write_result(result, out)
            fp_ops = result["floating_point"]["operations_per_second_median"]
            fx_ops = result["fixed_point"]["operations_per_second_median"]
            print(f"  {op:20s} {dist:10s}  FP={fp_ops:8,.0f} ops/s  FX={fx_ops:8,.0f} ops/s")
    print(f"Done. Results in {out_dir.resolve()}")

if __name__ == "__main__":
    main()
