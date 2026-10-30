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
    # Check iw scan for OPEN
    run_cmd("sudo iw dev wlan0 scan | grep -E '(SSID|freq|signal|BSS )'")
    # Check pynq.lib.wifi implementation
    run_cmd("python3 -c 'import pynq.lib.wifi, inspect; print(inspect.getsource(pynq.lib.wifi.Wifi))'")
    ser.close()

if __name__ == '__main__':
    main()

