import cv2, re, asyncio
from threading import Thread
from lcd import LCD
from time import sleep
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from interactWithAlive import interactiveAlive
from aliot.aliot import alive_iot as iot

iot.ObjConnecteAlive.set_url("wss://albumfamilial.ca/iotgateway/")
iot.ObjConnecteAlive.set_api_url("https://albumfamilial.ca/api")

stationnement = iot.ObjConnecteAlive(object_id = "3e273ab3-38d8-4d0a-984e-589fd39e3a84") 

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()
lcd = LCD()
servo = Servo(21, pin_factory=PiGPIOFactory())
gateOpen = False
command = interactiveAlive(stationnement)

def openGate():
    global gateOpen
    gateOpen = True
    servo.min()

def closeGate():
    global gateOpen
    gateOpen = False
    servo.max()

def verify(data):
    global gateOpen
    match = re.search(reg, data.upper())
    if not match:
        match = re.search(regRusse, data.upper())
    matricule = None
    if match:
        matricule = match.group()
    info = command.stationnement(matricule)
    if not gateOpen:
        print('coco')
        t = Thread(target=allow_entry, args=(data,info))
        t.start()
        t.join()

def allow_entry(data, info):
    global gateOpen
    #sleep(5)
    print('gateOPEN', gateOpen)
    if not gateOpen:
        openGate()
        lcd.text('Matricule:', 0)
        lcd.text(data, 1)
        sleep(2)
        lcd.text("{}".format(info['prenom']), 0)
        lcd.text("{}".format(info['nom']), 1)
        sleep(5)
        closeGate()
        lcd.clear()

def drawBox(bbox):
    points = [(int(bbox[0][i][0]), int(bbox[0][i][1])) for i in range(len(bbox[0]))]
    for i in range(len(points)):
        cv2.line(img, points[i - 1], points[i], (0, 255, 0), 2)
    cv2.putText(img, data, (points[0][0], points[0][1] - 5), cv2.FONT_HERSHEY_SIMPLEX, (points[1][0] - points[0][0]) * 0.004, (0, 0, 255), 1, cv2.LINE_AA)

closeGate()

regRusse = '[A-Z][0-9]{3}[A-Z]{2}'
reg = '[A-Z0-9]{3}\s[A-Z0-9]{3}'


@stationnement.main_loop(1)
def main():
    while True:
        try:
            _, img = cap.read()
            data, bbox, _ = detector.detectAndDecode(img)
            if data:
                #drawBox(bbox)
                verify(data)

            #cv2.imshow('QRCODEscanner', img)

            if cv2.waitKey(1) == ord('q'):
                break
        except KeyboardInterrupt:
            lcd.clear()
            break
        except Exception as e:
            pass

stationnement.begin()
cap.release()
cv2.destroyAllWindows()
