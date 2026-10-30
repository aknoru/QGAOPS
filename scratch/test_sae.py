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
    
    # Configure network 0 with SAE
    run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 set_network 0 key_mgmt 'SAE WPA-PSK'")
    run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 set_network 0 psk '\"FUKCYOUBITCH\"'")
    run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 set_network 0 ieee80211w 1")
    run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 enable_network 0")
    run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 select_network 0")
    run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 reassociate")
    
    print("\nWaiting for association...")
    for i in range(10):
        time.sleep(2)
        res = run_cmd("sudo wpa_cli -p /run/wpa_supplicant -i wlan0 status")
        if "wpa_state=COMPLETED" in res:
            print("\n*** SUCCESS! WPA_STATE is COMPLETED! ***")
            break
        
    ser.close()

if __name__ == '__main__':
    main()

