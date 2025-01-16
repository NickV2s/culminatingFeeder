import cv2
import matplotlib.pyplot as plt
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
    for i in range(0,5000):
        for j in range(0,5000):
            if catData1[i] == catData2[j]:
                percentage+=1
    percentage = percentage/2500.0
    return percentage
img1 = cv2.imread("pennyTest.jpg")
img2 = cv2.imread("pennyTest.jpg")
face_cascade = cv2.CascadeClassifier("catfacesExtended.xml")
rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
faces = face_cascade.detectMultiScale(rgb,1.2,2,minSize=(100,100))

for (x,y,w,h) in faces:  
    cv2.rectangle(rgb,(x,y),(x+w,y+h),(0,255,0),2)
    print(x,y,w,h)
    cropped = rgb[y:y+h,x:x+w]
    centerX = int(w/2)
    centerY = int(h/2) 
    data = []
    for row in range(centerX-220,centerX-170):
        for col in range(centerY-50,centerY+50):
            r, g, b = cropped[row, col]
            print(f"Pixel {row*25+col} at (row {row}, col {col}): [{r}, {g}, {b}]")
            newline = [r,g,b]
            data.append(newline)
            cropped[row,col] = (255,0,0)
    saveImgData(UNKNOWN_CAT,data)
    saveImgData(PENNY_DATA, data)
    #print(compareImgData(UNKNOWN_CAT,TIGER_DATA))
    print(compareImgData(UNKNOWN_CAT,PENNY_DATA))

    print(len(faces))
plt.imshow(rgb)
plt.show()

key = cv2.waitKey(0)
if key == 27:  
    cv2.destroyAllWindows