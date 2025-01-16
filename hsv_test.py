import cv2
import matplotlib.pyplot as plt
TIGER_DATA = "TigerData.txt"
PENNY_DATA = "PennyData.txt"
# import numpy as np
def saveArray(filename:str,data:str):
    f = open(filename, "w")
    f.write(data)
    f.close()
def readArray(filename:str):
    f = open(filename, "r")
    data=(f.read())
    return data     
img1 = cv2.imread("pennyTest.jpg")
img2 = cv2.imread("pennyTest.jpg")
face_cascade = cv2.CascadeClassifier("catfacesExtended.xml")
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
#plt.figure()
#gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
#gray = cv2.resize(gray,(480,640))
faces = face_cascade.detectMultiScale(gray,1.2,2,minSize=(30,30))

for (x,y,w,h) in faces:  
    cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),2)
    print(x,y,w,h)
    cropped = gray[y:y+h,x:x+w]
    centerX = int(w/2)
    centerY = int(h/2) 
    data = []
    for i in range(1,50):
        cropped[centerY,centerX+i] = (255,0,0)
        tests = cropped[[centerX,centerY]]
        hsv = cv2.cvtColor(tests, cv2.COLOR_RGB2HSV) 
        print(hsv[0][0][2])
        data.append(hsv[0][0][2])
    saveArray(PENNY_DATA,str(data))
    print(len(faces))
plt.imshow(cropped)
plt.show()

key = cv2.waitKey(0)
if key == 27:  
    cv2.destroyAllWindows