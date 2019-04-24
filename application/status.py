#!/usr/bin/python

#Import necessary libraries

import RPi.GPIO as GPIO
import time
import os
import sqlite3
import sys

from flask import Flask, render_template
app = Flask(__name__)

#Assign GPIO pins
happyButton = 17
sadButton = 27

#Variables
emotion = " "

#Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(happyButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sadButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#-----------------------------------------------------------
#SQLite Setup

db = sqlite3.connect('./log/emotionStatus.db')
cursor = db.cursor()
db.commit()

#-----------------------------------------------------------

def emotionStatus():

	emotionState = GPIO.input(17)
	emotionStateTwo = GPIO.input(27)

	if emotionState == False:
		emotion = "Happy"
		print emotion
	else:
		emotion = "Nothing"

	if emotionStateTwo == False:
		emotion = "Sad"
		print emotion
	else:
		emotion = "Nothing"

try:

	while True:

		emotionStatus()
		time.sleep(0.1)
	#END


except KeyboardInterrupt:
	os.system('clear')
	print('Your emotion has been recorded!')
	GPIO.cleanup()

