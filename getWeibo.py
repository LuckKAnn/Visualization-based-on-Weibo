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

def getRealLinks():

    dayOneAndThree = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23',
           '24','25','26','27','28','29','30','31']

    dayTwlve = ['04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23',
           '24','25','26','27','28','29','30','31']

    dayOne = [ '19', '20', '21', '22', '23',
                      '24', '25', '26', '27', '28', '29', '30', '31']
    dayTwo= ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23',
           '24','25','26','27','28','29']
    dayFour = ['01','02','03','04','05','06','07','08','09','10']
    # yearmonth2020= ["03",'04',"01","02"]
    yearmonth2020= ["01","02"]
    yearmonth2019= ["12"]
    # years = ['2020','2019']
    years = ['2019']
    WeiBoDtoList = []
    for year in years:
        month = ""
        if year=='2019':
            month=yearmonth2019
        else:
            month=yearmonth2020

        for i in range(len(month)):
            days = dayOneAndThree
            if month[i]=="01":
                days = dayOne
            if month[i]=="02":
                days = dayTwo
            if month[i]=='04':
                days = dayFour
            if month[i] == "12":
                days = dayTwlve
            for j in range(len(days)):
                dayTime = year+'-'+month[i]+'-'+days[j]
                # dayTime = "2019-12-06"
                print("+++++++++++++++++++++++++正在爬取"+dayTime+"数据+++++++++++++++++++++++")
                startTime =dayTime +'-0'
                endTime = dayTime+'-23'
                # url = 'https://s.weibo.com/weibo?q=%E6%96%B0%E5%86%A0%E7%97%85%E6%AF%92%7C%E6%96%B0%E5%86%A0%7C%E7%96%AB%E6%83%85%7C%E7%97%85%E6%AF%92%7C%E6%AD%A6%E6%B1%89%7CCOVID-19&xsort=hot&suball=1&' \
                #       'timescope=custom:'+startTime+':'+endTime
                for page in range(1,6):
                    print("++++++++++++++正在爬取第"+str(page)+"页++++++++++++++++++++++++++")
                    url = 'https://s.weibo.com/weibo?q=%E6%97%A5%7C%E6%88%96%7C%E7%9A%84%7C%E4%BA%86%7C%E6%96%B0&xsort=hot&suball=1&'\
                          'timescope=custom:' + startTime + ':' + endTime+'&Refer=g&page='+str(page)
                    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
                    cookie = 'SINAGLOBAL=5984400577652.446.1568472390521; SUHB=0D-Vfm7AvY9mhh; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWeusGPeqr7FuodIZAJHU-W5JpX5oz75NHD95QcSo-0SozXeoMNWs4DqcjGwGyRIc_uM7tt; ALF=1588934912; SUB=_2A25zidxQDeRhGeBI7lEX8irOzDuIHXVRdeQYrDV8PUJbkNAfLVrkkW1NRpYcTm0TVWbd94VBVuxABg0nenJgiw1q; UOR=www.csdn.net,widget.weibo.com,www.baidu.com; _s_tentry=-; Apache=4422827689863.431.1586604403454; ULV=1586604403573:14:4:4:4422827689863.431.1586604403454:1586575080480; WBStorage=42212210b087ca50|undefined; webim_unReadCount=%7B%22time%22%3A1586684769381%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A23%2C%22msgbox%22%3A0%7D'
                    headers = {"User-Agent": userAgent, "Cookie": cookie}
                    # print(url)
                    request = urllib.request.Request(url,headers=headers)
                    response = urllib.request.urlopen(request)
                    resHtml = response.read()

                    html = BeautifulSoup(resHtml, 'lxml')
                    # print(html)
                    # 错误检测:
                    error = html.select("div .m-error")
                    # try:
                    if len(error)==0:

                        mids = html.find_all(name='div', attrs={'class': {'card-wrap'}})
                        names = html.find_all(name='a', attrs={'class': {'name'}})
                        newNames = names[::-1]
                        # print(newNames)
                        # print(type(names))
                        # 拿到所有该页面的mid
                        weiboMidList = []

                        for mid in mids:
                            #每个天爬取其中至少二十个微博
                            if 'mid' in mid.attrs and len(weiboMidList)<=20:
                                countName = newNames.pop()
                                weiboMidList.append((mid['mid'],countName.text))

                        getDetail(weiboMidList,dayTime,WeiBoDtoList)
                    else:
                        print("出错")

                    if len(WeiBoDtoList)>=50 or dayTwo=="2019-12-31":
                        # utils.write_excel_list(WeiBoDtoList)
                        print("-------------------------正在写入数据------------------------------------------")
                        utils.write_excel_weibo(WeiBoDtoList)
                        WeiBoDtoList.clear()
                    # except Exception as E:
                    #     s = sys.exc_info()
                    #     print("Error '%s' happened on line %d" % (s[1], s[2].tb_lineno))
                        # print(E)


                # time.sleep(3)



def getDetail(weiboMidList,dayTime,WeiBoDtoList):
    for weibo in weiboMidList:
        weiboMid =weibo[0]
        countName = weibo[1]
        print("正在收集微博信息..........")
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
        # cookie='ALF=1588931065; _T_WM=78985747470; SCF=ApsvDs9eEtaZkCRkyCM3ARpSlewlDe1xi8tHQI5rarCpv3WkNB7DROhToSyqQMsnGOU2mVsZqixwbaYuGHUY2wU.; SUB=_2A25zidxQDeRhGeBI7lEX8irOzDuIHXVRdeQYrDV6PUJbkdANLWLEkW1NRpYcTpAvhzN-yHoJKBBRWmzMP90DiYXY; SUHB=0G0uE5BTCvU1-A; MLOGIN=1; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=oid%3D4479166621493445%26luicode%3D10000011%26lfid%3D2302833223933550_-_INFO; XSRF-TOKEN=4231cf'
        headers = {"User-Agent": user_agent_list[random.randint(0,len(user_agent_list)-1)]}

        url = "https://m.weibo.cn/statuses/extend?id=" + str(weiboMid)
        print("微博信息链接:"+url)
        r = requests.get(url,headers=headers)

        # cutHtml = re.compile(r'<[^>]+>', re.S)
        # jsonFile = cutHtml.sub('', str(r.json()))
        # tstr=jsonFile.replace("'","lkk")
        # tstr = tstr.replace("\"","aaa")
        # tstr=tstr.replace("lkk","\"")
        # tstr=tstr.replace("aaa","'")
        # tstr=tstr.replace("\\","")
        # print("微博Json:" + str(tstr))


        # jsonInfo = json.loads(str(html.select("body > p")[0])[3:-51])
        try:
            print("资源文件:"+r.text)
            jsonInfo = r.json()
            # print("微博Json:" + str(jsonInfo))
            if 'data' in jsonInfo:
                texts = jsonInfo['data']['longTextContent']
                cutHtml = re.compile(r'<[^>]+>', re.S)
                texts = cutHtml.sub('', texts)
                reposts = jsonInfo['data']['reposts_count']
                comments = jsonInfo['data']['comments_count']
                attitudes= jsonInfo['data']['attitudes_count']
                weiboDto = WeiBoDtoPure(weiboMid,countName,texts,dayTime,attitudes,comments,reposts)
                # utils.write_excel_xls_append(weiboDto)
                WeiBoDtoList.append(weiboDto)
        except Exception as E:
            print(E)
        time.sleep(3)



if __name__ == "__main__":
    getRealLinks()
