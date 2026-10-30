import paramiko
import os
import sys
import time

CANDIDATE_IPS = ["10.51.10.38", "192.168.0.221", "192.168.0.220", "192.168.3.1"]
if len(sys.argv) > 1:
    CANDIDATE_IPS.insert(0, sys.argv[1])

ssh = None
target_ip = None

for ip in CANDIDATE_IPS:
    try:
        print(f"[*] Attempting SSH connection to {ip}:22...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username="xilinx", password="xilinx", timeout=4)
        ssh = client
        target_ip = ip
        print(f"[+] Successfully connected to board at {ip}!")
        break
    except Exception as e:
        print(f"[-] {ip} not reachable ({e})")

if not ssh:
    print("[ERROR] Could not connect to board on any candidate IP.")
    print("Please ensure board is powered on, connected via Wi-Fi (192.168.0.220) or USB (192.168.3.1).")
    sys.exit(1)

sftp = ssh.open_sftp()

print("\n[1/5] Uploading web/index.html (with fixed camera alignment & Stage 22)...")
sftp.put(r"D:\QGPU\pynq_board_package\web\index.html", "/home/xilinx/pynq_board_package/web/index.html")

print("[2/5] Uploading qgpu_board.py (with on-board Quantum Benchmarking & CLI)...")
sftp.put(r"D:\QGPU\pynq_board_package\qgpu_board.py", "/home/xilinx/pynq_board_package/qgpu_board.py")

print("[3/5] Uploading run.sh...")
sftp.put(r"D:\QGPU\pynq_board_package\run.sh", "/home/xilinx/pynq_board_package/run.sh")
try:
    sftp.put(r"D:\QGPU\pynq_board_package\run.sh", "/home/xilinx/run.sh")
except Exception: pass

print("[4/5] Uploading Option B bitstream & hardware handoff (.bit & .hwh)...")
sftp.put(r"D:\QGPU\pynq_board_package\PARALLEL_GPU_PYNQZU.bit", "/home/xilinx/pynq_board_package/PARALLEL_GPU_PYNQZU.bit")
sftp.put(r"D:\QGPU\pynq_board_package\PARALLEL_GPU_PYNQZU.hwh", "/home/xilinx/pynq_board_package/PARALLEL_GPU_PYNQZU.hwh")

print("[5/5] Uploading quantum_ga test vectors...")
try:
    sftp.mkdir("/home/xilinx/pynq_board_package/quantum_ga")
except Exception: pass

qga_dir = r"D:\QGPU\pynq_board_package\quantum_ga"
for f in os.listdir(qga_dir):
    src = os.path.join(qga_dir, f)
    dst = f"/home/xilinx/pynq_board_package/quantum_ga/{f}"
    sftp.put(src, dst)

sftp.close()

# Ensure permissions
ssh.exec_command("chmod +x /home/xilinx/run.sh /home/xilinx/pynq_board_package/run.sh")

# Kill any manual/rogue instances and restart qgpu-gui systemd unit cleanly
print("[*] Terminating any stale instances and restarting qgpu-gui.service on board...")
stdin, stdout, stderr = ssh.exec_command("echo xilinx | sudo -S pkill -9 -f qgpu_board.py; sleep 1; echo xilinx | sudo -S systemctl restart qgpu-gui")
stdout.channel.recv_exit_status()

ssh.close()
print(f"\nSUCCESS: Fully updated all hardware (.bit/.hwh), quantum gates, and web GUI on {target_ip}!")
