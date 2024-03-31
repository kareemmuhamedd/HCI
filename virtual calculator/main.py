import cv2 # open cv
from cvzone.HandTrackingModule import HandDetector
import time


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
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '='],]
buttonList = []
for x in range(4): # x1 y2
    for y in range(4):
        xpos = x*100 + 650
        ypos = y*100 + 150
        buttonList.append(
            Button((xpos, ypos), 100, 100, buttonListValues[y][x]),)
print([buttonList])

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

    # Draw all buttons
    cv2.rectangle(img, (650, 50), (650 + 400, 70 + 100),
                  (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (650, 50), (650+400, 70+100),
                  (50, 50, 50), 3)

    for button in buttonList:
        button.draw(img)

    # Check for hand
    if hands:
        lmList = hands[0]['lmList'] # landmark
        length, _, img = detector.findDistance(
            lmList[8][0:2], lmList[12][0:2], img, color=(255, 0, 255), scale=10)
        x, y = lmList[8][0:2]
        if length < 50:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    myValue = buttonListValues[int(i % 4)][int(i/4)]
                    if myValue == "=":
                        myEquation = str(eval(myEquation))
                    else:
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








# int(i % 4) calculates the column index:

# When i is 0, 1, 2, or 3, int(i % 4) will be 0, indicating the first column.
# When i is 4, 5, 6, or 7, int(i % 4) will be 1, indicating the second column.
# When i is 8, 9, 10, or 11, int(i % 4) will be 2, indicating the third column.
# When i is 12, 13, 14, or 15, int(i % 4) will be 3, indicating the fourth column.
# int(i/4) calculates the row index:

# When i is 0, 4, 8, or 12, int(i/4) will be 0, indicating the first row.
# When i is 1, 5, 9, or 13, int(i/4) will be 1, indicating the second row.
# When i is 2, 6, 10, or 14, int(i/4) will be 2, indicating the third row.
# When i is 3, 7, 11, or 15, int(i/4) will be 3, indicating the fourth row.
