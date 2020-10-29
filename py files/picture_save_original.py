import cv2
import time
img_counter = 0

k=1
while k==1:
    if __name__ == '__main__' :
 
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
            cv2.imwrite(img_name, frame)
            img_counter += 1
     
        # Release video
        video.release()
        k=2
        img_rgb = cv2.imread(img_name)
        img_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        template = cv2.imread('pins.jpg',0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            #print("Position:", pt[0])
            #cv2.rectangle(crop_img, pt, (pt[0] + w, pt[1] + int(h/2)), (0,0,255), -1)
            cv2.circle(crop_img,((pt[0]+w/2) ,(pt[1]+h/2)),1,(0,255,0), 1)
            #crop_img = frame[200:350,950:1000]
            print 'pt[0]+w/2',(pt[0]+w/2),'pt[0]+h/2',(pt[0]+h/2)
            print 'w', crop_img.shape[1],'h', crop_img.shape[0]
            x_camera=(pt[0]+w/2)-10   #Centre of cropped image
            y_camera=(pt[0]+hi/2)-10  #centre of ropped image

