import cv2
import matplotlib.pyplot as plt
# import numpy as np
img1 = cv2.imread("pennyTest.jpg")
img2 = cv2.imread("pennyTest.jpg")
face_cascade = cv2.CascadeClassifier("catfacesExtended.xml")
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
#plt.figure()
#gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
gray = cv2.resize(gray,(480,640))
faces = face_cascade.detectMultiScale(gray,1.2,2,minSize=(30,30))
for (x,y,w,h) in faces:  
    cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),2)
    centerX = int((x+w)/2)
    centerY = int((y+h)/2) 
    gray[centerX,centerY] = (255,0,0)
    tests = gray[[centerX,centerY]]
    hsv = cv2.cvtColor(tests, cv2.COLOR_RGB2HSV) 
    print(hsv[0][0])
    print(len(faces))
plt.imshow(gray)
plt.show()

key = cv2.waitKey(0)
if key == 27:  
    cv2.destroyAllWindows