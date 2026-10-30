import serial
import time
import sys

def main():
    ser = serial.Serial('COM3', 115200, timeout=1.0)
    time.sleep(0.5)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    def run_cmd(cmd, timeout=30):
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
    # Clean up any manual wpa_supplicant or dhclient
    run_cmd("sudo killall -9 wpa_supplicant dhclient 2>/dev/null || true")
    run_cmd("sudo rm -f /etc/network/interfaces.d/*")
    
    # Use PYNQ's Wifi.connect with auto=True and force=True
    run_cmd("sudo /usr/local/share/pynq-venv/bin/python3 -c \"from pynq.lib import Wifi; w = Wifi(); w.reset(); w.connect('OPEN', 'FUKCYOUBITCH', auto=True, force=True)\"", timeout=45)
    
    # Check /etc/network/interfaces.d/wlan0
    run_cmd("cat /etc/network/interfaces.d/wlan0")
    
    # Wait for association and dhcp
    time.sleep(5)
    run_cmd("ip addr show wlan0")
    run_cmd("sudo systemctl restart qgpu-gui")
    run_cmd("sudo systemctl status qgpu-gui --no-pager")
    ser.close()

if __name__ == '__main__':
    main()

