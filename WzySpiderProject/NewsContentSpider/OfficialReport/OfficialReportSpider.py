import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import xlwt
import xlrd
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import requests
import json
import jieba


def main():
    cnt = 1
    workbook = xlwt.Workbook(encoding='GB2312')
    worksheet = workbook.add_sheet('sheet1')
    dataList = []
    URLlisit = getURLlist()
    for i in range(1200, 1500):
        print(i)
        data = []
        html = askURL(URLlisit[i])
        if (not html == 'error'):
            soup = BeautifulSoup(html, "html.parser")
            tempText = ""
            for item in soup.find_all(style="text-indent: 2em"):
                item = str(item).replace('<p style="text-indent: 2em">', '').replace("</p>", "").replace(
                    '<span style="text-indent: 2em">', "").replace("</span>", "")
                tempText += item
            index = tempText.find("<a href=")
            text = ""
            if (index > 0):
                text = tempText[0:index].replace("【相关阅读】", "")
                print(text)
                # data.append(URLlisit[i])
                # data.append(text)
                # dataList.append(data)
                # saveData(worksheet, dataList, cnt)
                # cnt = cnt + 1
                # dataList = []
            # if (len(dataList) == 50):
            #     saveData(dataList, sheetNum)
            #     sheetNum = sheetNum + 1
            #     dataList = []



def getURLlist():
    workbook = xlrd.open_workbook(
        "/Users/mac/PycharmProjects/BigHomework/Data Science Assignment/WzySpiderProject/NewsContentSpider/OfficialReport/疫情&抗疫相关新闻信息.xls")
    sheet = workbook.sheet_by_index(0)
    return sheet.col_values(3)


def askURL(URL):
    response = requests.get(URL)
    html = response.text
    return html


def saveData(worksheet, dataList, cnt):
    for i in range(0, len(dataList)):
        data = dataList[i]
        worksheet.write(cnt - 1, 0, data[0])
        worksheet.write(cnt - 1, 1, data[1])
        print("表格保存了第{}条新闻".format(cnt))


if __name__ == '__main__':
    main()
