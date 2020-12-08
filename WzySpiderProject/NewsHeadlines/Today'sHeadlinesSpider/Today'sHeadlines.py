import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import xlwt
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import requests
import json

findName = re.compile(r'<h4 class="fz-big clamp2" vrsid="imgFlex.b84b8b8">(.*?)</h4>')
findTime = re.compile(r'<span class="cite-date">(.*?)</span></div>')
findSource = re.compile(r'<span class="">(.*?)</span>')


def main():
    dataList = []

    baseURL1 = "https://m.sogou.com/web/search/ajax_query.jsp?type=1&dp=1&pid=sogou-waps-5b4e201ba2043c10&rcer=hNz_abkU5hEzbFxf3&m2web=news.sogou.com&keyword=%E4%B8%AD%E5%9B%BD%E7%96%AB%E6%83%85&suuid=dbaf6e96-9cff-4eef-8962-dedaa2e53891&p="
    baseURL2 = "&s_from=pagenext&showextquery=1&IPLOC=&insite="
    for i in range(2, 70):
        html = askURL(baseURL1, baseURL2, i)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="text-layout"):
            data = []
            item = str(item)
            name = re.findall(findName, item)
            if (name):
                data.append(name[0].replace("<em>", "").replace("</em>", ""))
            time = re.findall(findTime, item)
            if (time):
                data.append(time[0])
            source = re.findall(findSource, item)
            if (source):
                data.append(source[0])
            dataList.append(data)

    saveData(dataList)



def askURL(baseURL1, baseURL2, i):
    response = requests.get(baseURL1 + str(i) + baseURL2)
    html = response.text
    return html



def saveData(dataList):
    cnt = 0
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    for i in range(0, len(dataList)):
        data = dataList[i]
        if (len(data)==3):
            worksheet.write( cnt, 0, data[0])
            worksheet.write( cnt, 1, data[1])
            worksheet.write( cnt, 2, data[2])
            cnt = cnt+1
    workbook.save('今日头条有关疫情的新闻信息.xls')



if __name__ == '__main__':
    main()
