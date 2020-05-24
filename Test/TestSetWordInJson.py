import json
import os
import time

path = "../resources/data/word/"
fileLists = os.listdir(path)
# for fileList in fileLists:
#     realPath = path + fileList
datavalue= {"date":[]}

for i in range(1,133):
    # print(path+str(i)+".txt")
    realPath = path+str(i)+".txt"
    print("正在处理"+realPath)
    fp = open(realPath,"r", encoding= 'utf-8')
    tmp= []
    for line in fp.readlines():

          # print(line)
          # line = line.replace("\"","\'")
          # line = json.loads(line)
          # line = line.split("\n")[0]
          print(line)
          line = line.replace("\"","\'")
          # if  not line.endswith("\n") and not line.endswith(","):
          #     # print(line)
          #     line+=","

          dict = eval(line)
          print(type((dict)))
          print(type(type((dict))))

          # line = line.split('{"value":')[1]
          #
          # numb = line.split(",")[0]
          # word  =
          # time.sleep(10)
          if isinstance(dict,tuple):
               tmp.append(dict[0])
          else:
              tmp.append(dict)


    datavalue['date'].append(tmp)




jtxt = json.dumps(datavalue)
print(jtxt)
file_write_obj = open("../resources/data/word.txt", 'w')
file_write_obj.write(jtxt)
