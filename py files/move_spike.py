from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import sys
import os
import time
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt

s=open('scope_info.txt',"r")
sc=s.readlines()
scope=sc[0].split()
print scope[0],scope[1],scope[2],scope[3],scope[4],scope[5]

re_dir=scope[0]
scope_mod=scope[1]
scope_cnt=scope[2]
scope_ip=scope[3]
scope_port=scope[4]
scope_channel=scope[5]

x=0
y=0
x1=0
x2=0
x3=0
y1=0
y2=0
x_t=0
y_t=0
z_t=0
r=0
x_camera=0
y_camera=0
x_cam=0
y_cam=0

# SOCKET BOARD limits

x_upperlimit = 135
x_lowerlimit = -135
y_upperlimit = 80
y_lowerlimit = -80

# The X_ref and Y_ref pin coordinates. Save the last tested pin

x_ref = 0
y_ref = 0

x_site = 0
y_site = 0



#Input from the fiducial calibration.(System Arguments)

x_offset = -11715#int(sys.argv[1])
y_offset = 95#int(sys.argv[2])


process=True

a=open('offset.txt',"r")
offs=a.readlines()
offset=offs[0].split()
x_t0=float(offset[0])
y_t0=float(offset[1])
z_t0=float(offset[2])
x_t1=float(offset[3])
y_t1=float(offset[4])
z_t1=float(offset[5])
x_t2=float(offset[6])
y_t2=float(offset[7])
z_t2=float(offset[8])
x_f0=100*float(offset[9])
y_f0=100*float(offset[10])
x_f1=100*float(offset[11])
y_f1=100*float(offset[12])
x_f2=100*float(offset[13])
y_f2=100*float(offset[14])
a.close()

f=open('position.txt',"r")
line_pos=f.readlines()
position_lines=len(line_pos)
print position_lines
f.close()

g=open('pin_info.txt',"r")
line_pin=g.readlines()
pin_lines=len(line_pin)
print len(line_pin)
g.close()

