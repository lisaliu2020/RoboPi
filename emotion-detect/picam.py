#Import libraries for picamera
import picamera
import picamera.array
import numpy as np
import cv2
import time
import io

#Python image opener library
from PIL import Image

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

#boolean variables for smiles and frowns
smile = False
frown = False

#words to show what the camera status
cam_status = "words"

#get the cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('smile_cascade.xml')
smile_closed_cascade = cv2.CascadeClassifier('smile_closed_cascade.xml')
frown_cascade = cv2.CascadeClassifier('sad.xml')

#PiCamera function
def piCamera():
	#flag boolean
	flag = False
	while flag != True:
		#pi camera cature stream
		camera.capture(stream, format='jpeg', use_video_port = True)
		img = np.fromstring(stream.getvalue(), dtype=np.uint8)
		stream.seek(0)

		#get the images and turn an image gray
		img = cv2.imdecode(img, 1)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		#detects objects of different sizes -> returned as a list of rectangles
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		#use global variables
		global smile
		global frown
		global cam_status

		#If my camera is detecting a face there should be a blue rectangle around
		#the face. Get the gray image array and regular image array.
		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]

			#Detect the objects of different sizes -> returned as a list of rectangles
			smiles = smile_cascade.detectMultiScale(roi_gray)
			smiles_closed = smile_closed_cascade.detectMultiScale(roi_gray)
			frowns = frown_cascade.detectMultiScale(roi_gray)

			#If camera detects a face there should be a smile or a frown inside the face.
			#Put a red rectangle around the smile and a green rectangle around the frown.
			for (sx,sy,sw,sh) in smiles:
				cv2.rectangle(roi_color,(sx,sy),(sx+sw, sy+sh),(0,0,255),2)
				smile = True
				frown = False
				flag = True

			for (sx,sy,sw,sh) in smiles_closed:
				cv2.rectangle(roi_color,(sx,sy),(sx+sw, sy+sh),(0,0,255),2)
				smile = True
				frown = False
				flag = True

			for (sx,sy,sw,sh) in frowns:
				cv2.rectangle(roi_color,(sx,sy),(sx + sw, sy + sh), (0, 255, 0), 2)
				frown = True
				smile = False
				flag = True

		#when it breaks out of loop get cam_status string
		if smile == True:
			cam_status = "Smile"

		elif frown == True:
			cam_status = "Frown"

		else:
			cam_status = "None"

		#shows the video stream
		cv2.imshow('img', img)

		#exit stuff
		key = cv2.waitKey(1) & 0xff
		if key == ord("q"):
			break

	cv2.destroyAllWindows()

#------------------------------------------------------------------------------------------

#Assign GPIO pins
happyButton = 26
sadButton = 27

#Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(happyButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sadButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Create Window and images
cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
imgSmile = cv2.imread('smile_emoji.jpg',1)
imgFrown = cv2.imread('frown_emjoi.jpg',1)

#SQLite Setup
db = sqlite3.connect('./application/log/detectStatus.db')
cursor = db.cursor()
db.commit()

#emotion status funtion
def emotionStatus():
	flag = False

	#keey going until a button is clicked to define the person's actual emotion
	while flag != True:
		emotionState = GPIO.input(26)
		emotionStateTwo = GPIO.input(27)

		if emotionState == False:
			emotion = "Happy"
			cv2.imshow('image', imgSmile)
			flag = True

		elif emotionStateTwo == False:
			emotion = "Sad"
			cv2.imshow('image', imgFrown)
			flag = True

		else:
			emotion = "No Input"

	return emotion


try:

	while True:
		#call piCamera function
		piCamera()
		print(cam_status)

		status = emotionStatus()
		print(status)

		if cam_status == "Smile" and status == "Happy":
			robo_status = "True"

		elif cam_status == "Smile" and status == "Sad":
			robo_status = "False"

		elif cam_status == "Frown" and status == "Sad":
			robo_status = "True"

		elif cam_status == "Frown" and status == "Happy":
			robo_status = "False"

		else:
			robo_status = "None"


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

		time.sleep(10)
		#END

except KeyboardInterrupt:
	os.system('clear')
	db.close()
	print('Your emotion has been recorded')
	GPIO.cleanup()
