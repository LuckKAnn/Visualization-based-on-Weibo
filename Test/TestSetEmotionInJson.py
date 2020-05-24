import json
import os
import time

path = "../resources/data/emotion/"
fileLists = os.listdir(path)
# for fileList in fileLists:
#     realPath = path + fileList
datavalue= {"date":[]}

for i in range(1,102):
    # print(path+str(i)+".txt")
    realPath = path+str(i)+".txt"
    print("正在处理"+str(i))
    fp = open(realPath,"r", encoding= 'utf-8')
    nameList =[]
    value1=[]
    value2=[]
    for line in fp.readlines():
        try:
            word = line.split("\t")[0]
            firstNum = line.split("\t")[1].split(" ")[0]
            secondNum = line.split("\t")[1].split(" ")[6]
            secondNum = secondNum.split("\n")[0]
            nameList.append(word)
            value1.append(float(firstNum))
            value2.append(float(secondNum))
            print(word,end=" ")
            print(firstNum,end=" ")
            print(secondNum)
        except Exception as E:
            print(E)

    datavalue['date'].append({"name": nameList, "value1": value1, "value2":value2})

jtxt = json.dumps(datavalue)
print(jtxt)
file_write_obj = open("../resources/data/emotion.txt", 'w')
file_write_obj.write(jtxt)
        # print(line.split("\t")[0],end="  ")
        # print(line.split("\t")[0].split(" "))
        # print(line.split("\t")[6].split(" "))
        # print(line)
        # print(type(line))
    # time.sleep(1)
    # print(realPath)