def point_tilt (x_pin,y_pin):
    # distance between f0 and pin
    x_f0p=float(x_f0-x_pin)
    y_f0p=float(y_f0-y_pin)
    hyp_f0p=float(math.sqrt((x_f0p*x_f0p)+(y_f0p*y_f0p)))
    #print "F0p", x_f0p, y_f0p, hyp_f0p

    # distance between f1 and pin
    x_f1p=float(x_f1-x_pin)
    y_f1p=float(y_f1-y_pin)
    hyp_f1p=float(math.sqrt((x_f1p*x_f1p)+(y_f1p*y_f1p)))
    #print "F1p", x_f1p, y_f1p, hyp_f1p

    # distance between f2 and pin
    x_f2p=float(x_f2-x_pin)
    y_f2p=float(y_f2-y_pin)
    hyp_f2p=float(math.sqrt((x_f2p*x_f2p)+(y_f2p*y_f2p)))
    #print "F2p", x_f2p, y_f2p, hyp_f2p

    # Sphere center of f0 with radius of hyp_f0p
    # Sphere center of f1 with radius of hyp_f1p
    # Sphere center of f2 with radius of hyp_f2p

    # Intersection between sphere_0p and sphere_1p creating circle01
    # Distance between spheres center
    d_1=x_t1-x_t0;
    d_2=y_t1-y_t0;
    d_3=z_t1-z_t0;
    d=math.sqrt(d_1*d_1 + d_2*d_2 + d_3*d_3);
    # Angle between sphere_0 center and intersection point
    top=float(hyp_f0p*hyp_f0p + d*d - hyp_f1p*hyp_f1p)
    bot=float(2*hyp_f0p*d)
    t=top/bot
    alpha=math.acos(t)
    # Intersection circle radius r_c_01
    r_c01=float(hyp_f0p*math.sin(alpha))
    # Plane intersection of S0p and S1p
    A1=float(2*d_1)
    B1=float(2*d_2)
    C1=float(2*d_3)
    D1=float(x_t0*x_t0 - x_t1*x_t1 + y_t0*y_t0 - y_t1*y_t1
             + z_t0*z_t0 - z_t1*z_t1 - hyp_f0p*hyp_f0p + hyp_f1p*hyp_f1p)
    top=float(x_t0*A1 + y_t0*B1 +z_t0*C1 + D1)
    bot=float(A1*(x_t0-x_t1) + B1*(y_t0-y_t1) + C1*(z_t0-z_t1))
    t=float(top/bot)
    x_c01=float(x_t0 + t*(x_t1 - x_t0))
    y_c01=float(y_t0 + t*(y_t1 - y_t0))
    z_c01=float(z_t0 + t*(z_t1 - z_t0))

    # Intersection between sphere_1p and sphere_2p creating circle12
    # Distance between spheres center
    d_1=x_t2-x_t1;
    d_2=y_t2-y_t1;
    d_3=z_t2-z_t1;
    d=math.sqrt(d_1*d_1 + d_2*d_2 + d_3*d_3);
    # Angle between sphere_1 center and intersection point
    top=float(hyp_f1p*hyp_f1p + d*d - hyp_f2p*hyp_f2p)
    bot=float(2*hyp_f1p*d)
    t=top/bot
    alpha=math.acos(t)
    # Intersection circle radius r_c_12
    r_c12=float(hyp_f1p*math.sin(alpha))
    # Plane intersection of S0p and S1p
    A2=float(2*d_1)
    B2=float(2*d_2)
    C2=float(2*d_3)
    D2=float(x_t1*x_t1 - x_t2*x_t2 + y_t1*y_t1 - y_t2*y_t2
             + z_t1*z_t1 - z_t2*z_t2 - hyp_f1p*hyp_f1p + hyp_f2p*hyp_f2p)
    top=float(x_t1*A2 + y_t1*B2 +z_t1*C2 + D2)
    bot=float(A2*(x_t1-x_t2) + B2*(y_t1-y_t2) + C2*(z_t1-z_t2))
    t=float(top/bot)
    x_c12=float(x_t1 + t*(x_t2 - x_t1))
    y_c12=float(y_t1 + t*(y_t2 - y_t1))
    z_c12=float(z_t1 + t*(z_t2 - z_t1))

    # Direction of line intersection between planes of circles
    # Set z=t
    x1=float((B2*D1-B1*D2)/(A2*B1-A1*B2))
    x2=float((B2*C1-B1*C2)/(A2*B1-A1*B2))
    y1=float((-D1/B1)-((A1/B1)*x1))
    y2=float(((A1/B1)*x2)+(C1/B1))
    z1=0
    z2=1

    # Intersection between line and sphere of circle01
    cgx=float(x_c01-x1)
    cgy=float(y_c01-y1)
    cgz=float(z_c01-z1)
    cg_sq=cgx*cgx + cgy*cgy + cgz*cgz

    gh_sq=math.fabs((r_c01*r_c01) - cg_sq)
    top=gh_sq
    a=x2*x2
    b=y2*y2
    c=z2*z2
    bot = a+b+c
    t_sq=float(top/bot)
    t=math.sqrt(t_sq)
    x_tilt=x1 + t*x2
    y_tilt=y1 - t*y2
    
    # Z correction based on the plane equation of the PCB board.
    # In this example, my desired pin location would be at x_tilt , y_tilt

    # Fiducials that were taken are converted into arrays

    FD2 = np.array([x_t0,y_t0,z_t0])
    FD4 = np.array([x_t1,y_t1,z_t1])
    FD6 = np.array([x_t2,y_t2,z_t2])

    # Vectors P and Q lie on the plane and are FD2FD4 and FD2FD6 respectively

    P = FD4 - FD2
    Q = FD6 - FD2

    #print P
    #print Q

    # Finding the cross product of the vectors P and Q gives us our coefficients

    crossprod = np.cross(P,Q)

    #print crossprod

    coeff_x = crossprod[0]
    coeff_y = crossprod[1]
    coeff_z = crossprod[2]

    #print coeff_x, coeff_y, coeff_z

    # Determining the equation ax + by + cz + d = 0
    #Using our reference vector FD2

    d = (coeff_x * FD2[0]) + (coeff_y * FD2[1]) + (coeff_z * FD2[2])

    #print d

    # the x and y coordinates would always be specified, so we have to make z our subject

    z = (((coeff_x * x_tilt) + (coeff_y * y_tilt) - d ) * -1 )/coeff_z

    #print z

    z_tilt= z

    return x_tilt, y_tilt, z_tilt



import logging
logging.basicConfig()
log = logging.getLogger()
fil=logging.FileHandler('log.txt')
log.addHandler(fil)
log.setLevel(logging.ERROR)

