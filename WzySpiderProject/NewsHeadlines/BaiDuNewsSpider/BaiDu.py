import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import xlwt
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import requests
import json


def main():
    dataList = []
    baseURL1 = "https://m.baidu.com/sf/vsearch?word=%E7%96%AB%E6%83%85&pd=realtime&tn=vsearch&pn="
    baseURL2 = "&sa=vs_tab&mod=5&p_type=1&data_type=json&atn=index&lid=9903324562811712514"
    for i in range(1, 29):
        URL = baseURL1 + str(i * 10) + baseURL2
        html = askURL(URL)

        # for i in range(0, len(contents)):
        #     data = []
        #     dicData = contents[i]
        #     try:
        #         if (dicData['title'] and dicData['posttime'] and dicData['subsitename'] and dicData[
        #             'abstract'] and dicData['avatar']):
        #             data.append(dicData['title']),
        #             data.append(dicData['posttime']),  # 发布时间
        #             data.append(dicData['subsitename']),  # 平台
        #             data.append(dicData['abstract']),  # 简介
        #             data.append(dicData['avatar'])  # 链接
        #     except:
        #         print("在处理数据字典时出错")
        #     dataList.append(data)

        htlmList = html.split(",")
        data = []
        for j in range(len(htlmList)):
            if(len(htlmList[j])>=13):
                if(htlmList[j][1:8]=="title"):
                    data.append(htlmList[j][9:])
                    print("添加了title,data的长度为{}".format(len(data)))
                    #"posttime"
                if(htlmList[j][1:11]=="posttime"):
                    data.append(htlmList[j][12:])
                    print("添加了posttime,data长度为{}".format(len(data)))
                    #"subsitename"
                if(htlmList[j][1:14]=="subsitename"):
                    data.append(htlmList[j][15:])
                    print("添加了subsitename,data的长度为{}".format(len(data)))
                    if(len(data)==3):
                        dataList.append(data)
                        data = []
                        print("清空了data")














def askURL(URL):
    response = requests.get(URL)
    html = response.text
    return html


if __name__ == '__main__':
    main()
