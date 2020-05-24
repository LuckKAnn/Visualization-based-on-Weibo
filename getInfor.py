import datetime
import random
import sys

import xlrd
import xlwt
from bs4 import BeautifulSoup
import urllib.request
import json  # 使用了json格式存储

from tensorflow import name_scope

from WeiBoDto import WeiBoDto, WeiBoDtoPure
import  utils
from dto.CommentsDto import CommentsDto
from utils import  SaveUtils
import re
saveutil = SaveUtils()
import  time
import demjson
import requests
"""
    从网页端爬取微博基本内容，并得到其mid
    https://m.weibo.cn/detail/4479166621493445 手机端查看详情
    再前往: https://m.weibo.cn/statuses/extend?id={id} 是其json格式详情页面
    通过访问: https://m.weibo.cn/comments/hotflow?id={mid}&mid={mid} 获取到评论的json格式
        通过&max_id=143928019984375获取更多评论
    https://m.weibo.cn/api/container/getIndex?uid=3223933550&type=uid&value=3223933550 拿到基本信息，从中提取fid
    https://m.weibo.cn/api/container/getIndex?containerid=2302833223933550_-_INFO&title=基本资料&fid=2302833223933550 拿到基本资料，其中有性别和出生月份，所在地
"""

def getMids():

     # 读取excel文件 每个微博一次遍历 找到其评论，存储评论，评论者uid 以及max_id获取下一页
     workbook = xlrd.open_workbook("./comments.xls")  # 打开工作簿

     sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
     worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
     rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数

     for row in range(53637,rows_old):
         rdata = str(worksheet.row_values(row)[2])
         UID = rdata.split(".")[0]
         # print(mid)
         print("正在爬取用户:"+ str(worksheet.row_values(row)[3])+"的个人信息+++++++++++++++++++")
         url = "https://m.weibo.cn/api/container/getIndex?uid="+UID+"&type=uid&value="+UID

         getContainerId(UID,url)
         if len(InforList)>=100:
             utils.writeInfor(InforList)
             InforList.clear()
         #time.sleep(3)

     utils.writeInfor(InforList)


def getContainerId(UID,url):


    # cookie='ALF=1588931065; _T_WM=78985747470; SCF=ApsvDs9eEtaZkCRkyCM3ARpSlewlDe1xi8tHQI5rarCpv3WkNB7DROhToSyqQMsnGOU2mVsZqixwbaYuGHUY2wU.; SUB=_2A25zidxQDeRhGeBI7lEX8irOzDuIHXVRdeQYrDV6PUJbkdANLWLEkW1NRpYcTpAvhzN-yHoJKBBRWmzMP90DiYXY; SUHB=0G0uE5BTCvU1-A; MLOGIN=1; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=oid%3D4479166621493445%26luicode%3D10000011%26lfid%3D2302833223933550_-_INFO; XSRF-TOKEN=4231cf'
    # cookie="ALF=1588931065; SCF=ApsvDs9eEtaZkCRkyCM3ARpSlewlDe1xi8tHQI5rarCpv3WkNB7DROhToSyqQMsnGOU2mVsZqixwbaYuGHUY2wU.; SUB=_2A25zidxQDeRhGeBI7lEX8irOzDuIHXVRdeQYrDV6PUJbkdANLWLEkW1NRpYcTpAvhzN-yHoJKBBRWmzMP90DiYXY; SUHB=0G0uE5BTCvU1-A; _T_WM=68854507744; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4497155043765555%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E7%2596%25AB%25E6%2583%2585; XSRF-TOKEN=897818; WEIBOCN_FROM=1110106030"
    cookie="_T_WM=68854507744; ALF=1590834268; SCF=Ag0TBP8S7QgCOkJDFEIRccNUQ-eHTSyLbgs4-LUtX-bsZbgsAsrSZmC-XBr9Olot-lzOPrQ3rtbt4GY_giRRZnE.; SUB=_2A25zrtcPDeRhGeBI7lEX8irOzDuIHXVRUPlHrDV6PUJbktAKLVWlkW1NRpYcTmrtLCAHAo_e_DBoq3pZhVCKga8m; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWeusGPeqr7FuodIZAJHU-W5JpX5K-hUgL.FoqcSKeceoBES0M2dJLoI7URwGyuIc_0; SUHB=0V5l2Fn_jLAajI; XSRF-TOKEN=3075a4; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174%26fid%3D4499417371742500%26oid%3D4499417371742500"

    headers = {"User-Agent": user_agent_list[random.randint(0, len(user_agent_list) - 1)],"Cookie": cookie}
    print("正在爬取:" + url)
    # print(headers)
    IP= random.choice(proxies)
    try:
        requests.adapters.DEFAULT_RETRIES = 3
        res = requests.get(url,proxies={"http": IP},headers=headers, timeout=8)
        print(res.text)
        jsonResult = res.json()

        if 'data' in jsonResult:
            tabInfor = jsonResult['data']['tabsInfo']['tabs']
            container  = tabInfor[0]['containerid']
            if container is not None:
                getInfor(UID,container)
    #
    except Exception as E:
        print(E)
    time.sleep(2)




