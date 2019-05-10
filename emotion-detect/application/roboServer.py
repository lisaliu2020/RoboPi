
#!/usr/bin/python

from flask import Flask, render_template, request, Response, jsonify
app = Flask(__name__)

import sqlite3
import json

#Retrieve the data from the database

con = sqlite3.connect('./log/emotionStatus.db')
cursor = con.cursor()

def getData():

	for row in cursor.execute("SELECT * FROM emotionFormat ORDER BY timestamp DESC LIMIT 1"):
		timeStamp = str(row[0])
		status = row[1]

	con.close()
	
	return timeStamp, status

@app.route("/tableData")
def getChartData():
	print ("tableData called")
	con.row_factory = sqlite3.Row
	cursor.execute("SELECT * FROM emotionFormat")
	data = cursor.fetchall()

	tableInfo = []

	for row in data:
		tableInfo.append({"timeStamp": row[0], "status": row[1]})
	print(tableInfo)
	
	return Response(json.dumps(tableInfo), mimetype='application/json')

#Main route
@app.route("/")
def index():

	return render_template('index.html')


if __name__ == "__main__":
	app.run(host = '0.0.0.0', port=80, debug=False)
