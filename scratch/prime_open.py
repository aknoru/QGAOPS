import serial
import time
import sys

def main():
    ser = serial.Serial('COM3', 115200, timeout=1.0)
    time.sleep(0.5)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    def run_cmd(cmd, timeout=15):
        print(f"\n>>> Running: {cmd}")
        ser.write(f"{cmd}\r\n".encode('utf-8'))
        start = time.time()
        buf = ""
        while time.time() - start < timeout:
            if ser.in_waiting:
                chunk = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                buf += chunk
                sys.stdout.write(chunk)
                sys.stdout.flush()
                if "xilinx@pynq:" in buf and buf.strip().endswith("$"):
                    break
            time.sleep(0.1)
        return buf

    run_cmd("echo xilinx | sudo -S whoami")
    
    # 1. Clean interfaces and set up wlan0 interface file
    interfaces_wlan0 = (
        "auto wlan0\n"
        "allow-hotplug wlan0\n"
        "iface wlan0 inet dhcp\n"
        "    wpa-ssid \"OPEN\"\n"
        "    wpa-psk \"FUKCYOUBITCH\"\n"
        "    wpa-scan-ssid 1\n"
    )
    run_cmd(f"echo '{interfaces_wlan0}' | sudo tee /etc/network/interfaces.d/wlan0")

    # 2. Set up standalone wpa_supplicant.conf
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
    run_cmd(f"echo '{wpa_conf}' | sudo tee /etc/wpa_supplicant.conf")
    run_cmd("sudo cp /etc/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf")

    # 3. Create background looping connector script
    loop_script = (
        "#!/bin/bash\n"
        "while true; do\n"
        "    if ! ip addr show wlan0 | grep -q 'inet '; then\n"
        "        echo '[autoconnect] wlan0 has no IP, attempting connection to OPEN...'\n"
        "        pkill -9 wpa_supplicant 2>/dev/null\n"
        "        pkill -9 dhclient 2>/dev/null\n"
        "        ip link set wlan0 up\n"
        "        wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf\n"
        "        sleep 5\n"
        "        dhclient -v wlan0\n"
        "    fi\n"
        "    sleep 10\n"
        "done\n"
    )
    run_cmd(f"echo '{loop_script}' | sudo tee /usr/local/bin/wifi-loop.sh")
    run_cmd("sudo chmod +x /usr/local/bin/wifi-loop.sh")

    # 4. Service to run this loop
    service = (
        "[Unit]\n"
        "Description=Looping Wi-Fi autoconnect to OPEN\n"
        "After=network.target\n"
        "\n"
        "[Service]\n"
        "Type=simple\n"
        "ExecStart=/usr/local/bin/wifi-loop.sh\n"
        "Restart=always\n"
        "RestartSec=5\n"
        "\n"
        "[Install]\n"
        "WantedBy=multi-user.target\n"
    )
    run_cmd(f"echo '{service}' | sudo tee /etc/systemd/system/pynq-wifi-autoconnect.service")
    run_cmd("sudo systemctl daemon-reload")
    run_cmd("sudo systemctl restart pynq-wifi-autoconnect.service")
    run_cmd("sudo systemctl enable pynq-wifi-autoconnect.service")
    
    ser.close()
    print("\n[OK] Board is primed and continuously attempting connection to OPEN.")

if __name__ == '__main__':
    main()

