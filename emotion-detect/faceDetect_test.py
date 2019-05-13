import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('smile_cascade.xml')
smile_close_cascade = cv2.CascadeClassifier('smile_closed_cascade.xml')
frown_cascade = cv2.CascadeClassifier('sad.xml')

cap = cv2.VideoCapture(0)

while 1:
	ret, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		smiles = smile_cascade.detectMultiScale(roi_gray)
		smiles_closed = smile_close_cascade.detectMultiScale(roi_gray)
		frowns = frown_cascade.detectMultiScale(roi_gray)

		for (sx,sy,sw,sh) in smiles:
			cv2.rectangle(roi_color,(sx,sy),(sx + sw, sy + sh), (0, 0, 255), 2)

		for (sx,sy,sw,sh) in smiles_closed:
			cv2.rectangle(roi_color,(sx,sy),(sx + sw, sy + sh), (0, 0, 255), 2)

		for (sx,sy,sw,sh) in frowns:
			cv2.rectangle(roi_color,(sx,sy),(sx + sw, sy + sh), (0, 255, 0), 2)


	cv2.imshow('img',img)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
