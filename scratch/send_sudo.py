import serial
import time

ser = serial.Serial('COM3', 115200, timeout=1)
ser.write(b'xilinx\n')
time.sleep(1)
out = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("Password response:", out)

ser.write(b'netstat -tulpn | grep 8080\n')
time.sleep(1)
out2 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("Netstat 8080:", out2)

ser.write(b'curl -s http://127.0.0.1:8080/api/status\n')
time.sleep(1)
out3 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("Curl 127.0.0.1:8080:", out3)

ser.close()

