import serial
import time

ser = serial.Serial('COM3', 115200, timeout=1)
ser.write(b'\n')
time.sleep(0.3)
ser.read(ser.in_waiting)

ser.write(b'sudo ss -tulpn | grep 8080\n')
time.sleep(1)
out = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("ss 8080:")
print(out)

ser.write(b'curl -s http://localhost:8080/api/status\n')
time.sleep(1)
out2 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("curl local status:")
print(out2)

ser.close()

