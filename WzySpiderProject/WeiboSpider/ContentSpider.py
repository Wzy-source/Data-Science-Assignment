import random
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 网页源码的获取
from time import sleep

from bs4 import BeautifulSoup
import xlwt
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import requests
import json

'''
首页中对应的信息数据是通过阿贾克斯动态请求到的
'''
findApproveNum = re.compile(r'赞(.*)<')
findCommentNum = re.compile(r'评论(.*)<')
findCommentURL = re.compile(r'https://weibo.cn/comment/(.*)">评论')
findTransmitNum = re.compile(r'转发(.*)</a>')
findTime = re.compile(r'class="ct">(.*)</span>')


def main():
    dataList = []
    baseURL = "https://weibo.cn/jiankangzhongguo"
    # page 1-445
    for page in range(2, 446):
        print("当前在爬取第{}页的数据".format(page))
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "cookie": "SCF=Aq-wzm_VWw29cRnKZxrp2ZmOysw2NZmQ1D5IsL0DcmGh0oyEzRW7FPL9UBFLvX3oeFUPW8Uk-AszNN8FHeSB6Hg.; SUB=_2A25y02tzDeRhGeNI7VQQ-CnJzD2IHXVuPHU7rDV6PUJbktANLXjdkW1NSFc-Dxr6wyLXvORIztrJ10QC2UVPue37; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2GhTGdOA9fqaWbVU.bEJF5NHD95QfSoqceKnNSKMpWs4DqcjsgHL9g-pQ; _T_WM=e289b4f22067e6f7e4de9c794df9ce43",
            "origin": "https://weibo.cn",
            "referer": "https://weibo.cn/jiankangzhongguo?page=" + str(page)
        }
        userData = {
            "mp": "1694",
            "page": str(page)
        }
        sleep(0.5)
        html = requests.post(url=baseURL, headers=headers, data=userData).text
        soup = BeautifulSoup(html, "html.parser")
        cnt = 1
        for item in soup.findAll(class_="c"):
            # print(item.text)
            content = item.text
            itemData = []  # 保存一个新闻的全部信息
            '''
            信息内容：
            1.点赞数
            2.转发数
            3.评论数
            4.评论链接
            5.发布时间
            '''
            item = str(item)
            length = len(re.findall(findCommentURL, item))
            if (length > 0):
                commentURL = "https://weibo.cn/comment/"+(re.findall(findCommentURL, item)[0].split('"')[0])
                commentNUm = re.findall(findCommentNum, item)[0].replace("[", "").replace("]", "").split("<")[0]
                approveNum = re.findall(findApproveNum, item)[0].replace("[", "").replace("]", "").split("<")[0]
                transNum = re.findall(findTransmitNum, item)[0].replace("[", "").replace("]", "").split("<")[0]
                time = re.findall(findTime, item)[0]
                print("正在爬取第{}页的第{}个微博信息".format(page, cnt))
                itemData.append(content)  # 文章内容
                itemData.append(commentURL)  # 评论链接
                itemData.append(commentNUm)  # 评论数
                itemData.append(approveNum)  # 点赞数
                itemData.append(transNum)  # 转发数
                itemData.append(time)  # 发布时间
                print("第{}页的第{}个微博信息爬取完毕，当前itemData的长度为{}".format(page, cnt, len(itemData)))
                cnt = cnt + 1
                dataList.append(itemData)
    saveData(dataList)


def saveData(dataList):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    # itemData.append(content)  # 文章内容
    # itemData.append(commentURL)  # 评论链接
    # itemData.append(commentNUm)  # 评论数
    # itemData.append(approveNum)  # 点赞数
    # itemData.append(transNum)  # 转发数
    # itemData.append(time)  # 发布时间
    for item in range(len(dataList)):
        itemData = dataList[item]
        if(itemData[2].isnumeric() and itemData[3].isnumeric() and itemData[4].isnumeric()):  # 判断是否只有数字组成，把不符合规则的过滤掉
            try:
                worksheet.write(item,0,itemData[0])
                worksheet.write(item,1,itemData[1])
                worksheet.write(item,2,itemData[2])
                worksheet.write(item,3,itemData[3])
                worksheet.write(item,4,itemData[4])
                worksheet.write(item,5,itemData[5])
            except:
                print("错误！item的长度为{}".format(len(itemData)))
    workbook.save("微博id：健康中国.xls")


if __name__ == '__main__':
    main()

