
#!/usr/bin/python

from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3


#Retrieve the data from the database

con = sqlite3.connect('./log/emotionStatus.db')
cursor = con.cursor()

def getData():

	for row in cursor.execute("SELECT * FROM emotionFormat ORDER BY timestamp DESC LIMIT 1"):
		timeStamp = str(row[0])
		status = row[1]

	con.close()

	return timeStamp, status

def getChartData():
	cursor.execute("SELECT * FROM emotionFormat")
	data = cursor.fetchall()

	timeStamps = []
	statuses = []


	for row in reversed(data):
		timeStamps.append(row[0])
		statuses.append(row[1])

	return timeStamps, statuses

#Main route
@app.route("/")
def index():
	timeStamp, status = getChartData()
	templateData = {
		'timeStamp': timeStamp,
		'status': status
	}

	return render_template('index.html', **templateData)


if __name__ == "__main__":
	app.run(host = '0.0.0.0', port=80, debug=False)