#start Modbus connection
client=ModbusClient('10.0.2.250', port=502)
client.connect()

# change status to moving mode
rq=client.write_registers(0,[2],unit=1)
time.sleep(0.2)

rq=client.write_registers(1,[position_lines],unit=1)
time.sleep(0.2)
client.close()
time.sleep(0.2)

# Start default camera
cap = cv2.VideoCapture(0)
focus = 60 # min: 0, max: 255, increment:5
cap.set(28, focus) 

i=1

# go through the data file
print "Start \n"
while process==True:
        
    # initiate client
    client=ModbusClient('10.0.2.250', port=502)
    client.connect()

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
        
        # go to 1st line and seperate numbers
        with open('position.txt') as a:
            pos=a.readlines()[0]
            position=pos.split()
            print position[0],position[1],position[2]
            x_or=100*float(position[1])
            y_or=100*float(position[2])
            a.close()

        x,y,z=point_tilt(x_or,y_or)
        
        #add offset between camera and probe tip
        x_t=x + x_offset
        y_t=y + y_offset
        z=0

        x_site = (x_or /100)
        y_site = (y_or /100)
        
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
        re=[position_lines]
        re.append(x1)
        re.append(x2)
        re.append(x3)
        re.append(y1)
        re.append(y2)
        re.append(z)

        #When both points are out of range
        
        if (x_ref > x_upperlimit or x_ref < x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
            rq = client.write_registers(40,[1],unit=1)
            time.sleep(0.2)
            print " VR 40 DETERMINED"
            

        #When both x_ref and x-or are in but y_coordinates are out.    
        elif (x_ref < x_upperlimit and x_ref > x_lowerlimit) and (x_site < x_upperlimit or x_site > x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
            if (x_ref <= 0):
                rq = client.write_registers(41,[1],unit=1)
                time.sleep(0.2)
                print " VR 41 DETERMINED"
            else:
                rq = client.write_registers(50,[1],unit=1)
                time.sleep(0.2)
                print " VR 41.(2) DETERMINED"
            
        #When x_ref is IN , all others are out
        elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
            rq = client.write_registers(42,[1],unit=1)
            time.sleep(0.2)
            print " VR 42 DETERMINED"
            
        #When x_ref is in and y_ref and y_or are equal and outside
        elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
            if (y_ref == y_pin):
                rq = client.write_registers(43,[1],unit=1)
                time.sleep(0.2)
                print " VR 43 DETERMINED"
                
        #When x_ref and x_or are outside but y_ref and y_pin are inside
        elif (x_ref > x_upperlimit or x_ref < x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site < y_upperlimit or y_site > y_lowerlimit):
            rq = client.write_registers(44,[1],unit=1)
            time.sleep(0.2)
            print " VR 44 DETERMINED"
            
        #When x_ref is inside and y_pin is inside
        elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site < y_upperlimit or y_site > y_lowerlimit):
            rq = client.write_registers(45,[1],unit=1)
            time.sleep(0.2)
            print " VR 45 DETERMINED"
            
        #When x_ref is outside and y_ref is inside, y_pin is outside and x_pin is inside
        elif (x_ref > x_upperlimit or x_ref < x_lowerlimit) and (x_site < x_upperlimit or x_site > x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
            rq = client.write_registers(46,[1],unit=1)
            time.sleep(0.2)
            print " VR 46 DETERMINED"

        elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
            rq = client.write_registers(47,[1],unit=1)
            time.sleep(0.2)
            print " VR 47 DETERMINED"

        elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site < x_upperlimit or x_site > x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
            rq = client.write_registers(48,[1],unit=1)
            time.sleep(0.2)
            print " VR 48 DETERMINED"

        elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site < y_upperlimit or y_site > y_lowerlimit):
            rq = client.write_registers(49,[1],unit=1)
            time.sleep(0.2)
            print " VR 49 DETERMINED"

        else:
            print " NOTHING DETERMINED"


        # client send position to server
        rq=client.write_registers(10,re,unit=8)
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
        
        #save image
        img_counter = 0                
        k=1
        while k==1:
            stat=False
            while stat==False:
                try:
                    # if controller has finished movement for 1st time
                    rr=client.read_coils(102,1,unit=1)
                    time.sleep(0.2)
                    a=rr.bits[0]
                    stat=True
                except AttributeError as e:
                    log.error('error 2')
                    log.error(str(rr))
                    log.error(str(e))
                    time.sleep(0.2)
                
            if rr.bits[0]==True:
                time.sleep(0.5)

                # Number of frames to capture
                num_frames = 1;

                print "Picture {0}".format(img_counter)
                 
                # Save the frame
                for l in xrange(0, num_frames) :
                    ret, frame = cap.read()
                    # mirror the frame
                    frame = cv2.flip(frame, 1)
                    width = frame.shape[1]
                    height = frame.shape[0]
                    x=(width/2)-14
                    y=(height/2)-14
                    a=28
                    b=28
                    image=cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 2)
                    roi = frame[y:y+b, x:x+a]
                    crop_img = frame[y:y+b, x:x+a]
                    img_name = "pin.png".format(img_counter)
                    cv2.imwrite(img_name, frame)
                    img_counter += 1      
                k=2
                cam=1
                
                #close loop
                rq=client.write_registers(2,[1],unit=1)
                time.sleep(0.2)
                rq=client.write_coil(102,False,unit=1)
                time.sleep(0.2)     
        
            elif a==False:
                k=k

        while cam==1:
            stat=False
            rq=client.write_registers(2,[1],unit=1)
            time.sleep(0.2)
            while stat==False:
                try:
                    # if controller has finished movement                   
                    rr=client.read_coils(104,1,unit=1)
                    time.sleep(0.2)
                    a=rr.bits[0]
                    stat=True
                except AttributeError as e:
                    log.error('error 2')
                    log.error(str(rr))
                    log.error(str(e))
                    time.sleep(0.2)
                
            if rr.bits[0]==True:
                
               # Capture frame-by-frame
                ret, frame = cap.read()
                print 'template1'

                # mirror the frame
                frame = cv2.flip(frame, 1)
                width = frame.shape[1]
                height = frame.shape[0]
                x=(width/2)-14
                y=(height/2)-14
                a=28
                b=28
                image=cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 2)
                roi = frame[y:y+b, x:x+a]
                crop_img = frame[y:y+b, x:x+a]
                #imagee=cv2.rectangle(frame, ((x+a/2), (y+b/2)), ((x+a/2), (y+b/2)), (255, 255, 0), 2)
                img_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

                #template matching
                template = cv2.imread('pintemplateneww.png',0)
                w, h = template.shape[::-1]
                res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                threshold = 0.7
                x_cam=0
                y_cam=0
                loc = np.where( res >= threshold)
                for pt in zip(*loc[::-1]):
                    print 'template2'
                    #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
                    #print("Position:", pt[0])
                    #cv2.rectangle(crop_img, pt, (pt[0] + w, pt[1] + int(h/2)), (0,0,255), -1)
                    #crop_img = frame[200:350,950:1000]
                    #imagee=cv2.rectangle(frame, ((x+a/2), (y+b/2)), ((x+a/2), (y+b/2)), (255, 255, 0), 2)
                    cv2.circle(crop_img,((pt[0]+w/2) ,(pt[1]+h/2)),1,(0,255,0), 1)
                    
                    #centre of pin
                    x_camera=pt[0]+w/2
                    y_camera=pt[1]+h/2
                    y_cam= (x_camera-14)*15
                    x_cam= (y_camera-14)*17
                    print 'w',x_camera,'h',y_camera
                    break
                   
                cv2.imwrite('pinout1_1.png',frame)
                
                #create and save value in to a text
                file= open("pin_cam.txt","w")
                file.write("%d" %x_cam)
                file.write("\n")
                file.write("%d" %y_cam)
                file.write("\n")
                file.write("%d" %i)
                file.close()       
        
                # go to 1st line and seperate numbers
                with open('position.txt') as a:
                    pos=a.readlines()[0]
                    position=pos.split()
                    print position[0],position[1],position[2]
                    x_or=100*float(position[1])
                    y_or=100*float(position[2])
                    a.close()
                    
                #move to the new position
                x,y,z=point_tilt(x_or,y_or)
                x=x-x_cam
                y=y-y_cam
                z=z+35

                print x,y,z, "POSITON SENT second"
                if x>32767:
                    if x>65534:
                        x1=32767
                        x2=32767
                        x3=x-x1-x2
                    else:
                        x1=32767
                        x2=x-x1
                        x3=0
                elif x<32767:
                    x1=x
                    x2=0
                    x3=0
                if y>32767:
                    y1=32767
                    y2=y-32767
                elif y<32767:
                    y1=y
                    y2=0
                
                # put the position in a list
                re=[position_lines]
                re.append(x1)
                re.append(x2)
                re.append(x3)
                re.append(y1)
                re.append(y2)
                re.append(z)

                # client send position to server
                rq=client.write_registers(30,re,unit=8)
                time.sleep(0.2)
                cam=2                  
                rq=client.write_coil(102,False,unit=1)
                time.sleep(0.2)
                rq=client.write_coil(104,False,unit=1)
                time.sleep(0.2)
                rq=client.write_registers(2,[0],unit=1)
                time.sleep(0.2)
                
            elif a==False:
                cam=cam

        # client changes status to controller not requesting data
        rq=client.write_coil(100,False,unit=1)
        time.sleep(0.2)
        rq=client.write_coil(101,False,unit=1)
        time.sleep(0.2)
        i=1
        while i==1:
            stat=False
            while stat==False:
                try:
                    # if controller has finished movement for 1st time
                    rr=client.read_coils(101,1,unit=1)
                    time.sleep(0.2)
                    a=rr.bits[0]
                    stat=True
                except AttributeError as e:
                    log.error('error 2')
                    log.error(str(rr))
                    log.error(str(e))
                    time.sleep(0.2)
                
            if rr.bits[0]==True:
            #print "Spike Check tool"

                with open('pin_info.txt') as b:
                    print 'spike check'
                    pin=b.readlines()[0]
                    pin_info=pin.split()
                    print pin_info[0],pin_info[1],pin_info[2]
                    b.close()

                p=pin_info[0]
                th=pin_info[2]
                tl=pin_info[1]
                rmax=float(th)*1.2
                rmin=float(tl)*0.8

                print re_dir+" "+p+" "+th+" "+tl+" "+str(rmax)+" "+str(rmin)+" "+scope_mod+" "+scope_cnt+" "+scope_ip+" "+scope_port+" "+scope_channel

                time.sleep(1)
                rq=client.write_coil(101,False,unit=1)
                time.sleep(0.2)
        
                print 'SPIKE CHECK DONE first'
                i=2
                j=2
        
            elif a==False:
                i=i
              
        x_ref = x_site
        y_ref = y_site
        
