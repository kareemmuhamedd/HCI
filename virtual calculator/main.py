import cv2  # open cv
from cvzone.HandTrackingModule import HandDetector
import math


class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width,
                      self.pos[1]+self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width,
                      self.pos[1]+self.height), (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0]+40, self.pos[1]+60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0]+self.width and \
                self.pos[1] < y < self.pos[1]+self.height:
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width,
                                          self.pos[1]+self.height), (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0]+self.width,
                                          self.pos[1]+self.height), (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0]+25, self.pos[1]+80),
                        cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
            return True
        else:
            return False


# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Creating Buttons
buttonListValues = [['7', '8', '9', '*'], ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'], ['0', '/', 'C', '='], ['sqr', '^', '<-', ''],]
buttonList = []
for y in range(5):
    for x in range(4):
        xpos = x*100 + 650
        ypos = y*100 + 150
        buttonList.append(
            Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

# Variables
myEquation = ''
delayCounter = 0


# Loop
while True:
    # Get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detection of hand
    hands, img = detector.findHands(img, flipType=False)

    # Draw all buttons body of calc
    cv2.rectangle(img, (650, 50), (650 + 400, 70 + 100),
                  (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (650, 50), (650+400, 70+100),
                  (50, 50, 50), 3)

    for button in buttonList:
        button.draw(img)

    # Check for hand
    if hands:
        lmList = hands[0]['lmList']  # landmark
        length, _, img = detector.findDistance(
            lmList[8][0:2], lmList[12][0:2], img, color=(255, 0, 255), scale=10)
        x, y = lmList[8][0:2]
        if length < 50:
            for button in buttonList:
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = button.value
                    if myValue == "=" and myEquation:
                        if 'sqr' in myEquation:
                            sqr_index = myEquation.find('sqr')
                            num = myEquation[sqr_index + 3:]
                            result = math.sqrt(float(num))
                            myEquation = myEquation.replace(
                                'sqr' + num, str(result))
                        myEquation = str(eval(myEquation))
                    elif myValue == 'C':
                        myEquation = ''
                    elif myValue == '^':
                        myEquation += '*'
                    elif myValue == '<-':
                        if myEquation[-3:] == 'sqr':
                            myEquation = myEquation[:-3]
                        else:
                            myEquation = myEquation[:-1]
                    else:
                        if myValue != '=':
                            myEquation += myValue
                    delayCounter = 1

    # Avoid Duplicates
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Display the Equation/Result
    cv2.putText(img, myEquation, (670, 120),
                cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    # Display image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''
