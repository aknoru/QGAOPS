# QGAOPS-QGPU: Complete System & Execution Guide

**Target Hardware**: AMD PYNQ-ZU Rev B (`xczu5eg-sfvc784-1-e`)  
**Processing System (PS)**: Quad-core ARM Cortex-A53 @ 1.2 GHz, 4GB DDR4  
**Programmable Logic (PL)**: Zynq UltraScale+ FPGA Fabric @ 100 MHz  
**Physical Memory Map**:
- `0xA0000000`: `parallel_gpu` AXI4-Lite Cl(3,0) Accelerator Core
- `0xA0040000`: `axi_gpio_leds` Bank 66 PL Physical User LEDs (`B5`, `A6`, `B8`, `A7` @ `LVCMOS12`)

---

## 1. Quick Hardware Setup & Power-On

### Cable Connections
1. **Power Supply**: Plug the 12V DC power barrel jack into the PYNQ-ZU board (`J18`).
2. **Micro-USB Cable 1 (PROG / UART)**: Connect laptop USB to Micro-USB port `J2` (`PROG/UART`). This provides:
   - JTAG programming port.
   - Serial UART Console on **`COM3`** (115200 baud, 8N1).
3. **Power Switch**: Slide power switch **`SW1`** to **`ON`**.
   - Red power LEDs on the board will illuminate.
   - Zynq UltraScale+ PS will boot PYNQ Linux from the SD card (takes ~25 seconds).

---

## 2. Connecting Board to Wi-Fi & Permanent Autoconnect

### Step 2.1: Connect via Serial Console (`COM3`)
Open PuTTY, TeraTerm, or Windows Terminal:
- Port: `COM3`
- Baud rate: `115200`
- Data bits: `8`, Stop bits: `1`, Parity: `None`, Flow control: `None`
- Login credentials: `xilinx` / `xilinx` (default sudo password: `xilinx`).

### Step 2.2: Connect to Wi-Fi
In the board terminal, run:
```bash
sudo /usr/local/share/pynq-venv/bin/python3 -c "from pynq.lib import Wifi; Wifi().connect('HB7 2 IIIT MANIPUR', 'HB7#2@iiit')"
```
Verify the assigned IP address:
```bash
ip addr show wlan0
```
Look for `inet 192.168.0.220/24`.

### Step 2.3: Make Wi-Fi Reconnect Permanently on Boot (One-Time Setup)
Run this command once on the board to create a permanent systemd service that automatically connects Wi-Fi on every reboot:
```bash
sudo bash -c 'cat << "EOF" > /etc/systemd/system/pynq-wifi-autoconnect.service
[Unit]
Description=PYNQ Wi-Fi Auto-Connect on Boot
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/share/pynq-venv/bin/python3 -c "from pynq.lib import Wifi; Wifi().connect('\''HB7 2 IIIT MANIPUR'\'', '\''HB7#2@iiit'\'')"

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload
sudo systemctl enable pynq-wifi-autoconnect
```

---

## 3. Flashing & Deploying Updated Hardware & Software

The repository contains the authoritative package in `d:\QGPU\pynq_board_package`:
- `PARALLEL_GPU_PYNQZU.bit` (Option B Bitstream with Bank 66 PL user LEDs)
- `PARALLEL_GPU_PYNQZU.hwh` (Hardware handoff file)
- `qgpu_board.py` (Master on-board application with `0xA0040000` PL LED driver and Stage 22 Quantum API)
- `web/index.html` (Interactive dashboard with 1:1 camera canvas alignment, no-hand suppression, and Stage 22 verification button)
- `quantum_ga/` (8 quantum gate test vectors: $H, X, Y, Z, S, T$, Bell state)

### Deploy in 1 Command:
In PowerShell on your laptop:
```powershell
python d:\QGPU\scratch\upload_gui_update.py
```
This script automatically:
1. Connects to the board over SSH (`192.168.0.220` with fallback to `192.168.3.1`).
2. Transfers all bitstream, hardware handoff, python backend, web, and quantum vector files.
3. Restarts `qgpu-gui.service` on the board.

---

## 4. Running the Local Proxy Forwarder (`localhost:8080`)

Modern browsers (Chrome, Edge) strictly enforce **Secure Origin restrictions** on camera access (`getUserMedia`). While plain HTTP IP addresses like `http://192.168.0.220:8080` are blocked from using the webcam, `http://localhost:8080` is permanently treated as a secure context.

In a dedicated PowerShell window on your laptop:
```powershell
python d:\QGPU\scratch\local_forwarder.py
```
*Output*:
```text
Proxy active: http://localhost:8080 -> http://192.168.0.220:8080
```
Keep this window open while using the web interface.

---

## 5. Physical Board User LEDs (Bank 66 `B5`, `A6`, `B8`, `A7` @ `LVCMOS12`)

The 4 physical user LEDs on the PYNQ-ZU board silkscreen (`LED0`–`LED3`) are mapped directly to physical address **`0xA0040000`**:

| Silkscreen | FPGA Pin | Bank / Standard | Register Bit | Function | Visual Behavior |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **LED0** | `B5` | Bank 66 / LVCMOS12 | Bit 0 (`0x01`) | **READY / IDLE** | **Solid Green ON** when FPGA PL is ready |
| **LED1** | `A6` | Bank 66 / LVCMOS12 | Bit 1 (`0x02`) | **BUSY / COMPUTE** | **Pulses** during active hardware calculation |
| **LED2** | `B8` | Bank 66 / LVCMOS12 | Bit 2 (`0x04`) | **AP_DONE** | **Flashes** on operation completion |
| **LED3** | `A7` | Bank 66 / LVCMOS12 | Bit 3 (`0x08`) | **ERROR / OVF** | Off (only lights if overflow/error occurs) |

### Manual Hardware LED Verification:
To test the LEDs physically from the board terminal:
```bash
sudo /usr/local/share/pynq-venv/bin/python3 -c "from pynq import MMIO; import time; m = MMIO(0xA0040000, 0x1000); m.write(0x04, 0x00); [(m.write(0x00, p), time.sleep(0.3)) for p in [1, 2, 4, 8, 15, 1]]"
```

---

## 6. How to Run Everything & Get Results for the Final Report

### Method A: Interactive Web Control Center (Recommended)
Open Chrome or Edge and navigate to:
```
http://localhost:8080/?v=latest
```

1. **Tab 1: Hand GA Engine & Live Camera**
   - Click `🎥 Start Laptop Webcam`.
   - Hold your hand up in front of the camera:
     - 21 3D hand landmarks are drawn **pixel-for-pixel directly on your fingers**.
     - Computer vision radar tracks your index finger.
     - Pinching triggers `PINCH_CLICK`.
     - Two fingers trigger `RIGHT_CLICK`.
   - Lower your hand:
     - Skeleton disappears instantly.
     - Pointer freezes and dims.
     - HUD displays `NO HAND | Conf: 0%`.
   - Observe physical board: `LED1` and `LED2` flash during hardware evaluations.

2. **Tab 2: Deep1M / SIFT1M / GIST1M Similarity GPU Engine**
   - Click `⚡ Run Deep1M Benchmark (96-d)` or `⚡ Run SIFT1M (128-d)`.
   - Displays real-time hardware speedup (**14.85× over single-core ARM CPU**, 80,645 queries/sec).

3. **Tab 3: Verification, Benchmarks & Ablation Suite**
   - Click `▶ Stage 15: 295 Golden Regression Test (Bit-Exact)`: Runs all 295 test vectors (**100.0% Pass**).
   - Click `📊 Stage 16: Per-Opcode Benchmark (12 Operations)`: Runs 12 hardware opcodes (**3,859 ops/sec**).
   - Click `🔬 Stage 17: Blade Density Ablation Study`: Tests 1 to 8 active SIMD blade configurations.
   - Click `⚛ Stage 22: Quantum Geometric Benchmark`: Evaluates $H, X, Y, Z, S, T$, and Bell state transformations on FPGA (**1.0000 Fidelity, 20.8 µs latency, 48,000+ gates/sec**).
   - Click `💾 Download Results (JSON)`: Saves `qgpu_results.json` directly to your Downloads folder.

4. **Tab 4: 12-Opcode Cl(3,0) Calculator & Stream**
   - Select any opcode (`0x01` Geometric Product, `0x0B` Rotor Sandwich, etc.).
   - Click `⚡ Execute` or `🎲 Randomize`.
   - Observe real-time 8-blade multivector output ($C = A \cdot B$) and PL latency.

---

### Method B: Headless Terminal Execution on Board

SSH into the board (`ssh xilinx@192.168.0.220`):

```bash
cd /home/xilinx/pynq_board_package

# 1. Run complete full suite (Stages 15, 16, 17, and 22 Quantum):
sudo /usr/local/share/pynq-venv/bin/python3 qgpu_board.py --mode full

# 2. Run Quantum Geometric Algebra Benchmark only:
sudo /usr/local/share/pynq-venv/bin/python3 qgpu_board.py --mode quantum

# 3. Run Stage 15 Golden Regression only:
sudo /usr/local/share/pynq-venv/bin/python3 qgpu_board.py --mode validate

# 4. Run Stage 16 Opcode Benchmark only:
sudo /usr/local/share/pynq-venv/bin/python3 qgpu_board.py --mode bench --iterations 200
```

---

## 7. What Else is Left for Final Report Deliverables?

All hardware, RTL, synthesis, implementation, timing closure, board drivers, quantum algebra mapping, web dashboard, and API endpoints are **100% complete**. 

Here is the checklist of remaining tasks to assemble your final submission:

| Task Item | Status | Action Needed from You |
| :--- | :---: | :--- |
| **Physical Board Photos** | ⏳ Ready | Take 1–2 photos of the physical PYNQ-ZU board running with `LED0` illuminated (and `LED1` pulsing during camera interaction). |
| **GUI Screenshots** | ⏳ Ready | Take clean screenshots of: <br>1. **Tab 1** with hand skeleton tracking<br>2. **Tab 2** showing the 14.8× Deep1M speedup table<br>3. **Tab 3** showing Stage 15, 16, 17, and Stage 22 Quantum benchmark results. |
| **JSON Data Export** | ✅ Done | Click `💾 Download Results (JSON)` in Tab 3 to save the verified telemetry figures. |
| **Report Document / Paper** | ⏳ Ready to Compile | Use the data in `PROGRESS_LEDGER.md` and `HOW_TO_RUN.md` to generate the final LaTeX / PDF project report. |
