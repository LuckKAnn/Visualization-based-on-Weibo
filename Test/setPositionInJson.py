# -*- coding: utf-8 -*-


#导入需要使用的包
import json
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
    count = 0
    for p in positions:
        # print(p)
        tmp = {"name":p,"value":0}

        for row in range(num):
                rdata=table.row_values(row)
                position = rdata[8]
                if p in position:
                    count +=1
                    tmp['value']+=1
            # print(position)
        datavalue['data'].append(tmp)

    print(count)








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
    allxls=["../final/newWithSex.xls"] #列表中的为要读取文件的路径
    #存储所有读取的结果
    datavalue={"data":[]}
    dayOneAndThree = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                      '17', '18', '19', '20', '21', '22', '23',
                      '24', '25', '26', '27', '28', '29', '30', '31']

    dayTwlve = ['01', '02', '03','04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                '21', '22', '23',
                '24', '25', '26', '27', '28', '29', '30', '31']

    dayOne = ['19', '20', '21', '22', '23',
              '24', '25', '26', '27', '28', '29', '30', '31']
    dayTwo = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
              '18', '19', '20', '21', '22', '23',
              '24', '25', '26', '27', '28', '29']
    dayFour = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
    # yearmonth2020= ["03",'04',"01","02"]
    yearmonth2020 = ["01", "02","03",'04']
    yearmonth2019 = ["12"]
    # years = ['2020','2019']
    years = ['2019',"2020"]

    positions =["南海诸岛","北京","天津","上海","重庆","河北","河南","云南","辽宁",
                "黑龙江","湖南","安徽","山东","新疆","江苏","浙江","江西",
                "湖北","广西","甘肃","山西","内蒙古","陕西","吉林",
                "福建","贵州","广东","青海","西藏","四川","宁夏","海南","台湾","香港","澳门"]
    for fl in allxls:
        f=open_xls(fl)
        x=getshnum(f)
        for shnum in range(x):
            print("正在读取文件："+str(fl)+"的第"+str(shnum)+"个sheet表的内容...")
            getFile(fl,shnum)
    print("文件读取完成")
    jtxt = json.dumps(datavalue)
    print(jtxt)
    file_write_obj = open("../final/position.txt", 'w')
    file_write_obj.write(jtxt)
