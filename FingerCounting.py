import cv2
import time
import os
import HandTrackingModule as htm
wCam,hCam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
folderPath="FingerImages"
myList=os.listdir(folderPath)
print(myList)
overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)
pTime=0
detector=htm.handDetector()
detector.hands.tracking_confidence=0.75
tipIds=[4,8,12,16,20]
while True:
    success,img=cap.read()
    img=detector.findHand(img)
    img = cv2.flip(img, 1)
    lmList=detector.findPosition(img,draw=False)
   # print(lmList)
    if len(lmList)!=0:
        fingers=[]
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(0)
        else:
            fingers.append(1)
        for id in range(1,5):

            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalFingers=fingers.count(1)
        print(totalFingers)
        h, w, c = overlayList[0].shape
        overlayImg = overlayList[totalFingers ]
        overlayImg = cv2.resize(overlayImg, (w, h))
        img[0:h, 0:w] = overlayImg
        cv2.rectangle(img,(20,225),(170,425),(255,0,255),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)