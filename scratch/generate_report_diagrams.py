import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

OUT_DIR = "d:/QGPU/FINAL REPORT/images"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Gantt Chart
def gen_gantt():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    stages = [
        "Phase 1: Cl(3,0) Modeling & Contract",
        "Phase 2: HLS Sequential & Parallel IP",
        "Phase 3: Vivado AXI SMC & Timing",
        "Phase 4: PYNQ-ZU PL Bringup & LEDs",
        "Phase 5: Datasets, Vision & Quantum GA",
        "Phase 6: ZedBoard Dual-Flow & Bitstream"
    ]
    starts = [1, 3, 6, 8, 10, 12]
    durations = [2.5, 3.5, 2.5, 2.5, 2.5, 1.5]
    colors = ['#2563eb', '#06b6d4', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']

    y_pos = np.arange(len(stages))
    ax.barh(y_pos, durations, left=starts, align='center', color=colors, edgecolor='black', height=0.55)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages, fontsize=12, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel('Project Timeline (Weeks)', fontsize=12, fontweight='bold')
    ax.set_title('QGAOPS-QGPU: Complete Project Schedule Gantt Chart (Phases 1-6)', fontsize=15, fontweight='bold', pad=15)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "gantt_chart_master.png"))
    plt.close()

# 2. Hardware Resource Comparison
def gen_resource_cmp():
    labels = ['LUTs (%)', 'Registers (%)', 'DSPs (%)', 'Clock (MHz)', 'Dynamic Power (W)']
    pynq_seq = [13.0, 8.6, 1.3, 100, 0.69]
    pynq_par = [34.0, 12.0, 66.7, 100, 1.27]
    zed_seq = [6.7, 3.3, 5.5, 100, 1.59]
    
    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.bar(x - width, pynq_seq, width, label='PYNQ-ZU SEQ_GPU', color='#06b6d4')
    ax.bar(x, pynq_par, width, label='PYNQ-ZU PARALLEL_GPU', color='#2563eb')
    ax.bar(x + width, zed_seq, width, label='ZedBoard SEQ_GPU_ZED', color='#10b981')

    ax.set_ylabel('Utilization (%) / Power (W)', fontsize=12, fontweight='bold')
    ax.set_title('Cross-Platform FPGA Resource Utilization Matrix (PYNQ-ZU vs ZedBoard)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "resource_comparison_chart.png"))
    plt.close()

# 3. Kernel Compute Speedup vs CPU
def gen_speedup_chart():
    benchmarks = ['Geometric Product', 'Rotor Sandwich', 'Wedge Product', 'Inner Product', 'Deep1M Batch', 'SIFT1M Batch', 'GIST1M Batch']
    speedups = [2186.0, 2256.0, 1945.0, 2012.0, 14.85, 14.91, 14.92]
    colors = ['#ec4899', '#ec4899', '#ec4899', '#ec4899', '#06b6d4', '#06b6d4', '#06b6d4']

    fig, ax = plt.subplots(figsize=(13, 6), dpi=300)
    bars = ax.bar(benchmarks, speedups, color=colors, width=0.55, edgecolor='black')
    ax.set_yscale('log')
    ax.set_ylabel('Speedup Factor vs ARM Cortex CPU (Log Scale)', fontsize=12, fontweight='bold')
    ax.set_title('QGPU Hardware Acceleration Speedup: Raw Kernel Compute vs High-Dim Datasets', fontsize=14, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=20, ha='right', fontsize=11, fontweight='bold')

    for bar, val in zip(bars, speedups):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval * 1.2, f"{val:.1f}x", ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "kernel_speedup_comparison.png"))
    plt.close()

# 4. Quantum Fidelity & Gate Latency
def gen_quantum_chart():
    gates = ['Hadamard (H)', 'Pauli-X', 'Pauli-Y', 'Pauli-Z', 'Phase (S)', 'Pi/8 (T)', 'Bell State']
    latencies = [258.77, 260.72, 255.72, 256.54, 256.73, 257.66, 255.57]

    fig, ax = plt.subplots(figsize=(11, 5), dpi=300)
    ax.plot(gates, latencies, marker='o', linewidth=2.5, markersize=8, color='#8b5cf6')
    ax.set_ylabel('Hardware Execution Latency (µs)', fontsize=12, fontweight='bold')
    ax.set_ylim(240, 280)
    ax.set_title('Quantum Geometric Algebra (QGA) Single-Qubit & Bell Gate Latencies (Fidelity = 1.0000)', fontsize=13, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=25, ha='right', fontsize=11, fontweight='bold')
    for x, y in enumerate(latencies):
        ax.text(x, y + 2, f"{y:.1f} µs", ha='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "quantum_gate_latencies.png"))
    plt.close()

gen_gantt()
gen_resource_cmp()
gen_speedup_chart()
gen_quantum_chart()
print("Generated high-res visual diagrams!")

