import os
import time

path = "../resources/data/word/"
fileLists = os.listdir(path)
for fileList in fileLists:
    realPath = path + fileList
    fname = fileList.split(".txt")[0]
    print(fname)
    print(fname.split(".")[0])
    month = int(fname.split(".")[0])
    day = fname.split(".")[1]

    newName =""
    if month==12:
        newName = 0+int(day)
    if month==1:
        newName = 31+int(day)
    if month==2:
        newName = 62+int(day)
    if month==3:
        newName = 91+int(day)
    if month==4:
        newName = 122+int(day)
    newOne = path+str(newName)+".txt"
    os.rename(realPath,newOne)
    # fp = open(realPath,"r", encoding= 'utf-8')
    # for line in fp.readlines():
    #     print(line)
    # time.sleep(1)
