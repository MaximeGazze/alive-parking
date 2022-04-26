import cv2
from threading import Thread
from lcd import LCD
from time import sleep
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
lcd = LCD()
servo = Servo(21, pin_factory=PiGPIOFactory())
gateOpen = False

def openGate():
    global gateOpen
    gateOpen = True
    servo.min()

def closeGate():
    global gateOpen
    gateOpen = False
    servo.max()

def verify(data):
    # check if employe exists
    print(data)
    Thread(target=allow_entry, args=()).start()

def allow_entry():
    global gateOpen
    # sleep(5)
    if not gateOpen:
        openGate()
        lcd.text('Chien chaud', 0)
        lcd.text('Ta Mere En Short', 1)
        sleep(5)
        closeGate()
        lcd.clear()

def drawBox(bbox):
    points = [(int(bbox[0][i][0]), int(bbox[0][i][1])) for i in range(len(bbox[0]))]
    for i in range(len(points)):
        cv2.line(img, points[i - 1], points[i], (0, 255, 0), 2)
    cv2.putText(img, data, (points[0][0], points[0][1] - 5), cv2.FONT_HERSHEY_SIMPLEX, (points[1][0] - points[0][0]) * 0.004, (0, 0, 255), 1, cv2.LINE_AA)

closeGate()

while True:
    try:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            drawBox(bbox)
            verify(data)

        # cv2.imshow('QRCODEscanner', img)
        if cv2.waitKey(1) == ord('q'):
            break
    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()

