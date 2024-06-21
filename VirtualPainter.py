import cv2
import numpy as np
import os
import datetime
import HandTrackingModule as htm
from tkinter import colorchooser
point1 = None
point2 = None
brushThickness = 35
eraseThickness = 100
imageCanvas = np.zeros((720, 1280, 3), np.uint8)
imageCanvas1 = np.full((720, 1280, 3), 255, np.uint8)
folderPath = "Header"
folderPath1 = "Hover"
shape = 'freestyle'
myList = os.listdir(folderPath)
myList1 = os.listdir(folderPath1)
overlayList = [] 
overlayList1 = []
undo_stack = []
redo_stack = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
for imPath in myList1:
    image = cv2.imread(f'{folderPath1}/{imPath}')
    overlayList1.append(image)
header = overlayList[0]
header1 = overlayList1[0]
drawColor = (100, 50, 255)
def select_color_from_palette():
    color = colorchooser.askcolor(title="Select Color")
    if color[1] is not None:
        global drawColor
        drawColor = tuple(map(int, color[0][:3]))
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector()
detector.hands.tracking_confidence = 0.85
xp, yp = 0, 0
hover = False

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
            xp, yp = 0, 0
            hover = False

            if y1 < 130:
                if 0 < x1 < 249:
                    if 0 < x1 < 62 and 0 < y1 < 250:
                        header1 = overlayList1[0]
                        shape = 'circle'
                        hover = True
                    elif 63 < x1 < 125 and 0 < y1 < 250:
                        header1 = overlayList1[1]
                        hover = True
                    elif 126 < x1 < 188 and 0 < y1 < 250:
                        header1 = overlayList1[2]
                        shape = 'ellipse'
                        hover = True
                    elif 189 < x1 < 249 and 0 < y1 < 250:
                        header1 = overlayList1[3]
                        shape = 'rectangle'
                        hover = True
                elif 250 < x1 < 450:
                    header = overlayList[0]
                    shape = 'freestyle'
                    drawColor = (100, 50, 255)
                elif 500 < x1 < 600:
                    header = overlayList[1]
                    shape = 'freestyle'
                    drawColor = (150, 100, 0)
                elif 680 < x1 < 790:
                    header = overlayList[2]
                    shape = 'freestyle'
                    drawColor = (140, 180, 0)
                elif 810 < x1 < 990:
                    header = overlayList[3]
                    shape = 'freestyle'
                    drawColor = (0, 255, 255)
                elif 1010 < x1 < 1170:
                    header = overlayList[4]
                    shape = 'freestyle'
                    drawColor = (0, 0, 0)
                elif 1180 < x1 < 1280:
                    header = overlayList[5]
                    shape = 'freestyle'
                    imageCanvas = np.zeros((720, 1280, 3), np.uint8)
                    imageCanvas1 = np.full((720, 1280, 3), 255, np.uint8)

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                z1, z2 = lmList[4][1:]
                result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))

                if result < 0:
                    result = -1 * result

                u = result

                if fingers[1] and fingers[4]:
                    eraseThickness = u

                cv2.circle(img, (x1, y1), eraseThickness, drawColor, cv2.FILLED)
                cv2.circle(imageCanvas, (x1, y1), eraseThickness, drawColor, cv2.FILLED)
                cv2.circle(imageCanvas1, (x1, y1), eraseThickness, drawColor, cv2.FILLED)

            else:
                if shape == 'freestyle':
                    undo_stack.append(imageCanvas.copy())
                    #undo_stack.append(imageCanvas1.copy())
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imageCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imageCanvas1, (xp, yp), (x1, y1), drawColor, brushThickness)

                if shape == 'circle':
                    z1, z2 = lmList[4][1:]
                    result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))

                    if result < 0:
                        result = -1 * result

                    u = result

                    cv2.circle(img, (z1, z2), u, drawColor, 3)
                    if fingers[4]:
                        undo_stack.append(imageCanvas.copy())
                        #undo_stack.append(imageCanvas1.copy())
                        cv2.circle(imageCanvas, (xp, yp), u, drawColor, 1)
                        cv2.circle(imageCanvas1, (xp, yp), u, drawColor, 1)

                if shape == 'rectangle':
                    z1, z2 = lmList[4][1:]
                    result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))

                    if result < 0:
                        result = -1 * result

                    u = result

                    cv2.rectangle(img, (z1, z2), (x1, y1), drawColor, 1)
                    if fingers[4]:
                        undo_stack.append(imageCanvas.copy())
                        #undo_stack.append(imageCanvas1.copy())
                        cv2.rectangle(imageCanvas, (z1, z2), (x1, y1), drawColor, 1)
                        cv2.rectangle(imageCanvas1, (z1, z2), (x1, y1), drawColor, 1)

                if shape == 'ellipse':
                    z1, z2 = lmList[4][1:]
                    a = z1 - x1
                    b = z2 - x2

                    if x1 > 250:
                        b = int(b / 2)

                    if a < 0:
                        a = -1 * a

                    if b < 0:
                        b = -1 * b

                    cv2.ellipse(img, (x1, y1), (a, b), 0, 0, 360, drawColor, 1)

                    if fingers[4]:
                        undo_stack.append(imageCanvas.copy())
                        #undo_stack.append(imageCanvas1.copy())
                        cv2.ellipse(imageCanvas, (x1, y1), (a, b), 0, 0, 360, drawColor, 1)
                        cv2.ellipse(imageCanvas1, (x1, y1), (a, b), 0, 0, 360, drawColor, 1)

                if shape == 'triangle':
                    if point1 is None:
                        point1 = (x1, y1)
                    elif point2 is None:
                        point2 = (x1, y1)
                    else:
                        point3 = (x1, y1)
                        cv2.line(img, point1, point2, (0, 255, 0), brushThickness)
                        cv2.line(img, point2, point3, (0, 255, 0), brushThickness)
                        cv2.line(img, point3, point1, (0, 255, 0), brushThickness)
                        point1 = None
                        point2 = None

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imageCanvas, cv2.COLOR_BGRA2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imageCanvas)
    img[0:125, 0:1280] = header

    if hover:
        img[0:250, 0:1280] = header1

    cv2.imshow("Image", img)
    cv2.imshow("ImageCanvas", imageCanvas)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename1 = f"black_{current_time}.png"
        filename2 = f"white_{current_time}.png"
        filepath1 = r"C:\Users\Dell\Documents\hack\acumen\Saved files\\" + filename1
        filepath2 = r"C:\Users\Dell\Documents\hack\acumen\Saved files\\" + filename2
        cv2.imwrite(filepath1, imageCanvas)
        cv2.imwrite(filepath2, imageCanvas1)
        print(f"Canvas images saved as '{filename1}' and '{filename2}'")

    elif key == ord('c'):
        select_color_from_palette()

    if key == ord('u'):
        if len(undo_stack) > 0:
            redo_stack.append(imageCanvas.copy())
            #redo_stack.append(imageCanvas1.copy())
            imageCanvas = undo_stack.pop()
            #imageCanvas1 = undo_stack.pop()

    elif key == ord('r'):
        if len(redo_stack) > 0:
            undo_stack.append(imageCanvas.copy())
            #undo_stack.append(imageCanvas1.copy())
            imageCanvas = redo_stack.pop()
            #imageCanvas1 = redo_stack.pop()

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()
