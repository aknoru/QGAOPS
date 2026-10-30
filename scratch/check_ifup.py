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
    
    # Check if wpa_supplicant process is running
    run_cmd("ps aux | grep -i wpa")
    
    # Try ifdown then ifup with verbose output
    run_cmd("sudo ifdown --force wlan0", timeout=10)
    run_cmd("sudo ifup -v wlan0", timeout=25)
    
    # Check status
    time.sleep(3)
    run_cmd("ip addr show wlan0")
    run_cmd("sudo iw dev wlan0 link")
    ser.close()

if __name__ == '__main__':
    main()

