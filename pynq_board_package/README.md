# QGAOPS-QGPU: PYNQ-ZU Board Deployment Package

This is the **single, self-contained deployment package** to copy to your AMD PYNQ-ZU Rev B board. All previous and conflicting versions have been removed.

---

## Package Contents

```
pynq_board_package/
├── PARALLEL_GPU_PYNQZU.bit    # Hardware bitstream (Cl(3,0) accelerator @ 100 MHz)
├── PARALLEL_GPU_PYNQZU.hwh    # Hardware handoff specification (used by PYNQ)
├── golden_vectors_295.json    # 295 regression verification test vectors
├── qgpu_board.py              # Unified master Python application (Stages 15-19)
├── run.sh                     # One-line bash launcher script
├── web/
│   └── index.html             # Interactive browser dashboard (Port 8080)
└── README.md                  # This guide
```

---

## Step 1: Copy Package to PYNQ-ZU Board

From your laptop Windows PowerShell (ensure board is booted with PYNQ Ubuntu SD card):

```powershell
# Copy the entire folder to the board:
scp -r d:\QGPU\pynq_board_package xilinx@192.168.0.220:/home/xilinx/
```
*(Default password: `xilinx`)*

---

## Step 2: SSH into Board

```bash
ssh xilinx@192.168.0.220
cd /home/xilinx/pynq_board_package
chmod +x run.sh qgpu_board.py
```

---

## Step 3: Run Modes

### Option A: Interactive Web GUI (Recommended)
Launch the built-in web server:
```bash
./run.sh --mode gui
```
Then open your laptop browser at:
👉 **`http://192.168.0.220:8080`**

From the web dashboard you can:
- **Execute any of the 12 Cl(3,0) Geometric Algebra operations** directly on the FPGA
- **Randomize multivectors A & B** and view all 8 blades of result C in real-time
- **Monitor the 4 hardware PL LEDs**
- **Trigger Stage 15 Validation**, **Stage 16 Benchmark**, or **Continuous Synthetic Stream** with one click
- **Download benchmark results** as JSON

---

### Option B: Command-Line Benchmarking

```bash
# 1. Run Complete Pipeline (Stages 15, 16, and 17):
./run.sh --mode full

# 2. Stage 15 Only: 295 Golden Vector Regression Test
./run.sh --mode validate

# 3. Stage 16 Only: Per-Opcode Latency & Throughput Benchmark
./run.sh --mode bench --iterations 200

# 4. Stage 17 Only: Blade Density Ablation Study
./run.sh --mode ablate

# 5. Continuous Synthetic Multivector Stream (Hardware stress test):
./run.sh --mode synthetic --iterations 100
```

---

### Option C: Live Webcam Streaming (Stage 18)
If you want to stream real hand landmarks from your laptop camera over Wi-Fi:

1. **On the board**:
   ```bash
   ./run.sh --mode server
   ```
2. **On your laptop** (Windows):
   ```powershell
   python d:\QGPU\laptop_camera.py --board 192.168.0.220
   ```

---

## Results Output
When benchmarks finish, output files are automatically saved to:
`pynq_board_package/results/`
- `stage15_validation.json` (Golden test regression summary)
- `stage16_benchmark.json` and `stage16_benchmark.csv` (Per-opcode timings)
- `stage17_ablation.json` (Blade density scaling study)
