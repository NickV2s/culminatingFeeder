import cv2
import time
from datetime import datetime,timedelta
from Motor import *
from picamera2 import Picamera2
TIGER_DATA = "TigerData.txt"
PENNY_DATA = "PennyData.txt"
UNKNOWN_CAT = "Cat.txt"
def saveImgData(filename:str,data:list):
    dataStr = str(data)
    f = open(filename, "w")
    for line in data:
        f.write("%s\n" % line)
    f.close()
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
def compareImgData(file1:str,file2:str):
    percentage = 0.0
    catData1=readImgData(file1)
    catData2=readImgData(file2)
    for i in range(0,1250):
        for j in range(0,1250):
            if catData1[i] == catData2[j]:
                percentage+=1
    percentage = percentage/1562.5
    return percentage
def dispense(food):
    foodDispense(food)
    return True
def waitTime(filename,cat:list):
    time = datetime.now()
    f = open(filename, "r")
    line = f.readline()
    temp = line.split(",")
    waitTime=datetime.strptime(temp[cat[0]], "%Y-%m-%d %H:%M:%S.%f")
    print(waitTime)
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
penny = [0,2,2]
tiger = [1,2,1] 

face_cascade = cv2.CascadeClassifier('catfacesExtended.xml')
cv2.startWindowThread()
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640,480)})
picam2.configure(camera_config)
picam2.start()
while True:
    img = picam2.capture_array()
    faces = face_cascade.detectMultiScale(img,1.2,2,minSize=(30,30))
    for (x,y,w,h) in faces:  
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cropped = img[y:y+h,x:x+w]
        centerX = int(w/2)
        centerY = int(h/2) 
        data = []
        for row in range(centerX-25,centerX):
            for col in range(centerY-25,centerY+25):
                #print(cropped[row,col])
                r, g, b,x = cropped[row, col]
                #print(f"Pixel {row*25+col} at (row {row}, col {col}): [{r}, {g}, {b}]")
                newline = [r,g,b]
                data.append(newline)
                cropped[row,col] = (0,0,255,0)
        saveImgData(UNKNOWN_CAT,data)
        saveImgData(TIGER_DATA,data)
        compareImgData(TIGER_DATA,UNKNOWN_CAT)
        waitTime("waitTime.txt",tiger)
        print(len(faces))
    
    cv2.imshow('img',img)
    key = cv2.waitKey(0)
    if key == 27:  
        break
cv2.destroyAllWindows