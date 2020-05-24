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


def init():
    for year in years:
        if year == '2019':
            month = yearmonth2019
        else:
            month = yearmonth2020
        for i in range(len(month)):
            days = dayOneAndThree
            if month[i] == "02":
                days = dayTwo
            if month[i] == '04':
                days = dayFour
            if month[i] == "12":
                days = dayTwlve
            for j in range(len(days)):
                dayTime = year + month[i] + days[j]
                newList = []
                # 男
                newList.append(0)
                # 女
                newList.append(0)
                newList.append(0)
                newList.append(0)
                newList.append(0)
                newList.append(0)
                newList.append(0)
                newList.append(0)
                datavalue.append({'day':dayTime,"value":newList})

#读取文件内容并返回行内容
def getFile(file,shnum):
    f=open_xls(file)
    table=f.sheets()[shnum]
    num=table.nrows
    index = 0
    for year in years:
        if year == '2019':
            month = yearmonth2019
        else:
            index+=30
            month = yearmonth2020
        for i in range(len(month)):
            days = dayOneAndThree
            if month[i] == "02":
                days = dayTwo
            if month[i] == '04':
                days = dayFour
            if month[i] == "12":
                days = dayTwlve
            for j in range(len(days)):
                dayTime = year + month[i] + days[j]
                print("正在读取:"+str(dayTime))
                dataIndex = -1
                for p in range(len(datavalue)):
                    if datavalue[p]['day'] == dayTime:
                        dataIndex=p
                        break

                for row in range(num):
                        rdata=table.row_values(row)
                        try:
                            time = str(rdata[4]).split(".")[0]


                            if time==dayTime:
                                #age
                                age = int(str(rdata[7]).split(".")[0])
                                print(age)
                                if age != 0:
                                    if age <= 18:
                                        datavalue[dataIndex]['value'][2]+=1
                                    elif age >= 19 and age <= 25:
                                        datavalue[dataIndex]['value'][3] += 1
                                    elif age >= 26 and age <= 29:
                                        datavalue[dataIndex]['value'][4] += 1
                                    elif age >= 30 and age <= 40:
                                        datavalue[dataIndex]['value'][5] += 1
                                    elif age >= 41 and age <= 60:
                                        datavalue[dataIndex]['value'][6] += 1
                                    elif age >= 61:
                                        datavalue[dataIndex]['value'][7] += 1
                                #sex
                                sex = int(str(rdata[9]).split(".")[0])
                                if sex == 0:
                                    datavalue[dataIndex]['value'][1] += 1
                                else:
                                    datavalue[dataIndex]['value'][0] += 1
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
    allxls=["../final/newWithSex.xls"] #列表中的为要读取文件的路径
    #存储所有读取的结果
    datavalue=[]
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
    init()
    for fl in allxls:
        f=open_xls(fl)
        x=getshnum(f)
        for shnum in range(x):
            print("正在读取文件："+str(fl)+"的第"+str(shnum)+"个sheet表的内容...")
            getFile(fl,shnum)
    print("文件读取完成")
    rvalue=[]
    for i in range(len(datavalue)):
        obj = []
        obj.append(datavalue[i]['day'])
        for j in range(len(datavalue[i]['value'])):
            obj.append(datavalue[i]['value'][j])
        rvalue.append(obj)

    endfile='../final/sexAndAge3.xls'
    wb=xlsxwriter.Workbook(endfile)
    #创建一个sheet工作对象
    ws=wb.add_worksheet()
    for a in range(len(rvalue)):
        for b in range(len(rvalue[a])):
            c=rvalue[a][b]
            ws.write(a,b,c)
    wb.close()
