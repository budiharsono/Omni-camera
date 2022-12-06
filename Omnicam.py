import cv2
import math
import numpy as np

cam = cv2.VideoCapture(0)
cam.set(3,1280)
cam.set(4,720)

mask = np.zeros((720,1280), dtype='uint8')
cv2.circle(mask, (650,390), 325, 255, -1)

if not cam.isOpened():
    print('Tidak dapat mengakses kamera')
    exit()

while True:
    ret, frame = cam.read()
    if ret:
        cv2.circle(frame, (650,390), 5, (0,0,255),-1)
        masked = cv2.bitwise_and(frame,frame, mask=mask)
        hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
        mask_ball = cv2.inRange(hsv, (0,150,150), (20,255,255))
        imask = mask>0
        obyek = np.zeros_like(masked, np.uint8)
        obyek[imask] = masked[imask]
        cnts = cv2.findContours(mask_ball.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) >0:
            c= max(cnts, key=cv2.contourArea)
            ((x,y),radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            if M['m00']==0:
                continue
            center = (int(M["m10"]/M["m00"]), int(M['m01']/M['m00']))
            if radius > 10:
                cv2.circle(masked, (int(x), int(y)), int(radius),
                           (0,0,255), 2)
                cv2.circle(masked, center, 5, (255, 0, 0), -1)
                cv2.line(masked, (650,390), (650,70), (0,0,255), 1)
                cv2.line(masked, (650,390), center, (255,0,0), 1)
                if int(y) > 390:
                    if int(x) < 650:
                        sudut = -(round(((math.atan((int(y)-390.0)/(650.0-int(x)))/math.pi)*180+90),2))
                    elif int(x) > 650:
                        sudut = round(((math.atan((int(y)-390.0)/(int(x)-650.0))/math.pi)*180+90),2)
                    else:
                        sudut = 180.00
                else:
                    if int(x) < 650:
                        sudut = round(((math.atan((390.0-int(y))/(650.0-int(x)))/math.pi)*180-90),2)
                    elif int(x) > 650:
                        sudut = round(90-((math.atan((390.0-int(y))/(int(x)-650.0))/math.pi)*180),2)
                    else:
                        sudut = 0.00    
                cv2.ellipse(masked, (650,390), (int(math.sqrt((int(x)-650)**2+ (int(y)-390)**2))-20,int(math.sqrt((int(x)-650)**2+ (int(y)-390)**2))-20), 270, 0 ,sudut, 255, 5)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(masked, str(sudut), (int(x),int(y)*2//3),font,1,(0,255,0),3,cv2.LINE_AA)
                jarak = round(math.sqrt((650.0-int(x))**2+(int(y)-390.0)**2))
                cv2.putText(masked, str(jarak)+ 'px', (int(x)+(650-int(x))//2, int(y)+(390-int(y))//2), font, 1, (0,255,0),3,cv2.LINE_AA)
        
        cv2.imshow('Video', masked)
        key=cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
        
print('Selesai')
    
