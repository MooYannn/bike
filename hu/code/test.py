import cv2

cap = cv2.VideoCapture(r"C:\Users\12081\Desktop\bike\hu\video\vio_1.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        print("video read error")
        break
    else:
        frame = cv2.resize(frame, (640, 480))
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break