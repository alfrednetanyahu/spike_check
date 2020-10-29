import cv2
import time
img_counter = 0

# Open Webcam
cap = cv2.VideoCapture(0) # 0 is camera device number, 0 is for internal webcam and 1 will access the first connected usb webcam

while(True):

    # Capture frame-by-frame
    ret, frame = cap.read()
    


    # Number of frames to capture
    num_frames = 2;

    print "Capturing {0} frames".format(num_frames)
     
    # Grab a few frames
    for i in xrange(0, num_frames) :
        time.sleep(1)
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
        img_name = "fid1_trial{0}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        img_counter += 1

    #template matching
        ###########################################################################################
                    template = cv2.imread('fidtemplateoriginal.png',0)
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
                        y_cam= (x_camera-15)*20
                        x_cam= (y_camera-15)*20
                        print 'w',x_camera,'h',y_camera
                        break
                       
                    cv2.imwrite('pinout1_1.png',frame)
#######################################################################################################3
                
    # Release video
    cap.release()
