import os
from pathlib import Path

v_dir = Path("D:/QGPU/HW/vitis/SEQ_GPU/work/hls/impl/verilog")
files = sorted([f.as_posix() for f in v_dir.glob("*.v")])
with open("D:/QGPU/scratch/seq_gpu_files.f", "w") as f:
    for file in files:
        f.write(f'"{file}"\n')

print(f"Wrote {len(files)} files to seq_gpu_files.f")
