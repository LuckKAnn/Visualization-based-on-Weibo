# -*- coding: utf-8 -*-
import json
import xlwt
import datetime
import traceback
import sys

import xlrd
import xlwt
from xlutils.copy import copy


class SaveUtils(object):
    # 导出excel/csv
    def __init__(self):
        self.row = int(1)
        self.wb = xlwt.Workbook(encoding="utf-8")
        self.ws = self.wb.add_sheet(u"Excel Name", cell_overwrite_ok=True)
        self.ws.write(0, 0, u"编号")
        self.ws.write(0, 1, u"文本内容")
        self.ws.write(0, 2, u"文本属性")
        self.ws.write(0, 3, u"时间")
        self.ws.write(0, 4, u"点赞数")
        self.ws.write(0, 5, u"评论数")
        self.ws.write(0, 6, u"转发数")

        self.ws.col(1).width = 10000
        # self.ws.col(2).width = 5000
        # self.ws.col(0).width = 5000

    def save(self, WeiBoDto):
        try:

            n = 0
            self.ws.write(self.row, 0, WeiBoDto.id)
            self.ws.write(self.row, 1, WeiBoDto.comments)
            self.ws.write(self.row,2, WeiBoDto.type)
            self.ws.write(self.row, 3, WeiBoDto.time)
            self.ws.write(self.row, 4, WeiBoDto.transfer)
            self.ws.write(self.row,5, WeiBoDto.comment)
            self.ws.write(self.row,6, WeiBoDto.good)
            self.row += 1

        except Exception:
            traceback.print_exc()


# if __name__ =="__main__":
#         q = QueryFromMysqlToExcelManage()
#         q.ip_manage("sadas")
#         q.wb.save("./Excel_导出.xls")

def write_excel_xls_append(WeiBoDto):
    # index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook("./mydata.xls")  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格

    new_worksheet.write(rows_old, 0, WeiBoDto.id)
    new_worksheet.write(rows_old, 1, WeiBoDto.comments)
    new_worksheet.write(rows_old, 2, WeiBoDto.type)
    new_worksheet.write(rows_old, 3, WeiBoDto.time)
    new_worksheet.write(rows_old, 4, WeiBoDto.transfer)
    new_worksheet.write(rows_old, 5, WeiBoDto.comment)
    new_worksheet.write(rows_old, 6, WeiBoDto.good)
    new_workbook.save("./mydata.xls")  # 保存工作簿
    # print("xls格式表格【追加】写入数据成功！")
def write_excel_list(WeiBoDtoList):
    # index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook("./mydata.xls")  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for WeiBoDto in WeiBoDtoList:
        new_worksheet.write(rows_old, 0, WeiBoDto.id)
        new_worksheet.write(rows_old, 1, WeiBoDto.comments)
        new_worksheet.write(rows_old, 2, WeiBoDto.type)
        new_worksheet.write(rows_old, 3, WeiBoDto.time)
        new_worksheet.write(rows_old, 4, WeiBoDto.transfer)
        new_worksheet.write(rows_old, 5, WeiBoDto.comment)
        new_worksheet.write(rows_old, 6, WeiBoDto.good)
        rows_old+=1

    new_workbook.save("./mydata.xls")  # 保存工作簿


def write_excel_weibo(WeiBoDtoList):
    # index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook("./weibo03-2.xls")  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数

    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格

    for WeiBoDto in WeiBoDtoList:
        try:
            new_worksheet.write(rows_old, 0, WeiBoDto.mid)
            new_worksheet.write(rows_old, 1, WeiBoDto.countName)
            new_worksheet.write(rows_old, 2, WeiBoDto.contents)
            new_worksheet.write(rows_old, 3, WeiBoDto.time)
            new_worksheet.write(rows_old, 4, WeiBoDto.comment)
            new_worksheet.write(rows_old, 5, WeiBoDto.transfer)
            new_worksheet.write(rows_old, 6, WeiBoDto.good)
            # new_worksheet.write(rows_old, 7, int(WeiBoDto.comment)*0.5+int(WeiBoDto.transfer)*0.3+int(WeiBoDto.good)*0.2)
            rows_old+=1
        except Exception as E:
            print(E)
    print("***************************当前已写入行数" + str(rows_old) + "***********************************")
    new_workbook.save("./weibo03-2.xls")  # 保存工作簿


def writeContents(CommentsDtos):
    # index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook("./comments03.xls")  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数

    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格

    for CommentsDto in CommentsDtos:
        try:
            new_worksheet.write(rows_old, 0, CommentsDto.mid)
            new_worksheet.write(rows_old, 1, CommentsDto.content)
            new_worksheet.write(rows_old, 3, CommentsDto.Name)
            new_worksheet.write(rows_old, 2, CommentsDto.fid)

            # new_worksheet.write(rows_old, 7, int(WeiBoDto.comment)*0.5+int(WeiBoDto.transfer)*0.3+int(WeiBoDto.good)*0.2)
            rows_old+=1
        except Exception as E:
            print(E)
    print("***************************当前已写入行数" + str(rows_old) + "***********************************")
    new_workbook.save("./comments03.xls")  # 保存工作簿

def writeInfor(inforLists):
    # index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook("./infor.xls")  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数

    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格

    for inforList in inforLists:
        try:
            sex = "未知"
            birth = "未知"
            address = "中国"
            uid = ""
            for eachInfo in inforList:
                for key in eachInfo.keys():

                    if(key=="性别"and key.strip()!=""):
                        sex = eachInfo[key]
                    if (key == "生日" and key.strip()!=""):

                        birth = eachInfo[key]
                    if (key == "所在地"and key.strip()!=""):
                        address = eachInfo[key]
                    if (key == "uid" and key.strip()!=""):
                        uid = eachInfo[key]
            new_worksheet.write(rows_old, 0, uid)
            new_worksheet.write(rows_old, 1, sex)
            new_worksheet.write(rows_old, 2, birth)
            new_worksheet.write(rows_old, 3, address)


            # new_worksheet.write(rows_old, 7, int(WeiBoDto.comment)*0.5+int(WeiBoDto.transfer)*0.3+int(WeiBoDto.good)*0.2)
            rows_old+=1
        except Exception as E:
            print(E)
    print("***************************当前已写入行数" + str(rows_old) + "***********************************")
    new_workbook.save("./infor.xls")  # 保存工作簿