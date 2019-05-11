#!/usr/bin/python

#Import libraries for picamera
import picamera
import picamera.array
import numpy as np
import cv2
import time
import io

#Additional libraries for database logging and buttons
import RPi.GPIO as GPIO
import os
import sqlite3
import sys

#Flask
from flask import Flask, render_template
app = Flask(__name__)

#Variables for picamera
stream = io.BytesIO()
camera = picamera.PiCamera()
camera.resolution = (640, 480)

smile = False
frown = False

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('smile_cascade.xml')
smile_closed_cascade = cv2.CascadeClassifier('smile_closed_cascade.xml')
frown_cascade = cv2.CascadeClassifier('frown_cascade.xml')

#PiCamera function
def piCamera():
	camera.capture(stream, format='jpeg', use_video_port = True)
	img = np.fromstring(stream.getvalue(), dtype=np.uint8)
	stream.seek(0)

	img = cv2.imdecode(img, 1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	global smile
	global frown

	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		smiles = smile_cascade.detectMultiScale(roi_gray)
		smiles_closed = smile_closed_cascade.detectMultiScale(roi_gray)
		frowns = frown_cascade.detectMultiScale(roi_gray)

		for (sx,sy,sw,sh) in smiles:
			cv2.rectangle(roi_color,(sx,sy),(sx+sw, sy+sh),(0,0,255),2)
			smile = True
			frown = False

		for (sx,sy,sw,sh) in smiles_closed:
			cv2.rectangle(roi_color,(sx,sy),(sx+sw, sy+sh),(0,0,255),2)
			smile = True
			frown = False

		for (sx,sy,sw,sh) in frowns:
			cv2.rectangle(roi_color,(sx,sy),(sx + sw, sy + sh), (0, 255, 0), 2)
			frown = True
			smile = False

		cv2.imshow('img', img)

		key = cv2.waitKey(1) & 0xff
		if key == ord("q"):
			break

		cv2.destroyAllWindows()

		if smile == True:
			cam_emotion = "Smile"

		elif frown == True:
			cam_emotion = "Frown"

		else:
			cam_emotion = "None"

		return cam_emotion

#------------------------------------------------------------------------------------------
#Assign GPIO pins

happyButton = 26
sadButton = 27

#Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(happyButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sadButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#SQLite Setup

db = sqlite3.connect('./application/log/detectStatus.db')
cursor = db.cursor()
db.commit()


def emotionStatus():

	emotionState = GPIO.input(26)
	emotionStateTwo = GPIO.input(27)

	if emotionState == False:
		emotion = "Happy"

	elif emotionStateTwo == False:
		emotion = "Sad"

	else:
		emotion = "No Input"

	return emotion


try:

	while True:

		piCamera()

		emotionStatus()
		time.sleep(0.1)

		robo_status = "dkadasg"
		cam_status = piCamera()

		status = emotionStatus()

		if cam_status == "Smile" and status == "Happy":
			robo_status == "True"

		elif cam_status == "Smile" and status == "Sad":
			robo_status == "False"

		elif cam_status == "Frown" and status == "Sad":
			robo_status == "True"

		elif cam_status == "Frown" and status == "Happy":
			robo_status == "False"

		else:
			robo_status == "None"


		#Update timeStamp
		timeStamp = (time.strftime("%Y-%m-%d %H:%M:%S"))


		#Inserts into detectFormat table within database
		if((status == "Happy" or status == "Sad") and (cam_status == "Smile" or cam_status == "Frown")):
			cursor.execute('''INSERT INTO detectFormat VALUES(?,?,?,?) ''', (timeStamp, cam_status, status, robo_status))
			db.commit()
			all_rows = cursor.execute('''SELECT * FROM detectFormat''')
			os.system('clear')
			for row in all_rows:
				print('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3]))

		#END

except KeyboardInterrupt:
	os.system('clear')
	print('Your emotion has been recorded')
	GPIO.cleanup()
