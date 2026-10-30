import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", 22, "xilinx", "xilinx", timeout=5)

remote_py = """
from pynq import MMIO
import time
try:
    led_mmio = MMIO(0xA0040000, 0x1000)
    led_mmio.write(0x04, 0x00) # Output
    print("[+] Successfully initialized AXI GPIO @ 0xA0040000")
    for pattern in [0x1, 0x2, 0x4, 0x8, 0xF, 0x1]:
        led_mmio.write(0x00, pattern)
        print("  PL LEDs pattern:", bin(pattern))
        time.sleep(0.4)
    print("[+] Test completed successfully.")
except Exception as e:
    print("[!] Error:", e)
"""

cmd = f"sudo /usr/local/share/pynq-venv/bin/python3 -c '{remote_py}'"
stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()

