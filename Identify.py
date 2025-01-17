#import libraries and functions from Motor
import cv2
import time
from datetime import datetime,timedelta
from Motor import *
from picamera2 import Picamera2
#Set constants as names of txt files to edit later
TIGER_DATA = "TigerData.txt"
PENNY_DATA = "PennyData.txt"
UNKNOWN_CAT = "Cat.txt"
#Function to save image data to txt file
def saveImgData(filename:str,data:list):
    dataStr = str(data)
    f = open(filename, "w")
    for line in data:
        f.write("%s\n" % line)
    f.close()
#Function to read data from txt file
def readImgData(filename:str):
    data = []
    f = open(filename, "r")
    while True:
        line=f.readline()
        if len(line)==0:
            break
        else:
            newDataLine = [0,0,0]
            tempLine=line.replace(']\n','').split(',')
            rValue=tempLine[0].strip(',[]')
            gValue=tempLine[1].strip(',[]')
            bValue=tempLine[2].strip(',[]\n]')
            newDataLine[0]=int(rValue)
            newDataLine[1]=int(gValue)
            newDataLine[2]=int(bValue)

            data.append(newDataLine)
    return data
#Function uses readImgData funtion to compare data from unknown cat to our saved cat data    
def compareImgData(file1:str,file2:str):
    percentage = 0.0
    catData1=readImgData(file1)
    catData2=readImgData(file2)
    for i in range(0,1250):
        for j in range(0,1250):
            if catData1[i] == catData2[j]:
                #Percentage is used as an integer value of how similar the unknown cat is to the saved data
                percentage+=1
    percentage = percentage/15625.0
    return percentage
#function to dispense food by accessing functions in Motor.py
def dispense(food):
    foodDispense(food)
    return True
#function to check if it has been long enough for the cat to eat and sets a new time that they can eat at based on the value given
def waitTime(filename,cat:list):
    #Current time
    time = datetime.now()
    f = open(filename, "r")
    line = f.readline()
    temp = line.split(",")
    #gets time they can eat again at
    waitTime=datetime.strptime(temp[cat[0]], "%Y-%m-%d %H:%M:%S.%f")
    if time>=waitTime:
        dispense(cat[1])
        waitTime = time + timedelta(hours=cat[2])
        print(waitTime)
    f = open(filename, "w")
    if cat[0]==0:
        f.write(str(waitTime) +"," + temp[1])
    else:
        f.write(temp[0]+"," +str(waitTime))
    f.close()
    return True
#arrays for cats representing identity, food amount, and wait time in hours
penny = [0,2,2]
tiger = [1,2,1] 
#load classifier and set up camera
face_cascade = cv2.CascadeClassifier('catfacesExtended.xml')
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640,480)})
picam2.configure(camera_config)
picam2.start()
#loop to contantly run and check for cats
while True:
    cv2.startWindowThread()
    img = picam2.capture_array()
    #looks for cat faces in image
    faces = face_cascade.detectMultiScale(img,1.2,2,minSize=(30,30))
    for (x,y,w,h) in faces: 
        #Draws a rectangle around cat face and crops the image to only contain the face in the square 
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cropped = img[y:y+h,x:x+w]
        centerX = int(w/2)
        centerY = int(h/2)
        #create empty list to add colour data later 
        data = []
        #starts going through pixels in a rectangle on their forhead and collects data
        for row in range(centerX-25,centerX):
            for col in range(centerY-25,centerY+25):
                r, g, b,x = cropped[row, col]
                newline = [r,g,b]
                data.append(newline)
                #sets section to red so user can see what has been added to data
                cropped[row,col] = (0,0,255,0)
        #saves the data to txt file
        saveImgData(UNKNOWN_CAT,data)
        #compares data of unknown cat to known cats
        tigerMatch=compareImgData(TIGER_DATA,UNKNOWN_CAT)
        pennyMatch=compareImgData(PENNY_DATA,UNKNOWN_CAT)            
        #checks percentage and picks one with higher percent match
        #Dispenses food and updates wait time
        if tigerMatch>pennyMatch:
            waitTime("waitTime.txt",tiger)
        elif pennyMatch>tigerMatch:
            waitTime("waitTime.txt",penny)
        else:
            continue
    #Shows image to user then starts loop again after 0.5 seconds and closes image
    cv2.imshow('img',img)
    time.sleep (0.5)
    cv2.destroyAllWindows