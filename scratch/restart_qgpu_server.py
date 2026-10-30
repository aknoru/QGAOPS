import serial
import time

ser = serial.Serial('COM3', 115200, timeout=1)
ser.write(b'\n')
time.sleep(0.3)
ser.read(ser.in_waiting)

ser.write(b'sudo killall python3\n')
time.sleep(1)
ser.write(b'xilinx\n')
time.sleep(1)
out = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("Killall out:", out)

ser.write(b'cd /home/xilinx/pynq_board_package && sudo /usr/local/share/pynq-venv/bin/python3 qgpu_board.py --port 8080 > server.log 2>&1 &\n')
time.sleep(2)
out2 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("Start out:", out2)

ser.write(b'cat server.log\n')
time.sleep(1)
out3 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("server.log:", out3)

ser.close()

