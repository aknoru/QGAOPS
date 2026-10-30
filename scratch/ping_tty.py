import serial
import time

ser = serial.Serial('COM3', 115200, timeout=1)
ser.write(b'\n')
time.sleep(0.5)
out = ser.read(ser.in_waiting)
print("Initial:", out)

ser.write(b'echo test\n')
time.sleep(0.5)
out2 = ser.read(ser.in_waiting)
print("Echo:", out2)

ser.close()

