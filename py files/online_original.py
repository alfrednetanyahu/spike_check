import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("Fiducial Offset Calibration")

img_counter = 0

while True:
    ret, frame = cam.read()
      # mirror the frame
    width = frame.shape[1]
    height = frame.shape[0]

    
    
    x=(width/2)-10
    y=(height/2)-10
    a=20
    b=20
    
    val_x=x+a/2
    val_y=y+b/2
    image=cv2.rectangle(frame, (x,y), (x+a, y+b), (255, 255, 255), 2)
    dot = cv2.circle(image,(x+(a/2) ,y+(b/2)),1,(0,255,0), 1)
    
    cv2.imshow("Fiducial Offset Calibration", frame)

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
        

cam.release()

cv2.destroyAllWindows()

cam.release()

