import picamera
import picamera.array
import numpy as np
import cv2
import time
import io

stream = io.BytesIO()
camera = picamera.PiCamera()
camera.resolution = (640, 480)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('smile_cascade.xml')
smile_closed_cascade = cv2.CascadeClassifier('smile_closed_cascade.xml')

while True:
	camera.capture(stream, format='jpeg', use_video_port = True)
	img = np.fromstring(stream.getvalue(), dtype=np.uint8)
	stream.seek(0)

	img = cv2.imdecode(img, 1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		smiles = smile_cascade.detectMultiScale(roi_gray)
		smiles_closed = smile_closed_cascade.detectMultiScale(roi_gray)

		for (sx,sy,sw,sh) in smiles:
			cv2.rectangle(roi_color,(sx,sy),(sx+sw, sy+sh),(0,0,255),2)

		for (sx,sy,sw,sh) in smiles_closed:
			cv2.rectangle(roi_color,(sx,sy),(sx+sw, sy+sh),(0,0,255),2)

	cv2.imshow('img', img)

	key = cv2.waitKey(1) & 0xff
	if key == ord("q"):
		break

cv2.destroyAllWindows()
