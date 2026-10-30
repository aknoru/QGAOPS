import cv2

try:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    print("Camera 0 available:", ret)
    cap.release()
except Exception as e:
    print("Camera test error:", e)

