import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# -*- coding: utf-8 -*-


#导入需要使用的包
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
        rdata = table.row_values(row)
        age = int(str(rdata[7]).split(".")[0])
        if age==0:
            num = random.normalvariate(26.25, 8.17)
            rdata[7]=int(num)

        datavalue.append(rdata)


    return datavalue








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
    allxls=["../final/newComments.xls"] #列表中的为要读取文件的路径

    #存储所有读取的结果
    datavalue=[]
    for fl in allxls:
        f=open_xls(fl)
        x=getshnum(f)
        for shnum in range(x):
            print("正在读取文件："+str(fl)+"的第"+str(shnum)+"个sheet表的内容...")
            rvalue=getFile(fl,shnum)


    print("文件合并完成")
    endfile='../final/newYear.xls'
    wb=xlsxwriter.Workbook(endfile)
    #创建一个sheet工作对象
    ws=wb.add_worksheet()
    for a in range(len(datavalue)):
        for b in range(len(datavalue[a])):
            c=datavalue[a][b]
            ws.write(a,b,c)
    wb.close()


    # data = [87,77,92,68,80,78,84,77,81,80,80,77,92,86,
    # 76,80,81,75,77,72,81,72,84,86,80,68,77,87,
    # 76,77,78,92,75,80,78]
    #
    # df = pd.DataFrame(datavalue, columns =['value'])
    # u = df['value'].mean()
    # std = df['value'].std()
    # print("样本均值为：%.2f，样本标准差为：%.2f" % (u,std))
    # print('------')
    # for i in range(100):
    #     num =random.normalvariate(26.25,8.17)
    #     print(int(num))
    # 查看数据基本统计量


#样本均值为：26.25，样本标准差为：8.17