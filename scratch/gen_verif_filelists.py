from pathlib import Path

seq_dir = Path("D:/QGPU/HW/vitis/SEQ_GPU/work/hls/impl/verilog")
par_dir = Path("D:/QGPU/HW/vitis/PARALLEL_GPU/work/hls/impl/verilog")

seq_files = sorted([f.as_posix() for f in seq_dir.glob("*.v")])
par_files = sorted([f.as_posix() for f in par_dir.glob("*.v")])

with open("D:/QGPU/HW/vivado/verification/scripts/seq_gpu_verilog.f", "w") as f:
    for file in seq_files:
        f.write(f'"{file}"\n')

with open("D:/QGPU/HW/vivado/verification/scripts/parallel_gpu_verilog.f", "w") as f:
    for file in par_files:
        f.write(f'"{file}"\n')

print(f"Wrote {len(seq_files)} files to seq_gpu_verilog.f")
print(f"Wrote {len(par_files)} files to parallel_gpu_verilog.f")
