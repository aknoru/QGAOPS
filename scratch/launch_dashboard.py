import sys
import time
import subprocess
import webbrowser
import requests
import re

print("==================================================")
print("     QGPU Automated Board Connector & Launcher    ")
print("==================================================")

CANDIDATES = ["10.51.10.38", "192.168.0.220", "192.168.0.221", "192.168.3.1"]

def test_ip(ip):
    for endpoint in ["/api/status", "/"]:
        try:
            r = requests.get(f"http://{ip}:8080{endpoint}", timeout=2.0)
            if r.status_code == 200:
                return True
        except Exception:
            pass
    return False

board_ip = None

# 1. Quick check known candidates
print("[*] Probing known IP addresses...")
for ip in CANDIDATES:
    if test_ip(ip):
        board_ip = ip
        break

# 2. If not found, sweep local subnet
if not board_ip:
    print("[*] Not found on quick cache. Checking local network...")
    # Find current local IP
    ipconfig = subprocess.run(["ipconfig"], capture_output=True, text=True).stdout
    matches = re.findall(r"IPv4 Address[ .:]+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", ipconfig)
    for local_ip in matches:
        if local_ip.startswith("127."):
            continue
        prefix = ".".join(local_ip.split(".")[:3])
        print(f"[*] Scanning subnet {prefix}.0/24...")
        import concurrent.futures
        def check(i):
            probe_ip = f"{prefix}.{i}"
            return probe_ip if test_ip(probe_ip) else None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=40) as ex:
            for res in ex.map(check, range(1, 255)):
                if res:
                    board_ip = res
                    break
        if board_ip:
            break

if not board_ip:
    print("\n[!] Could not locate board on the network.")
    print("Please ensure:")
    print(" 1. Phone hotspot 'OPEN' is turned ON (Security: WPA2-Personal).")
    print(" 2. Board is powered on and PL LED0 (READY) is illuminated.")
    print(" 3. Laptop Wi-Fi is connected to 'OPEN'.")
    input("\nPress Enter to exit...")
    sys.exit(1)

print(f"\n[+] Board detected at: http://{board_ip}:8080")
print("[*] Launching local proxy and dashboard...")

# Start forwarder in background if needed
url = f"http://{board_ip}:8080/?v=latest"
webbrowser.open(url)

print("\n==================================================")
print(f" SUCCESS! Dashboard opened at:")
print(f" {url}")
print("==================================================")
time.sleep(3)

