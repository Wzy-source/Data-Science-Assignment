import random
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 网页源码的获取
from http.client import RemoteDisconnected
from time import sleep

from bs4 import BeautifulSoup
import xlwt
import xlrd
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import requests
import json

findMp = re.compile(r'value="跳页" />&nbsp;(.*)页')
findComment = re.compile(r'class="ctt">(.*?)</span>')  # 非贪婪匹配
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER"
    "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
    "Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3"
    "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0"
    "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
    "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"
]


def main():
    data = xlrd.open_workbook('微博id：健康中国.xls')
    sheet = data.sheet_by_index(0)
    rowNum = 4200  # 4243
    cnt = 0
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    worksheet.write(0, 0, "微博内容")
    worksheet.write(0, 1, "评论URL")
    worksheet.write(0, 2, "点赞数")
    worksheet.write(0, 3, "转发数")
    worksheet.write(0, 4, "发布时间")
    worksheet.write(0, 5, "评论数")
    contentDataList = []
    commentDataList = []

    for i in range(3500, rowNum):
        random_header = random.choice(my_headers)
        baseURL = sheet.cell(i, 1).value  # 获取到了每个评论列表的URL
        headers = {
            "user-agent": random_header,
            "cookie": "SCF=Aq-wzm_VWw29cRnKZxrp2ZmOysw2NZmQ1D5IsL0DcmGh0oyEzRW7FPL9UBFLvX3oeFUPW8Uk-AszNN8FHeSB6Hg.; SUB=_2A25y02tzDeRhGeNI7VQQ-CnJzD2IHXVuPHU7rDV6PUJbktANLXjdkW1NSFc-Dxr6wyLXvORIztrJ10QC2UVPue37; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2GhTGdOA9fqaWbVU.bEJF5NHD95QfSoqceKnNSKMpWs4DqcjsgHL9g-pQ; _T_WM=e289b4f22067e6f7e4de9c794df9ce43",
            "origin": "https://weibo.cn",
            "referer": "https://weibo.cn/jiankangzhongguo",
            "sec-fetch-dest": "document",
            "authority": "weibo.cn",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none"
        }
        sleep(random.randrange(100, 1000, 13) / 1000.0)

        # 先通过get请求获得具体的页数得到mp，然后使用post请求，formData的page从1到mp
        try:
            request = urllib.request.Request(url=baseURL, headers=headers)
            response = urllib.request.urlopen(request)
            Text_get = response.read().decode("utf-8")
            print("=====进入第{}个URL=====".format(i))
            '''
            网页形式：
            1.没有mp：评论内容不足一页
            2.含有mp：评论内容多于一页，可以通过re.findall(findMp,requestText_get)[0]获得mp
            注意：课程要求是获取"重点新闻（评论量远超（考虑数据分布）其它新闻的新闻）"则可以将评论筛
            选对象精确到含有mp值的评论。
            微博内容获取模式：soup中的text对象+筛选
            微博评论获取模式：html代码正则提取
            
            '''
            mp = re.findall(findMp, Text_get)
            if (len(mp) > 0):
                """
                HTTP Error 403: Forbidden!
                """
                realMaxPage = 0
                try:
                    maxPage = int(mp[0].split("/")[1])
                    realMaxPage = maxPage
                    if (maxPage > 50):
                        maxPage = 50  # 50页以后就没有评论了
                except:
                    maxPage = 0
                    print("maxPage格式转化错误")
                cnt = cnt + 1
                print("=====当前热门微博数：{}=====".format(cnt))
                firstPage = True
                commentData = []
                contentData = []
                for commentPage in range(1, maxPage + 1):
                    formData = {
                        "mp": str(realMaxPage),  # mp是评论的最大页数(确信)
                        "page": str(commentPage)
                    }
                    sleep(random.randrange(100, 1000, 3) / 713.0)
                    html = requests.post(url=baseURL, headers=headers, data=formData).text
                    print("=====获取到该微博下的第{}页=====".format(commentPage))
                    soup = BeautifulSoup(html, "html.parser")
                    if (firstPage):
                        contentData = []
                        # print(soup.text)
                        startIndex = soup.text.find(":") + 1  # 找到第一个 ：的位置
                        endIndex = soup.text.find("          ")  # 找到内容结束的位置
                        content = soup.text[startIndex:endIndex]
                        url = sheet.cell(i, 1).value
                        # commentNum = sheet.cell(i, 2).value
                        approveNum = sheet.cell(i, 3).value
                        transmitNum = sheet.cell(i, 4).value
                        time = sheet.cell(i, 5).value
                        contentData.append(content)  # 内容
                        contentData.append(url)  # URL
                        # contentData.append(commentNum)  # 评论数
                        contentData.append(approveNum)  # 点赞数
                        contentData.append(transmitNum)  # 转发数
                        contentData.append(time)  # 发布时间
                        firstPage = False
                        # contentDataList.append(contentData)
                        print("=====内容爬取完毕，contentData长度{}=====".format(len(contentData)))
                    print("=====现在爬取第{}页的评论=====".format(commentPage))
                    '''
                    评论有两种方式：
                    1.直接评论
                    2.回复模式
                    都先使用正则提取：
                    class="ctt"
                    再对第二种模式进行特殊处理
                    '''

                    soup = BeautifulSoup(html, "html.parser")
                    for item in soup.find_all('div', class_="c"):
                        comments = re.findall(findComment, str(item))
                        if (len(comments) > 0):
                            comment = comments[0]
                            if (len(comment) > 0 and comment[0:1] != ':' and (comment.find('<a href="') == -1) and (
                                    comment.find("<img alt=") == -1)):
                                if (comment[0:2] != "回复"):
                                    print(comment)
                                    if ((comment not in commentData) and (len(commentData) < 248)):
                                        commentData.append(comment)
                                else:
                                    primeIndex = comment.find("</a>:") + 5
                                    comment = comment[primeIndex:]
                                    if ((comment not in commentData) and (len(commentData) < 248)):
                                        commentData.append(comment)

                    print("=====该微博第{}页的评论爬取完毕=====".format(commentPage))
                contentData.append(len(commentData))
                contentDataList.append(contentData)
                commentDataList.append(commentData)
        except(urllib.error.URLError or RemoteDisconnected() or requests.exceptions.ConnectionError):
            print("ERROR")
    saveData(contentDataList, commentDataList, workbook, worksheet)

    # comments = re.findall(findComment, html)
    # if (len(comments) > 0):
    #     for Cnt in range(0, len(comments)):
    #         if (len(comments[Cnt]) > 0 and comments[Cnt][0:1] != ':'):
    #             if (comments[Cnt][0:2] != "回复"):
    #                 print(comments[Cnt])
    #                 commentData.append(comments[Cnt])
    #             else:
    #                 primeIndex = comments[Cnt].find("</a>:") + 1
    #                 print(comments[Cnt][primeIndex:])
    #                 commentData.append(comments[Cnt][primeIndex:])
    #     print("    该微博第{}页的评论爬取完毕".format(commentPage))
    #     if (len(contentData) > 0):
    #         commentDataList.append(contentData)


def saveData(content, comment, workbook, worksheet):
    for i in range(1, len(content) + 1):
        contentItem = content[i - 1]
        for j in range(0, len(contentItem)):
            worksheet.write(i, j, contentItem[j])
        commentItem = comment[i - 1]
        for j in range(0, len(commentItem)):
            worksheet.write(i, j + 6, commentItem[j])
    workbook.save("微博id：健康中国(热门含评论)7.xls")


if __name__ == '__main__':
    main()
