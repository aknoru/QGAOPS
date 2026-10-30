import os
from pathlib import Path

v_dir = Path("D:/QGPU/HW/vitis/PARALLEL_GPU/work/hls/impl/verilog")
files = sorted([f.as_posix() for f in v_dir.glob("*.v")])
with open("D:/QGPU/scratch/parallel_gpu_files.f", "w") as f:
    for file in files:
        f.write(f'"{file}"\n')

print(f"Wrote {len(files)} files to parallel_gpu_files.f")
