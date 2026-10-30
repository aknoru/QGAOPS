import serial
import time

ser = serial.Serial('COM3', 115200, timeout=1)
ser.write(b'\n')
time.sleep(0.3)
ser.read(ser.in_waiting)

ser.write(b'sed -n "620,645p" /home/xilinx/pynq_board_package/qgpu_board.py\n')
time.sleep(1)
out = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("Lines 620-645 on board:")
print(out)

ser.close()

