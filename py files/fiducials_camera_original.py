from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import sys
import os
import os.path
import time
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt

print "\n",sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]
print "Fiducials"

x=int(sys.argv[1])+ int(sys.argv[2])+ int(sys.argv[3])#68665 
y=int(sys.argv[4])+int(sys.argv[5])#2720
x1=0
x2=0
x3=0
y1=0
y2=0
x_t=0
y_t=0
z_t=0
x_camera = 0
y_camera = 0

import logging
logging.basicConfig()
log = logging.getLogger()
fil=logging.FileHandler('log.txt')
log.addHandler(fil)
log.setLevel(logging.ERROR)

i=1
process=True

# go through the data file
print "Start \n"
while process==True:
       
    # initiate client
    client=ModbusClient('10.0.2.250', port=502)
    client.connect()

        
    # change status to moving mode
    rq=client.write_registers(0,[3],unit=1)
    time.sleep(0.2)

    stat=False
    while stat==False:
        try:
            # read coil 0 to check if controller is requesting data for 1st time
            rr=client.read_coils(100,1,unit=1)
            time.sleep(0.2)
            a=rr.bits[0]
            stat=True
        except AttributeError as e:
            log.error('error 1')
            log.error(str(rr))
            log.error(str(e))
            time.sleep(0.2)

    # if controller is requesting data for 1st time   
    if rr.bits[0]==True:
        #print "Sending data"        
        
        x_t=x-11717
        y_t=y+95
        z=0
        print x_t,y_t,z, "POSITON SENT first"
        
        if x_t>32767:
            if x_t>65534:
                x1=32767
                x2=32767
                x3=x_t-x1-x2
            else:
                x1=32767
                x2=x_t-x1
                x3=0
        elif x_t<32767:
            x1=x_t
            x2=0
            x3=0
        if y_t>32767:
            y1=32767
            y2=y_t-32767
        elif y_t<32767:
            y1=y_t
            y2=0
        
        # put the position in a list
        re=[]
        re.append(x1)
        re.append(x2)
        re.append(x3)
        re.append(y1)
        re.append(y2)
        re.append(z)

        # client send position to server
        rq=client.write_registers(21,re,unit=8)
        time.sleep(0.2)

            
        rq=client.write_registers(15,[3],unit=1)
        time.sleep(0.2)
               
        # client changes status to controller not requesting data
        rq=client.write_coil(100,False,unit=1)
        time.sleep(0.2)
        rq=client.write_coil(101,False,unit=1)
        time.sleep(0.2)
        rq=client.write_coil(102,False,unit=1)
        time.sleep(0.2)

        client.close()
        time.sleep(0.2)
        img_counter = 0
        
        # Start default camera
        cap = cv2.VideoCapture(0)
        focus = 60 # min: 0, max: 255, increment:5
        cap.set(28, focus) 


        k=1
        while k==1:
            stat=False
            while stat==False:
                try:
                    # if controller has finished movement for 1st time
                    rr=client.read_coils(102,1,unit=1)
                    time.sleep(0.2)
                    a=rr.bits[0]
                    print 'waiting_camera'
                    stat=True
                except AttributeError as e:
                    log.error('error 2')
                    log.error(str(rr))
                    log.error(str(e))
                    time.sleep(0.2)
                
            if rr.bits[0]==True:
            #print "Spike Check tool"
                time.sleep(0.5)
         
                # Number of frames to capture
                num_frames = 1;

                print "Picture {0}".format(img_counter)
                 
                # Grab a few frames
                for l in xrange(0, num_frames) :
                    ret, frame = cap.read()
                    # mirror the frame
                    frame = cv2.flip(frame, 1)
                    width = frame.shape[1]
                    height = frame.shape[0]
                    x=(width/2)-40
                    y=(height/2)-40
                    a=30
                    b=30
                    image=cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 2)
                    roi = frame[y:y+b, x:x+a]
                    crop_img = frame[y:y+b, x:x+a]
                    img_name = "z {0}.png".format(img_counter)
                    cv2.imwrite(img_name, frame)
                    img_counter += 1
                k=2
                i=1
                rq=client.write_registers(16,[3],unit=1)
                time.sleep(0.2)
                rq=client.write_coil(102,False,unit=1)
                time.sleep(0.2)
                rq=client.write_coil(103,False,unit=1)
                time.sleep(0.2) 
            elif a==False:
                k=k
                
        while i==1:
            stat=False
            while stat==False:
                try:
                    # if controller has finished movement for 1st time                   
                    rr=client.read_coils(104,1,unit=1)
                    time.sleep(0.2)
                    a=rr.bits[0]
                    print 'waiting_template'
                    stat=True
                except AttributeError as e:
                    log.error('error 2')
                    log.error(str(rr))
                    log.error(str(e))
                    time.sleep(0.2)
                
            if rr.bits[0]==True:
                time.sleep(0.5)
                # Capture frame-by-frame
                ret, frame = cap.read()

                # mirror the frame
                frame = cv2.flip(frame, 1)
                width = frame.shape[1]
                height = frame.shape[0]
                x=(width/2)-40
                y=(height/2)-40
                a=40
                b=40
                image=cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 2)
                roi = frame[y:y+b, x:x+a]
                crop_img = frame[y:y+b, x:x+a]
                #imagee=cv2.rectangle(frame, ((x+a/2), (y+b/2)), ((x+a/2), (y+b/2)), (255, 255, 0), 2)
                img_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

                template = cv2.imread('fidtemplateoriginal.png',0) #...................................................................................
                w, h = template.shape[::-1]
                res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                threshold = 0.94
                loc = np.where( res >= threshold)
                for pt in zip(*loc[::-1]):
                    
                    #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
                    #print("Position:", pt[0])
                    #cv2.rectangle(crop_img, pt, (pt[0] + w, pt[1] + int(h/2)), (0,0,255), -1)
                    cv2.circle(crop_img,((pt[0]+w/2) ,(pt[1]+h/2)),1,(0,255,0), 1)
                    #crop_img = frame[200:350,950:1000]
                    #imagee=cv2.rectangle(frame, ((x+a/2), (y+b/2)), ((x+a/2), (y+b/2)), (255, 255, 0), 2)
                    x_camera=pt[0]+w/2
                    y_camera=pt[1]+h/2
                    print 'w',x_camera,'h',y_camera
                    break
                rq=client.write_coil(102,False,unit=1)
                                     
                cv2.imwrite('pinout1_1.png',frame)
                cap.release()

                rq=client.write_coil(102,False,unit=1)
                time.sleep(0.2)
                rq=client.write_coil(104,False,unit=1)
                time.sleep(0.2)
                rq=client.write_registers(16,[0],unit=1)
                time.sleep(0.2)
                x_cam=(20-x_camera)*5
                y_cam=(20-y_camera)*5
                
                file= open("fid_cam.txt","w")
                file.write("%d" %x_cam)
                file.write("\n")
                file.write("%d" %y_cam)
                file.close()

                rq=client.write_registers(15,[0],unit=1)
                time.sleep(0.2)
                rq=client.write_registers(0,[1],unit=1)
                time.sleep(0.2)
                rq=client.write_coil(100,False,unit=1)
                time.sleep(0.2)
                rq=client.write_coil(101,False,unit=1)
                time.sleep(0.2)
                rq=client.write_coil(102,False,unit=1)
                time.sleep(0.2)
                rq=client.write_coil(104,False,unit=1)
                time.sleep(0.2)
                


                
            elif a==False:
                i=i
  
        # client changes status to controller not requesting data
        rq=client.write_coil(100,False,unit=1)
        time.sleep(0.2)
        rq=client.write_coil(101,False,unit=1)
        time.sleep(0.2)
        rq=client.write_registers(15,[0],unit=1)
        time.sleep(0.2)

        process=False
        
    # if controller is  moving
    else:
        # close client
        client.close()