#New lines...................................................................
        
        rq=client.write_registers(41,[0],unit=1)
        time.sleep(0.2)
        rq=client.write_registers(42,[0],unit=1)
        time.sleep(0.2)
        
        rq=client.write_registers(43,[0],unit=1)
        time.sleep(0.2)
        rq=client.write_registers(44,[0],unit=1)
        time.sleep(0.2)
        
        rq=client.write_registers(45,[0],unit=1)
        time.sleep(0.2)
        rq=client.write_registers(46,[0],unit=1)
        time.sleep(0.2)
        
        rq=client.write_registers(47,[0],unit=1)
        time.sleep(0.2)
        rq=client.write_registers(48,[0],unit=1)
        time.sleep(0.2)
        
        rq=client.write_registers(49,[0],unit=1)
        time.sleep(0.2)
        rq=client.write_registers(50,[0],unit=1)
        time.sleep(0.2)

    





       
        
        # move to next line
        while i <= position_lines:
            while j <=pin_lines:
                # initiate client
                client=ModbusClient('10.0.2.250', port=502)
                client.connect()
                
                # change status to moving mode
                rq=client.write_registers(0,[2],unit=1)
                time.sleep(0.2)

                stat=False
                while stat==False:
                    try:
                        # read coil 0 to check if controller is requesting data
                        rr=client.read_coils(100,1,unit=1)
                        time.sleep(0.2)
                        a=rr.bits[0]
                        stat=True
                    except AttributeError as e:
                        log.error('error 3')
                        log.error(str(rr))
                        log.error(str(e))
                        time.sleep(0.2)
                
                print rr.bits[0], "Request"

                # if controller is requesting data
                if rr.bits[0]==True:

                    # go to next line and seperate numbers
                    with open('position.txt') as a:
                        pos=a.readlines()[i - 1]
                        position=pos.split()
                        print position[0],position[1],position[2]
                        x_or=100*float(position[1])
                        y_or=100*float(position[2])
                        a.close()

                    #move offset
                    x,y,z=point_tilt(x_or,y_or)
                    x_t=x + x_offset
                    y_t=y + y_offset
                    z=0

                    x_site = (x_or /100)
                    y_site = (y_or /100)
                    
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
                    re=[position_lines]
                    re.append(x1)
                    re.append(x2)
                    re.append(x3)
                    re.append(y1)
                    re.append(y2)
                    re.append(z)

                    

                    #When both points are out of range
                    if (x_ref > x_upperlimit or x_ref < x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
                        rq = client.write_registers(40,[1],unit=1)
                        time.sleep(0.2)
                        print " VR 40 DETERMINED"
                        

                    #When both x_ref and x-or are in but y_coordinates are out.    
                    elif (x_ref < x_upperlimit and x_ref > x_lowerlimit) and (x_site < x_upperlimit or x_site > x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
                        if (x_ref <= 0):
                            rq = client.write_registers(41,[1],unit=1)
                            time.sleep(0.2)
                            print " VR 41 DETERMINED"
                        else:
                            rq = client.write_registers(50,[1],unit=1)
                            time.sleep(0.2)
                            print " VR 41.(2) DETERMINED"
                        
                    #When x_ref is IN , all others are out
                    elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
                        rq = client.write_registers(42,[1],unit=1)
                        time.sleep(0.2)
                        print " VR 42 DETERMINED"
                        
                    #When x_ref is in and y_ref and y_or are equal and outside
                    elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
                        if (y_ref == y_pin):
                            rq = client.write_registers(43,[1],unit=1)
                            time.sleep(0.2)
                            print " VR 43 DETERMINED"
                            
                    #When x_ref and x_or are outside but y_ref and y_pin are inside
                    elif (x_ref > x_upperlimit or x_ref < x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site < y_upperlimit or y_site > y_lowerlimit):
                        rq = client.write_registers(44,[1],unit=1)
                        time.sleep(0.2)
                        print " VR 44 DETERMINED"
                        
                    #When x_ref is inside and y_pin is inside
                    elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref > y_upperlimit or y_ref < y_lowerlimit) and (y_site < y_upperlimit or y_site > y_lowerlimit):
                        rq = client.write_registers(45,[1],unit=1)
                        time.sleep(0.2)
                        print " VR 45 DETERMINED"
                        
                    #When x_ref is outside and y_ref is inside, y_pin is outside and x_pin is inside
                    elif (x_ref > x_upperlimit or x_ref < x_lowerlimit) and (x_site < x_upperlimit or x_site > x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
                        rq = client.write_registers(46,[1],unit=1)
                        time.sleep(0.2)
                        print " VR 46 DETERMINED"

                    elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
                        rq = client.write_registers(47,[1],unit=1)
                        time.sleep(0.2)
                        print " VR 47 DETERMINED"

                    elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site < x_upperlimit or x_site > x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site > y_upperlimit or y_site < y_lowerlimit):
                        rq = client.write_registers(48,[1],unit=1)
                        time.sleep(0.2)
                        print " VR 48 DETERMINED"

                    elif (x_ref < x_upperlimit or x_ref > x_lowerlimit) and (x_site > x_upperlimit or x_site < x_lowerlimit) and (y_ref < y_upperlimit or y_ref > y_lowerlimit) and (y_site < y_upperlimit or y_site > y_lowerlimit):
                        rq = client.write_registers(49,[1],unit=1)
                        time.sleep(0.2)
                        print " VR 49 DETERMINED"

                    else:
                        print " NOTHING DETERMINED"


                    # client send position to server
                    rq=client.write_registers(10,re,unit=8)
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

                    x_ref = x_site
                    y_ref = y_site
                    
                    k=1
                    while k==1:
                        stat=False
                        while stat==False:
                            try:
                                # if controller has finished movement for 1st time
                                rr=client.read_coils(102,1,unit=1)
                                time.sleep(0.2)
                                a=rr.bits[0]
                                stat=True
                            except AttributeError as e:
                                log.error('error 2')
                                log.error(str(rr))
                                log.error(str(e))
                                time.sleep(0.2)
                            
                        if rr.bits[0]==True:
                        # save picture
                            time.sleep(0.5)
                     
                            # Number of frames to capture
                            num_frames = 1;

                            print "Picture {0} ".format(img_counter)
                             
                          
                            # Grab a few frames
                            for l in xrange(0, num_frames) :
                                ret, frame = cap.read()
                                # mirror the frame
                                frame = cv2.flip(frame, 1)
                                width = frame.shape[1]
                                height = frame.shape[0]
                                x=(width/2)-14
                                y=(height/2)-14
                                a=28
                                b=28
                                image=cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 2)
                                roi = frame[y:y+b, x:x+a]
                                crop_img = frame[y:y+b, x:x+a]
                                img_name = "pin.png".format(img_counter)
                                cv2.imwrite(img_name, frame)
                                img_counter += 1

                            k=2
                            cam=1
                            rq=client.write_registers(2,[1],unit=1)
                            time.sleep(0.2)
                            rq=client.write_coil(102,False,unit=1)
                            time.sleep(0.2)

                        elif a==False:
                            k=k

                    #Template matching
                    while cam==1:
                        stat=False
                        rq=client.write_registers(2,[1],unit=1)
                        time.sleep(0.2)
                        while stat==False:
                            try:
                                # if controller has finished movement for 1st time                   
                                rr=client.read_coils(104,1,unit=1)
                                time.sleep(0.2)
                                a=rr.bits[0]
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
                            print 'template1'

                            # mirror the frame
                            frame = cv2.flip(frame, 1)
                            width = frame.shape[1]
                            height = frame.shape[0]
                            x=(width/2)-14
                            y=(height/2)-14
                            a=28
                            b=28
                            image=cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 2)
                            roi = frame[y:y+b, x:x+a]
                            crop_img = frame[y:y+b, x:x+a]
                            #imagee=cv2.rectangle(frame, ((x+a/2), (y+b/2)), ((x+a/2), (y+b/2)), (255, 255, 0), 2)
                            img_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

                            template = cv2.imread('pintemplateneww.png',0)
                            w, h = template.shape[::-1]
                            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                            threshold = 0.7
                            x_cam=0
                            y_cam=0
                            loc = np.where( res >= threshold)
                            for pt in zip(*loc[::-1]):
                                print 'template2'
                                #cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
                                #print("Position:", pt[0])
                                #cv2.rectangle(crop_img, pt, (pt[0] + w, pt[1] + int(h/2)), (0,0,255), -1)
                                #crop_img = frame[200:350,950:1000]
                                #imagee=cv2.rectangle(frame, ((x+a/2), (y+b/2)), ((x+a/2), (y+b/2)), (255, 255, 0), 2)
                                cv2.circle(crop_img,((pt[0]+w/2) ,(pt[1]+h/2)),1,(0,255,0), 1)
                                x_camera=pt[0]+w/2
                                y_camera=pt[1]+h/2
                                y_cam= (x_camera-14)*15
                                x_cam= (y_camera-14)*17
                                print 'w',x_camera,'h',y_camera
                                break
                            '''time.sleep(0.5)
                            frame = cv2.imread('point33 1.png')
                            x=280
                            y=220
                            a=50
                            b=50
                            image= cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 2)
                            roi = frame[y:y+b, x:x+a]
                            crop_img = frame[220:270,280:330]
                                
                            img_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                            template = cv2.imread('pintemplate.png',0)
                            w, h = template.shape[::-1]

                            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                            threshold = 0.93
                            loc = np.where( res >= threshold)
                            for pt in zip(*loc[::-1]):
                                #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
                                #print("Position:", pt[0])
                                #cv2.rectange(img_rgb, pt, (pt[0] + w, pt[1] + int(h/2)), (0,0,255), -1)
                                cv2.circle(crop_img,((pt[0]+w/2) ,(pt[1]+h/2)),0,(0,255,0), 0)
                                print((pt[0]+w/2) ,(pt[1]+h/2))
                                x_camera=pt[0]+w/2
                                y_camera=pt[1]+h/2'''
                               
                            cv2.imwrite('pinout1_1.png',frame)
                            
                            #save the value into a text file
                            file= open("pin_cam.txt","w")
                            file.write("%d" %x_cam)
                            file.write("\n")
                            file.write("%d" %y_cam)
                            file.write("\n")
                            file.write("%d" %i)
                            file.close()
                               
                    
                            # go to 1st line and seperate numbers
                            with open('position.txt') as a:
                                pos=a.readlines()[i-1]
                                position=pos.split()
                                print position[0],position[1],position[2]
                                x_or=100*float(position[1])
                                y_or=100*float(position[2])
                                a.close()

                            x,y,z=point_tilt(x_or,y_or)
                            x=x-x_cam
                            y=y-y_cam
                            z=z+35

                            print x,y,z, "POSITON SENT second"
                            if x>32767:
                                if x>65534:
                                    x1=32767
                                    x2=32767
                                    x3=x-x1-x2
                                else:
                                    x1=32767
                                    x2=x-x1
                                    x3=0
                            elif x<32767:
                                x1=x
                                x2=0
                                x3=0
                            if y>32767:
                                y1=32767
                                y2=y-32767
                            elif y<32767:
                                y1=y
                                y2=0
                            
                            # put the position in a list
                            re=[position_lines]
                            re.append(x1)
                            re.append(x2)
                            re.append(x3)
                            re.append(y1)
                            re.append(y2)
                            re.append(z)

                            # client send position to server
                            rq=client.write_registers(30,re,unit=8)
                            time.sleep(0.2)
                            cam=2                                              
                            cam=2                  
                            rq=client.write_coil(102,False,unit=1)
                            time.sleep(0.2)
                            rq=client.write_coil(104,False,unit=1)
                            time.sleep(0.2)
                            rq=client.write_registers(2,[0],unit=1)
                            time.sleep(0.2)
                            
                        elif a==False:
                            cam=cam

                    # client changes status to controller not requesting data
                    rq=client.write_coil(100,False,unit=1)
                    time.sleep(0.2)
                    rq=client.write_coil(101,False,unit=1)
                    time.sleep(0.2)
                    
                    line=j

                    while j==line:

                        stat=False
                        while stat==False:
                            try:
                                # if controller has finished movement
                                rr=client.read_coils(101,1,unit=1)
                                time.sleep(0.2)
                                a=rr.bits[0]
                                #print a , 'waiting_spike'
                                stat=True
                            except AttributeError as e:
                                log.error('error 4')
                                log.error(str(rr))
                                log.error(str(e))
                                time.sleep(0.2)

                        if rr.bits[0]==True:

                            with open('pin_info.txt') as b:
                                pin=b.readlines()[j - 1]
                                pin_info=pin.split()
                                print pin_info[0],pin_info[1],pin_info[2]
                                b.close()

                            p=pin_info[0]
                            th=pin_info[2]
                            tl=pin_info[1]
                            rmax=float(th)*1.2
                            rmin=float(tl)*0.8

                            print re_dir+" "+p+" "+th+" "+tl+" "+str(rmax)+" "+str(rmin)+" "+scope_mod+" "+scope_cnt+" "+scope_ip+" "+scope_port+" "+scope_channel
                            print 'SPIKE CHECK'

                            time.sleep(1)
                            rq=client.write_coil(101,False,unit=1)
                            time.sleep(0.2)

                            print "done ", i, "\n"


 #New lines.....................................................................

                            rq=client.write_registers(41,[0],unit=1)
                            time.sleep(0.2)
                            rq=client.write_registers(42,[0],unit=1)
                            time.sleep(0.2)
                            
                            rq=client.write_registers(43,[0],unit=1)
                            time.sleep(0.2)
                            rq=client.write_registers(44,[0],unit=1)
                            time.sleep(0.2)
                            
                            rq=client.write_registers(45,[0],unit=1)
                            time.sleep(0.2)
                            rq=client.write_registers(46,[0],unit=1)
                            time.sleep(0.2)
                            
                            rq=client.write_registers(47,[0],unit=1)
                            time.sleep(0.2)
                            rq=client.write_registers(48,[0],unit=1)
                            time.sleep(0.2)
                            
                            rq=client.write_registers(49,[0],unit=1)
                            time.sleep(0.2)
                            rq=client.write_registers(50,[0],unit=1)
                            time.sleep(0.2)
 #....................................................................................       
                            client.close()
                            time.sleep(0.2)
                            print j
                            j=j+1
                            i=i+1

                            if j==pin_lines+1:
                                j=1

                            print j, i, position_lines, "\n \n \n"
                            if i==position_lines+1:
                                j=pin_lines+1
                                i=position_lines+2
                                print i
                                print j

                        elif a==False:
                            j=line


        print "PROCESS DONE"
        process=False
        video.release()

    # if controller is  moving
    else:
        # close client
        client.close()
