import serial
import time

ser = serial.Serial('COM3', 115200, timeout=1)
ser.write(b'\n')
time.sleep(0.3)
ser.read(ser.in_waiting)

ser.write(b'sudo fuser -k 8080/tcp; sleep 1\n')
time.sleep(2)

# Start with nohup
ser.write(b'cd /home/xilinx/pynq_board_package && sudo nohup /usr/local/share/pynq-venv/bin/python3 qgpu_board.py --mode gui > server.log 2>&1 &\n')
time.sleep(3)

ser.write(b'cat /home/xilinx/pynq_board_package/server.log\n')
time.sleep(1)
out = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("Server Log:")
print(out)

ser.write(b'sudo ss -tulpn | grep 8080\n')
time.sleep(1)
out2 = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
print("SS 8080:")
print(out2)

ser.close()

