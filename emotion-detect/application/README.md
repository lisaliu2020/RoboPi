Edit this README.md file when the application is complete!!!

# Web Application Setup

A Flask web server application was established in which a google visualization table was displayed. The google
visualization table contains the content from the sqlite database table that is populated by the variables from 
the "picam.py" python script file from the "emotion-detect" directory.

Step 1:

(In the application directory):

-Create /log directory

-The database file created in the next few steps will be in this "log" directory.  


Step 2:

-Install sqlite3 and follow the appropriate steps under the "AnSQLiteSession.pdf" file on Google Classroom with respect to the picam.py file. 

-Sqlite will be used to create a table where the string for date timestamp, camera detection emotion status, button emotion status, and the "true or false" value can be recorded.

-The information from this table will be stored in a database file.    


Step 3:

-Establish a web page that displays the information within the database file:

-There are many ways to establish a web server. So utilize whatever software that you are comfortable with (i.e Flask, Node.js, lightpd, etc...). In this project, a Flask server was utilized. In order to create a functional flask server, a few things are required in the 
"application" directory:
  - a flask server python file that will require certain libraries and contain functions to fetch the data from the database table. These functions require app routes so they can be utilized in the index.html file. Also use JSON to transmit data. 
  
  - a "static" directory that can contain any javascript files that you may need to create the google visualiation table. You could also just establish the google visualization chart within the index.html file. 
  
  - a "templates" directory that contains the "index.html" file. 


Recommended:

	-Create an "index.html" file that references the javascript files in the "static" directory in order to create a web page that displays a visualization table showing the information within the database file. Or you could just create the visualization table in the index.html file. There are MANY ways to do this...So pick any method you please. 

	-Refer to online sources if necessary to help you establish a web server. Regardless of your method, make sure there is a way to display your Raspberry Pi's IP address and any port of your choosing to the console when you run your server. The port that you want the server to run on, should be referenced in the flask server python file. 
  
Step 4: 
  
-Run your flask server file. Go to your preferred browser. Type in your Raspberry PI's IP address along with the port number. It should be formatted as something like "0.0.0.0:80" 
 
-The web page should display the google visualization table that you created which graphically portrays the contents of the database file. The "picam.py" file was established so that each time it is run, new information is logged to the database table. That being said, each time the "picam.py" file is run, new information should be added to the visualization table that is displayed in the web browser.  
