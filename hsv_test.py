import cv2
import matplotlib.pyplot as plt
TIGER_DATA = "TigerData.txt"
PENNY_DATA = "PennyData.txt"
UNKNOWN_CAT = "Cat.txt"
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
rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
#plt.figure()
#gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
#gray = cv2.resize(gray,(480,640))
faces = face_cascade.detectMultiScale(rgb,1.2,2,minSize=(30,30))

for (x,y,w,h) in faces:  
    cv2.rectangle(rgb,(x,y),(x+w,y+h),(0,255,0),2)
    print(x,y,w,h)
    cropped = rgb[y:y+h,x:x+w]
    centerX = int(w/2)
    centerY = int(h/2) 
    data = []
    for row in range(centerX-25,centerX+25):
        for col in range(centerY-25,centerY+25):
            r, g, b = cropped[row, col]
            print(f"Pixel {row*25+col} at (row {row}, col {col}): [{r}, {g}, {b}]")
            data.append(f"[{r},{g},{b}]")
            cropped[row,col] = (255,0,0)
    # for i in range(1,50):
    #     for j in range(1,50):
    #         tests = cropped[[centerX+j,centerY+i]]
    #         #hsv = cv2.cvtColor(tests, cv2.COLOR_RGB2HSV) 
    #         print(tests[0][0])
    #         data.append(tests[0][0])
    #         cropped[centerY+j,centerX+i] = (255,0,0)

    saveArray(UNKNOWN_CAT,str(data))
    print(len(faces))
plt.imshow(cropped)
plt.show()

key = cv2.waitKey(0)
if key == 27:  
    cv2.destroyAllWindows