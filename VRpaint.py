from cv2 import cv2
import numpy as np

frameWidth = 540
frameHeight = 380

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 300)


myColors = [[90, 193, 70, 154, 255, 255], 
            [114, 130, 152, 172, 255, 255], 
            [0, 165, 124, 80, 255, 255]]

myColorValues = [[245, 121, 39],    #BGR
                 [214, 28, 228], 
                 [39, 39, 245]]

myPoints = []  #[x, y, colorId]


def findColor(img, myColors, myColorValues):
    count = 0
    newPoints = []
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
    return newPoints



def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgResult, cnt, -1, (0, 255, 0), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP) 

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow('Camera', imgResult)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break