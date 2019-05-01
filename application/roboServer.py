#Enter server python script

#!/usr/bin/python

#from flask import Flask, render_template, request
#app = Flask(__name__)

import sqlite3

import matplotlib.pyplot as plt

#Retrieve the data from the database
def getData():
	con = sqlite3.connect('../log/emotionStatus.db')
	cursor = con.cursor()

	for row in cursor.execute("SELECT * FROM emotionFormat ORDER BY timestamp DESC LIMIT 1"):
		timeStamp = str(row[0])
		status = row[1]

	con.close()

	return timeStamp, status

def getChartData():
	cursor.execute("SELECT * FROM emotionFormat ORDER BY timestamp DESC LIMIT")
	data = cursor.fetchall()

	timeStamps = []
	statuses = []

	for row in reversed(data):
		timeStamps.append(row[0])
		statuses.append(row[1])

	return timeStamps, statuses

#Main route
#@app.route("/")
def index():
	timeStamp, status = getData()
	templateData = {
		'timeStamp': timeStamp,
		'status': status
	}

	return render_template('index.html', **templateData)


#@app.route("/plottable")
def plot_table():
	timeStamps, statuses = getChartData()

	fig = plt.figure()
	ax = fig.add_subplot(11)
	col_labels = ['Timestamp', 'Emotion']
	table_vals=[[timeStamps], [statuses]]

	#Draw Table
	the_table=plt.table(cellText=table_vals, colWidths=[0.1] * 3, colLabels=col_labels, loc='center')

	the_table.auto_set_font_size(False)
	the_table.set_fontsize(24)
	the_table.scale(4,4)

	plt.show()

try:
	plot_table()
