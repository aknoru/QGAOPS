import serial
import time
import sys

def main():
    print("Opening COM3...")
    ser = serial.Serial('COM3', 115200, timeout=1.0)
    time.sleep(0.5)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    ser.write(b"\r\n")
    time.sleep(0.5)
    data = ser.read(ser.in_waiting or 100)
    print("Initial response:", repr(data))
    
    # If not at prompt, send another newline or check for login
    if b"login:" in data:
        print("Logging in...")
        ser.write(b"xilinx\r\n")
        time.sleep(1.0)
        ser.write(b"xilinx\r\n")
        time.sleep(1.0)
    elif b"$" not in data and b"#" not in data:
        ser.write(b"\r\n")
        time.sleep(0.5)
        data += ser.read(ser.in_waiting or 100)
        print("After second enter:", repr(data))

    # Send a test command: echo "SERIAL_OK"
    ser.write(b"echo 'SERIAL_OK'\r\n")
    time.sleep(1.0)
    resp = ser.read(ser.in_waiting or 100).decode('utf-8', errors='ignore')
    print("Echo response:", resp)
    ser.close()

if __name__ == '__main__':
    main()