def getInfor(UID,containerId):
    cookie="_T_WM=68854507744; ALF=1590834268; SCF=Ag0TBP8S7QgCOkJDFEIRccNUQ-eHTSyLbgs4-LUtX-bsZbgsAsrSZmC-XBr9Olot-lzOPrQ3rtbt4GY_giRRZnE.; SUB=_2A25zrtcPDeRhGeBI7lEX8irOzDuIHXVRUPlHrDV6PUJbktAKLVWlkW1NRpYcTmrtLCAHAo_e_DBoq3pZhVCKga8m; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWeusGPeqr7FuodIZAJHU-W5JpX5K-hUgL.FoqcSKeceoBES0M2dJLoI7URwGyuIc_0; SUHB=0V5l2Fn_jLAajI; XSRF-TOKEN=3075a4; MLOGIN=1; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302833223933550%26oid%3D4499417371742500%26fid%3D2302833223933550_-_INFO%26uicode%3D10000011"
    headers = {"User-Agent": user_agent_list[random.randint(0, len(user_agent_list) - 1)] ,"Cookie": cookie}
    url = "https://m.weibo.cn/api/container/getIndex?containerid="+str(containerId)+"_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid="+str(containerId)
    IP = random.choice(proxies)
    try:
        requests.adapters.DEFAULT_RETRIES = 3
        res = requests.get(url, proxies={"http": IP}, headers=headers, timeout=8)
        print(res.text)
        jsonResult = res.json()

        if 'data' in jsonResult:
            inforDiv = jsonResult['data']['cards']
            infors = inforDiv[1]['card_group']
            # print(infors)
            userInforList = []
            for info in infors:
                # print(info)

                if 'item_content' in info:
                    if 'item_name' in info:
                         tmp = {info['item_name']:info['item_content']}
                         userInforList.append(tmp)
                         print(tmp)
            uid ={"uid":UID}
            userInforList.append(uid)
            InforList.append(userInforList)



    except Exception as E:
        print(E)
    time.sleep(2)



    pass


if __name__ == "__main__":
    InforList = []
    proxies = [  # 'http://27.208.231.100:8060'
        "https://117.88.176.162:3000",
        # "http://1.193.245.3:9999"
        "https://115.49.74.102:8118",
        "https://117.88.176.221:3000",
        "https://58.254.220.116:52470","https://117.88.176.162:3000",
        "https://183.195.106.118:8118","https://223.68.190.130:8181",
        "https://27.184.157.205	8118","https://110.189.152.86:52277",
        "https://119.84.112.137:80",
        "https://183.250.255.86:63000",
        "https://218.76.253.201:61408",
        "https://121.237.149.206:3000",
        "https://221.218.102.146:33323",
        "https://218.75.69.50:39590",
        "https://222.95.144.59:3000",
        "https://121.237.149.136:3000",
        "https://121.237.148.179:3000",
        "https://117.88.177.153:3000",


    ]
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
    ]
    getMids()
