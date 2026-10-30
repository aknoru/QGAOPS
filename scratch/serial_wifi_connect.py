import serial
import time
import sys
import re

class SerialShell:
    def __init__(self, port='COM3', baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1.0)
        time.sleep(0.5)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ensure_prompt()

    def read_all(self, wait=0.5):
        time.sleep(wait)
        out = b""
        while self.ser.in_waiting:
            out += self.ser.read(self.ser.in_waiting)
            time.sleep(0.1)
        return out.decode('utf-8', errors='ignore')

    def ensure_prompt(self):
        self.ser.write(b"\r\n")
        res = self.read_all(0.5)
        if "login:" in res:
            self.ser.write(b"xilinx\r\n")
            time.sleep(1)
            self.ser.write(b"xilinx\r\n")
            time.sleep(1)
            res = self.read_all(0.5)
        # Prime sudo
        self.ser.write(b"echo xilinx | sudo -S whoami\r\n")
        time.sleep(1.0)
        res = self.read_all(0.5)
        print("Sudo prime output:", res.strip())

    def run_cmd(self, cmd, timeout=15):
        print(f"\n>>> Running: {cmd}")
        self.ser.write(f"{cmd}\r\n".encode('utf-8'))
        start = time.time()
        buf = ""
        while time.time() - start < timeout:
            if self.ser.in_waiting:
                chunk = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
                buf += chunk
                sys.stdout.write(chunk)
                sys.stdout.flush()
                if "xilinx@pynq:" in buf and buf.strip().endswith("$"):
                    break
            time.sleep(0.1)
        return buf

    def close(self):
        self.ser.close()

def main():
    sh = SerialShell('COM3', 115200)

    # 1. Stop existing wpa_supplicant and dhclient
    sh.run_cmd("sudo pkill -9 wpa_supplicant", timeout=5)
    sh.run_cmd("sudo pkill -9 dhclient", timeout=5)

    # 2. Configure /etc/wpa_supplicant.conf strictly for OPEN
    wpa_conf = (
        "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n"
        "update_config=1\n"
        "\n"
        "network={\n"
        "    ssid=\"OPEN\"\n"
        "    psk=\"FUKCYOUBITCH\"\n"
        "    key_mgmt=WPA-PSK\n"
        "}\n"
    )
    sh.run_cmd("sudo rm -f /etc/wpa_supplicant.conf", timeout=5)
    sh.run_cmd(f"echo '{wpa_conf}' | sudo tee /etc/wpa_supplicant.conf", timeout=5)
    sh.run_cmd("sudo cp /etc/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf", timeout=5)

    # 3. Create persistent autoconnect script
    script_content = (
        "#!/bin/bash\n"
        "echo '[wifi-autoconnect] Starting Wi-Fi for OPEN...'\n"
        "pkill -9 wpa_supplicant\n"
        "pkill -9 dhclient\n"
        "ip link set wlan0 up\n"
        "sleep 1\n"
        "wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf\n"
        "sleep 4\n"
        "dhclient -v wlan0\n"
        "echo '[wifi-autoconnect] Connected to:'\n"
        "ip addr show wlan0\n"
    )
    sh.run_cmd(f"echo '{script_content}' | sudo tee /usr/local/bin/wifi-autoconnect.sh", timeout=5)
    sh.run_cmd("sudo chmod +x /usr/local/bin/wifi-autoconnect.sh", timeout=5)

    # 4. Create systemd service for boot autoconnect
    service_content = (
        "[Unit]\n"
        "Description=PYNQ Wi-Fi Autoconnect to OPEN\n"
        "After=network.target\n"
        "\n"
        "[Service]\n"
        "Type=oneshot\n"
        "ExecStart=/usr/local/bin/wifi-autoconnect.sh\n"
        "RemainAfterExit=yes\n"
        "\n"
        "[Install]\n"
        "WantedBy=multi-user.target\n"
    )
    sh.run_cmd(f"echo '{service_content}' | sudo tee /etc/systemd/system/pynq-wifi-autoconnect.service", timeout=5)
    sh.run_cmd("sudo systemctl daemon-reload", timeout=5)
    sh.run_cmd("sudo systemctl enable pynq-wifi-autoconnect.service", timeout=5)

    # 5. Connect right now
    print("\n================ STARTING WI-FI CONNECTION ================")
    sh.run_cmd("sudo ip link set wlan0 down", timeout=5)
    time.sleep(1)
    sh.run_cmd("sudo ip link set wlan0 up", timeout=5)
    time.sleep(1)
    sh.run_cmd("sudo wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf", timeout=10)
    
    print("\nWaiting for WPA association...")
    for i in range(10):
        time.sleep(2)
        out = sh.run_cmd("sudo wpa_cli -i wlan0 status", timeout=5)
        if "wpa_state=COMPLETED" in out:
            print("\n*** WPA State: COMPLETED! Connected to SSID OPEN! ***")
            break
        else:
            print(f"Waiting... (attempt {i+1}/10)")

    # 6. Request IP via dhclient
    print("\nRequesting DHCP lease...")
    sh.run_cmd("sudo dhclient -v wlan0", timeout=15)
    
    # 7. Check final IP
    ip_info = sh.run_cmd("ip addr show wlan0", timeout=5)
    match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", ip_info)
    if match:
        ip = match.group(1)
        print(f"\n\n==========================================")
        print(f" SUCCESS! Board connected to OPEN!")
        print(f" Board IP Address: {ip}")
        print(f"==========================================\n")
    else:
        print("\nCould not find inet IP address in output.")

    # 8. Check GUI service status and restart it to bind cleanly
    sh.run_cmd("sudo systemctl restart qgpu-gui", timeout=10)
    sh.run_cmd("sudo systemctl status qgpu-gui --no-pager", timeout=5)

    sh.close()

if __name__ == '__main__':
    main()

