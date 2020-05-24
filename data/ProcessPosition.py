# -*- coding: utf-8 -*-
# 样本均值为：样本均值为：13.66，样本标准差为：9.36
# ------

#导入需要使用的包
import json
import random
import re
import time
import pandas as pd

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
            flag = False
            position = rdata[8]
            print(position)
            if "中国"==position:
                num=-1
                while num<0 or num>=len(positions):
                    num =int(random.normalvariate(13.66,9.36))
                print(num)
                rdata[8] =positions[num]


            datavalue.append(rdata)








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
    allxls=["../final/newYear.xls"] #列表中的为要读取文件的路径
    positions =["南海诸岛","北京","天津","上海","重庆","河北","河南","云南","辽宁",
                "黑龙江","湖南","安徽","山东","新疆","江苏","浙江","江西",
                "湖北","广西","甘肃","山西","内蒙古","陕西","吉林",
                "福建","贵州","广东","青海","西藏","四川","宁夏","海南","台湾","香港","澳门"]
    datavalue=[]
    for fl in allxls:
        f=open_xls(fl)
        x=getshnum(f)
        for shnum in range(x):
            print("正在读取文件："+str(fl)+"的第"+str(shnum)+"个sheet表的内容...")
            getFile(fl,shnum)
    print("文件读取完成")

    # df = pd.DataFrame(datavalue, columns =['value'])
    # u = df['value'].mean()
    # std = df['value'].std()
    # print("样本均值为：%.2f，样本标准差为：%.2f" % (u,std))
    # print('------')
    # for i in range(100):
    #     num =random.normalvariate(26.25,8.17)
    #     print(int(num))
    # 查看数据基本统计量

    endfile = '../final/final.xls'
    wb = xlsxwriter.Workbook(endfile)
    # 创建一个sheet工作对象
    ws = wb.add_worksheet()
    for a in range(len(datavalue)):
        for b in range(len(datavalue[a])):
            c = datavalue[a][b]
            ws.write(a, b, c)
    wb.close()

