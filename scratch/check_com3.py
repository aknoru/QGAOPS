import serial

try:
    ser = serial.Serial('COM3', 115200, timeout=1)
    ser.write(b'\n')
    line = ser.read(200)
    print("COM3 Output:", line)
    ser.close()
except Exception as e:
    print("Error:", e)

