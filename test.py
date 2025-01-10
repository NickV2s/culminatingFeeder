import cv2
from matplotlib import pyplot as plt
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
face_cascade = cv2.CascadeClassifier('catfaces.xml')
img = cv2.imread("TestTabby.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
faces = face_cascade.detectMultiScale(img_gray,1,5)
for (x,y,w,h) in faces:  
    # To draw a rectangle in a face  
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)  
    roi_gray = img_gray[y:y+h, x:x+w]  
    roi_color = img[y:y+h, x:x+w]  
#cv2.imshow('img',img_rgb)
# plt.subplot(1, 1, 1)
# plt.imshow(img_rgb)
# plt.show()
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



