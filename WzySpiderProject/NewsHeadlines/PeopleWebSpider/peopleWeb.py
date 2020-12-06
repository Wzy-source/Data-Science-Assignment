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




def main():
    title_list = []
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8"
    }
    for page in range(1,191):
        baseURL = "http://search.people.cn/api-search/elasticSearch/search"
        data = {"key": "疫情", "page": str(page), "limit": "20", "hasTitle": "true", "hasContent": "true", "isFuzzy": "true",
                "type": "7", "domain": "opinion.people.com.cn", "sortType": "2", "startTime": "0", "endTime": "0"}
        try:
            jsonStr = json.dumps(data)
        except:
            print("json字符串转化出错")

        # 发出post请求+获取相应数据(.json()),得到json串，返回的是字典类型
        json_titles = requests.post(url=baseURL, headers=head, data=jsonStr).json()
        # title是在record中的字典中的value值
        # 每遍历一个record拿到的都是一个字典
        json_records = json_titles['data']
        for dic in json_records['records']:
            temp = dic["title"].replace("<em>", "").replace("</em>", "")
            title_list.append(temp)
        saveData(title_list)


def saveData(title_list):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    worksheet.write(0, 0, "文章标题")
    for i in range(0, len(title_list)):
        data = title_list[i]
        worksheet.write(i + 1, 0, data)
    workbook.save('"疫情"相关新闻标题.xls')


if __name__ == '__main__':
    main()
