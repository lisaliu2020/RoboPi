#Enter server python script

#!/usr/bin/python

from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3

#Retrieve the data from the database
def getData():
	con = sqlite3.connect('../Enter database file name')
	cursor = con.cursor()

	for row in cursor.execute("SELECT * FROM //Enter Table Name// ORDER by timestamp DESC LIMIT 1"):
		timeStamp = str(row[0])
		happy = row[1] #Happy will be set as a boolean value
		sad = row[2] #Sad will be set as a boolean value

	con.close()

	return timeStamp, happy, sad

#Main route
def index():
	timeStamp, happy, sad = getData()
	templateData = {
		'timeStamp': timeStamp,
		'happy': happy
		'sad': sad
	}

	return render_template('index.html', **templateData)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=False)
