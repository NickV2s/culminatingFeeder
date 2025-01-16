from datetime import datetime,timedelta
time = datetime.now()
def waitTime(filename,cat:list):
    time = datetime.now()
    f = open(filename, "r")
    line = f.readline()
    temp = line.split(",")
    waitTime=datetime.strptime(temp[cat[0]], "%Y-%m-%d %H:%M:%S.%f")
    print(waitTime)
    if time>=waitTime:
        #dispense(cat[1])
        waitTime = time + timedelta(hours=cat[2])
        print(waitTime)
    f = open(filename, "w")
    if cat[0]==1:
        f.write(str(waitTime) +"," + temp[1])
    else:
        f.write(temp[0]+"," +str(waitTime))
    f.close()
    return
penny = [0,2,2]
tiger = [1,2,1] 
waitTime("waitTime.txt",penny)