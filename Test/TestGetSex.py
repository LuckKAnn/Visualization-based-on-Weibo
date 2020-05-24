# -*- coding: utf-8 -*-


#导入需要使用的包
import re
import time

import xlrd  #读取Excel文件的包
import xlsxwriter   #将文件写入Excel的包




#打开一个excel文件
def open_xls(file):
    f = xlrd.open_workbook(file)
    return f


#获取excel中所有的sheet表
def getsheet(f):
    return f.sheets()


#获取sheet表的行数
def get_Allrows(f,sheet):
    table=f.sheets()[sheet]
    return table.nrows


#读取文件内容并返回行内容
def getFile(file,shnum):
    f=open_xls(file)
    table=f.sheets()[shnum]
    num=table.nrows

    for row in range(num):
            rdata=table.row_values(row)
            try:
                sex = int(str(rdata[1]).split(".")[0])
                if sex ==0:
                    sexList[0]+=1
                else:
                    sexList[1]+=1

                print()



                # if rdata[4]

            except Exception as E:
                print(E)




#获取sheet表的个数
def getshnum(f):
    x=0
    sh=getsheet(f)
    for sheet in sh:
        x+=1
    return x






#函数入口
if __name__=='__main__':
    #定义要合并的excel文件列表
    # allxls=['../resources/tmp/2.17-3.13.xls','../resources/tmp/3.14-4.10.xls','../resources/tmp/12.27-1.21.xls','../resources/tmp/0122-0216.xls'] #列表中的为要读取文件的路径
    allxls=["./person_infor.xls"] #列表中的为要读取文件的路径
    #存储所有读取的结果
    datavalue=[]
    sexList = []
    sexList.append(0)
    sexList.append(0)


    for fl in allxls:
        f=open_xls(fl)
        x=getshnum(f)
        for shnum in range(x):
            print("正在读取文件："+str(fl)+"的第"+str(shnum)+"个sheet表的内容...")
            rvalue=getFile(fl,shnum)
    print("文件合并完成")
    for i in range(len(sexList)):
        print(sexList[i])