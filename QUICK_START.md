# Super Simple Quick Start (2 Steps)

Use your **Laptop Webcam** for input and get the real-time **FPGA Result Blades** on your screen!

---

### Step 1: On the FPGA Board
Open a terminal on your PYNQ board and run:
```bash
python board_server.py
```
*The FPGA bitstream loads, and **LED0 (Ready)** turns on.*

---

### Step 2: On Your Laptop
In PowerShell or Command Prompt, run:
```powershell
python laptop_camera.py --board 192.168.2.99
```
*(Replace `192.168.2.99` with your PYNQ board's IP address, or just run `python laptop_camera.py` for standalone mode)*

---

### What happens automatically:
1. Your laptop camera window opens immediately.
2. Hold your hand in front of the camera:
   - Tracks your hand skeleton in 3D.
   - Calculates the palm plane and normal orientation.
   - Converts the hand geometry into Signed Q16.16 Fixed-Point Multivectors.
3. Sends the vectors to the FPGA board.
4. **Board LED1 (Processing) GLOWS ON** while the FPGA accelerator computes the geometric product!
5. **Board LED2 (Success) pulses ON** when the computation completes.
6. The **8 FPGA Result Blades ($c_0$ to $c_7$)** and the **Detected Gesture** are displayed live on your laptop screen!
7. Press **`q`** or **`ESC`** in the video window to quit.
