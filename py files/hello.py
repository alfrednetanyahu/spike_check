import serial   #import serial library
import os
import time
import sys
import cv2
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# initiate client
client=ModbusClient('10.0.2.250', port=502)
client.connect()

# change status to moving mode
rq=client.write_registers(0,[2],unit=1)
time.sleep(0.2)

img_counter = 0

time.sleep(0.5)

if __name__ == '__main__' :

    time.sleep(0.2)
 
    # Start default camera
    video = cv2.VideoCapture(0);

    # Number of frames to capture
    num_frames = 1;

    print "Capturing {0} frames".format(num_frames)
     
    # Grab a few frames
    for i in xrange(0, num_frames) :
        ret, frame = video.read()
        # mirror the frame
        frame = cv2.flip(frame, 1)
        width = frame.shape[1]
        height = frame.shape[0]
        x=(width/2)-8
        y=(height/2)-8
        a=15
        b=15
        image=cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 2)
        roi = frame[y:y+b, x:x+a]
        crop_img = frame[y:y+b, x:x+a]
        img_name = "z {}.png".format(img_counter)
        cv2.imwrite(img_name, crop_img)
        img_counter += 1

    # Release video
    video.release()


    print "DONE\n"
    
#close client
client.close()
    print "Close \n"
