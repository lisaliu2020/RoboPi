import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('/data/smile_cascade.xml')

'''
cameras = []
for i in range(0,199):
	cap = cv2.VideoCapture(i)
	if cap is None or not cap.isOpened():
        	print('Warning: unable to open video source: ', i)
	else:
		valid_cams.append(i)

print(cameras)
'''

cap = PiCamera()
rawCap = PiRGBArray(cap)


#while 1:
    #ret, img = cap.read()
   
for frame in cap.capture_continuous(rawCap, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
   
    #ret, img = cap.capture(rawCap, format="bgr")

   
    img = frame.array

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    '''    
    # add this
    # image, reject levels level weights.
    watches = watch_cascade.detectMultiScale(gray, 50, 50)
    
    # add this
    for (x,y,w,h) in watches:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
    '''
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
