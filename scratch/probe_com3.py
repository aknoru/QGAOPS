import serial
import time

try:
    ser = serial.Serial('COM3', 115200, timeout=1)
    ser.write(b'\n')
    time.sleep(0.3)
    out = ser.read(ser.in_waiting)
    print("COM3 Output:", out)
    ser.write(b'echo ALIVE\n')
    time.sleep(0.3)
    out2 = ser.read(ser.in_waiting)
    print("Echo Output:", out2)
    ser.close()
except Exception as e:
    print("COM3 Error:", e)

