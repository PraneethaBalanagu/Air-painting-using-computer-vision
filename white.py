import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
brushThickness=10
eraseThickness=50
#imageCanvas=np.zeros((720,1280,3),np.uint8)
imageCanvas = np.full((720, 1280, 3), 255, np.uint8)

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
header = overlayList[0]
drawColor= (100, 50, 255)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector()
detector.hands.tracking_confidence = 0.85
xp,yp=0,0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHand(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()

        if fingers[1] and fingers[2]:
            if y1 < 130:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor= (100, 50, 255)
                elif 500 < x1 < 600:
                    header = overlayList[1]
                    drawColor=(150,100,0)
                elif 680 < x1 < 790:
                    header = overlayList[2]
                    drawColor=(140,180,0)
                elif 810 < x1 < 990:
                    header = overlayList[3]
                    drawColor=(0,255,255)
                elif 1010 < x1 < 1170:
                    header = overlayList[4]
                    drawColor=(255,255,255)
                elif 1180 < x1 < 1280:
                    header = overlayList[5]
                    drawColor=(0,0,0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawColor==(255,255,255):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraseThickness)
                cv2.line(imageCanvas, (xp, yp), (x1, y1), drawColor,eraseThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imageCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp,yp=x1,y1
    img[0:125, 0:1280] = header
    cv2.imshow("Image", img)
    cv2.imshow("Canvas",imageCanvas)
    cv2.waitKey(1)