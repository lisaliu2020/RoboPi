# Emotion Detector

Using OpenCV and Python Lisa will be creating haarcascades for smile and frown detection.

Anthony will create the web application using flask ... //anthony do this.

##Haarcascades

haarcascade_frontalface_default.xml -> frontal face detector *[not mine]*

sad.xml -> created a frown detector

smile_cascade.xml -> created a smile detector, this detects smiles with teeth

smile_closed_cascade.xml -> created a smile detector, this detects smiles without teeth

nohup.out -> output file while training cascades

##Python Files

picam.py -> python file to be able to collect information from the picamera using our created cascades and two buttons which will then log the information to our database which will be shown on our web application *[look at Web Application section]*

faceDetect_test.py -> python file to test cascades on webcam camera

images.py -> python file to collect negative images, remove the "ugly" images *[look at Data for Training Cascades section]*, and create the bg.txt file

##Data for Training Cascades

data_smiles | data_smiles_closed | frown_data_test -> data for training cascades

neg -> negative images for training

sad | smiles -> positive images for training

ugly -> to remove unnecessary images from negative images

bg.txt -> negative images text file

positives.vec | positives2.vec -> vector file for smile_cascade.xml *[look at Haarcascades section | positives.vec used]* and smile_closed_cascade.xml *[look at Haarcascades section | positives2.vec used]*. This is used for training the smile cascades.

sad.vec -> vector file for sad.xml *[look at Haarcascades section]*; this is used for training the frown cascade.

frown5050.jpg | frownB.jpg | sad.jpg -> frown positive images to train with

smile.jpg | smile3.jpg | smile5050.jpg -> smile positive images to train with

smile_emoji.jpg | frown_emoji.jpg -> smile emoji will show when the button is clicked to show that

#Web Application

application -> //anthony do this
