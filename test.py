import cv2
def dispense(food):
    return True
def captureImage():
    img = "Placeholder"
    return img
def waitTimeSet(current, waitTime):
    return current+waitTime
def timeCheck(current,waitTime):
    if current>=waitTime:
        return True
    else: 
        return False
motionDetected = True
pennyFound = True
pennyFood = 2
pennyWait = 0
tigerFound = False
tigerWait = 0
tigerFood = 3
img = cv2.imread("Tiger.jpg")
#img = cv2.resize(img,(700,935))
img = cv2.resize(img,(900,1200))

face_cascade = cv2.CascadeClassifier('catfacesExtended.xml')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(img_gray,1.2,2,minSize=(30,30))
if len(faces)!=0:
    for (x,y,w,h) in faces:  
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)  
        print(len(faces))
else:
    print("no faces")

while True:
    cv2.imshow('img',img)
    key = cv2.waitKey(0)
    if key == 27:  
        break

if motionDetected:
    img = captureImage()
    if pennyFound:
        if timeCheck(1417,1400):
            dispense(pennyFood)
            pennyWait=waitTimeSet(1417,300)
    elif tigerFound:
        if timeCheck(1417,1200):
            dispense(tigerFood)
            tigerWait=waitTimeSet(1417,200)  
    else:
        None     



