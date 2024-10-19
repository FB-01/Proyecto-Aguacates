import numpy as np
import cv2

cap = cv2.VideoCapture(0)

lower=np.array([15,17,125])
high=np.array([70,59,231])


while True:
    ret,frame=cap.read()
    mask=cv2.inRange(frame,lower,high)
    imgn=cv2.bitwise_and(frame,frame,mask=mask)
    
    cv2.imshow('FRAMES',frame)
    cv2.imshow('Objeto Amarillo',imgn)

    k=cv2.waitKey(1) & 0xFF
    if(k==ord('q')):
        break

cv2.destroyAllWindows
cap.release()
