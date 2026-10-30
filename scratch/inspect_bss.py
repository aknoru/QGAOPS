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
    # Scan specifically for the BSS of OPEN
    run_cmd("sudo iw dev wlan0 scan | grep -A 25 '72:46:bc:4f:aa:14'")
    # Let wpa_supplicant scan
    run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 scan")
    time.sleep(3)
    run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 scan_results")
    run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 reassociate")
    ser.close()

if __name__ == '__main__':
    main()

