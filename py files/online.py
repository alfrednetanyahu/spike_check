import os
import cv2
import numpy as np
import time
import math
from matplotlib import pyplot as plt


cap = cv2.VideoCapture(0)
focus = 60 # min: 0, max: 255, increment:5
cap.set(28, focus)

#cv2.namedWindow("Fiducial Offset Calibration")

template = cv2.imread('fidtemplateoriginal.png',cv2.IMREAD_GRAYSCALE)
w , h = template.shape[::-1] 

while True :
    
                
    ret, frame = cap.read()
    width = frame.shape[1]
    height = frame.shape[0]
    
    #set region of interest
    
    #dimensions
    frame_x = width/2
    frame_y = height/2
    x=(width/2)-20
    y=(height/2)-20
    a=40
    b=40

    #Draw rectangle on the region of detection.
    
    cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 1)
    cv2.circle(frame,((x+a/2) ,(y+b/2)),1,(0,255,0), 1)

    #print frame_x, frame_y
    
    #roi = frame[y:y+b, x:x+a]
    #crop_img = frame[100:140, 140:180]
    #img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #.......
    
    
    #template matching 
    #res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    
    #threshold = 0.8
    
    x_cam=0
    y_cam=0

    #loc = np.where( res >= threshold)
    
    #for pt in zip(*loc[::-1]):

        #puting  dot (.) on centrepoint of the recognized area 
        
        #cv2.rectangle(frame,pt,((pt[0] + w), (pt[1] + h)),(0,255,0), 1)
        #cv2.circle(frame,((pt[0]+w/2) ,(pt[1]+h/2)),1,(0,255,0), 1)
        #x_camera=pt[0]+w/2
        #y_camera=pt[1]+h/2

    #x_cam = frame_x - x_camera
    #y_cam = frame_y - y_camera

        #print x_cam , y_cam
        
    cv2.imshow("Fiducial Offset Calibration",frame)

    #if (x_cam == 0) and (y_cam == 0):
            
        #font = cv2.FONT_HERSHEY_SIMPLEX #Creates a font
        #x = 20 #position of text
        #y = 20 #position of text
        #cv2.putText(frame,'Centre point found', (x,y),font, 255, (0,255,0),2,cv2.LINE_AA) #Draw the text

        #time.sleep(1)
        #cap.release()
    
        
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "fidtemplate.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} saved!".format(img_name))
        img_counter += 1
        

cap.release()

cv2.destroyAllWindows()

