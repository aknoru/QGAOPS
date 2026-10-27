import json
from pathlib import Path
from software.benchmarks.runner import run, write_result
from software.benchmarks.workloads import WorkloadConfig

root = Path(__file__).resolve().parents[1]
config_data = json.loads((root / "configs/benchmarks/default.json").read_text(encoding="utf-8"))
repetitions = config_data.pop("repetitions")
warmup = config_data.pop("warmup")
result = run(WorkloadConfig(**config_data), repetitions=repetitions, warmup=warmup)
write_result(result, root / "results/raw/stage6_cpu_benchmark.json")
print("wrote results/raw/stage6_cpu_benchmark.json")
