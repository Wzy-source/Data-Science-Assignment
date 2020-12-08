import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import xlwt
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import requests
import json

'''
首页中对应的信息数据是通过阿贾克斯动态请求到的
'''
''''''


def main():
    findLink = re.compile(r'<a href="(.*?)" target="_blank">')
    finkTitle = re.compile(r' target="_blank">(.*?)</a>')
    findSource = re.compile(r'<span class="src"> (.*?)</span>')
    findTime = re.compile(r'<span class="tim">(.*?)</span>')
    findDis = re.compile('(?s)<p class="bre">(.*?)</p>')

    dataList = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Content-Type": "charset=UTF-8"}

    for page in range(0, 95):
        print("当前程序在page" + str(page + 1))
        baseURL = "https://www.mem.gov.cn/was5/web/search?channelid=297594&page=" + str(
            page + 1) + "&orderby=RELEVANCE&stype=0&sw=%E7%96%AB%E6%83%85&searchword=siteid=18%20and%20docreltime=%272019-12-01%27%20to%20%272020-12-08%27"
        requsetData = {"channelid": "297594",
                       "page": str(page + 1),
                       "orderby": "RELEVANCE",
                       "stype": "0",
                       "sw": "%E7%96%AB%E6%83%85",
                       "searchword": "siteid=18%20and%20docreltime=%272019-12-01%27%20to%20%272020-12-08%27"}
        # 注意这里的相应数据是一组text文件 or html文件
        html = requests.post(url=baseURL, headers=headers, data=requsetData).text
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('li'):
            data = []  # 保存一条新闻的所有信息
            item = str(item)
            '''
            '南京：上线“安全生产-<font color="#FF0000">疫情</font>摸排”系统 加强复工企业<font color="#FF0000">疫情</font>防控'
            '''
            title = re.findall(finkTitle, item)[0].strip()
            if (title):
                title = title.replace('<font color="#FF0000">', "").replace('<font color="#FF0000">', '').replace(
                    '</font>', '')
                data.append(title)
            else:
                data.append("暂无标题")
            time = re.findall(findTime, item)[0]
            if (time):
                data.append(time)
            else:
                data.append("暂无时间")
            source = re.findall(findSource, item)[0]
            if (source):
                data.append(source)
            else:
                data.append("暂无出处")
            link = re.findall(findLink, item)[0]
            if (link):
                data.append(link)
            else:
                data.append("暂无链接")
            describe = re.findall(findDis, item)[0].strip()
            if (len(describe)>0):
                describe = describe.replace('<font color="#FF0000">', "").replace('<font color="#FF0000">', '').replace(
                    '</font>', '')
                data.append(describe)
            else:
                data.append("暂无简介")
            dataList.append(data)
    saveData(dataList)


def saveData(dataList):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    for i in range(0, len(dataList)):
        '''
        1.题目
        2.时间
        3.出处
        4.URL
        5.简介
        '''
        data = dataList[i]
        worksheet.write(i, 0, data[0])
        worksheet.write(i, 1, data[1])
        worksheet.write(i, 2, data[2])
        worksheet.write(i, 3, data[3])
        worksheet.write(i, 4, data[4])
    workbook.save("疫情报导from国家应急管理部.xls")


if __name__ == '__main__':
    main()
