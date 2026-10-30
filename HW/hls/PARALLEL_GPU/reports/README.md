# PARALLEL_GPU Synthesis and Simulation Reports Directory

This directory is designated for archiving actual reports generated from the Vitis HLS GUI flow for `PARALLEL_GPU`.

## Expected Report Files

When the user runs C Synthesis and Implementation in Vitis HLS, copy the resulting reports here:

1. `parallel_gpu_csynth.rpt`: Synthesis summary report containing latency, clock frequency, initiation interval, and estimated utilization (LUT, FF, DSP, BRAM).
2. `parallel_gpu_csim.log`: Output transcript from C Simulation showing execution of all 285 test vectors.
3. `parallel_gpu_cosim.rpt`: (Optional) C/RTL co-simulation report validating cycle-accurate RTL behavior.

## Current Status: NOT RUN IN AGENT WORKFLOW

In accordance with Section 11 of the master prompt, automated background synthesis runs are NOT fabricated. Tool-dependent checks are marked **NOT RUN** until executed through the manual Vitis HLS GUI workflow detailed in [`../README.md`](file:///d:/QGPU/HW/hls/PARALLEL_GPU/README.md).
