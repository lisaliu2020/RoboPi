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
happyButton = 26
sadButton = 27

#Variables

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

		emotionStatus()
		time.sleep(0.1)

		status = emotionStatus()

		#Update timestamp
		timeStamp = (time.strftime("%Y-%m-%d %H:%M:%S"))

		#Inserts into emotionFormat table within database
		if status == "Happy" or status == "Sad":
			cursor.execute('''INSERT INTO emotionFormat VALUES(?,?) ''', (timeStamp, status))
			db.commit()
			all_rows = cursor.execute('''SELECT * FROM emotionFormat''')
			os.system('clear')
			for row in all_rows:
				print('{0} : {1}'.format(row[0], row[1]))

		#END


except KeyboardInterrupt:
	os.system('clear')
	print('Your emotion has been recorded!')
	GPIO.cleanup()

