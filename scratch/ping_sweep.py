import subprocess
import concurrent.futures
import re

def ping(ip):
    res = subprocess.run(["ping", "-n", "1", "-w", "200", ip], capture_output=True, text=True)
    return ip, res.returncode == 0

ips = [f"192.168.0.{i}" for i in range(1, 255)]
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
    results = list(ex.map(ping, ips))

alive = [ip for ip, ok in results if ok]
print("Alive IPs on 192.168.0.x:", alive)

# Now check arp -a
arp_out = subprocess.run(["arp", "-a"], capture_output=True, text=True).stdout
print(arp_out)

