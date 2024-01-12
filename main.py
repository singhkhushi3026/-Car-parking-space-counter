import cv2
import pickle
import numpy as np
 
cap = cv2.VideoCapture('carPark.mp4')
width, height = 103, 43
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

val1 = 25
val2 = 16
val3 = 5
 
def checkSpaces():
    spaces = 0 
    for pos in posList:
        x, y = pos
        w, h = width, height
 
        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)
 
        if count < 900:
            color = (0, 200, 0) # change the color to green
            thic = 5
            spaces += 1
 
        else:
            color = (0, 0, 200) # change the color to red
            thic = 2
 
        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)
 
        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                    color, 2)
    cv2.putText(img, f'Free: {spaces}/{len(posList)}', (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 200, 0), 2)
 
 
while True:
 
    # Get image frame
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT): # replaying the video
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)
 
    checkSpaces()
    # Display Output
 
    cv2.imshow("Image", img)
    #cv2.imshow("ImageGray", imgThres)
    #scv2.imshow("ImageBlur", imgBlur)
    key = cv2.waitKey(1)
    if key == ord('r'):
        pass