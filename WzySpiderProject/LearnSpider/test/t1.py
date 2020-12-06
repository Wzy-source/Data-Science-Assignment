import xlwt  # 进行excel操作
import bs4  # 进行网页解析，获取数据
import sqlite3  # 进行SQLite数据库操作
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup

# 爬取网页
# 逐一解析数据
# 保存数据


findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式的对象，表示规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.s:忽略这里面的换行符
findTittle = re.compile(r'<span class="tittle">(.*?)</span>')
findRat = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(,*?)</span>')
findBD = re.compile(r'<p class="">(.*?)</p>', re.S)


def main():
    baseUrl = "https://movie.douban.com/top250?start="
    getData(baseUrl)


# 爬取网页
def getData(baseUrl):
    dataList = []
    # 逐一解析数据
    for i in range(0, 1):
        url = baseUrl + str(i * 25)  # 调用获取页面的函数10次，获取250条数据
        html = askURL(url)
        # 对网页源码逐一进行解析
        soup = BeautifulSoup(html, "html.parser")  # 形成一个树形结构的对象
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)
            link = re.findall(findLink, item)[0]
            data.append(link)
            imgSRC = re.findall(findImgSrc,item)[0]
            data.append(imgSRC)
            tittle = re.findall(findTittle,item)
            # if(len(tittle)==2):
            #     ctittle = tittle[0]
            #     data.append(ctittle)
            #     otittle = tittle[1].replace("/","")
            #     data.append(otittle)  #添加中文名和外文名
            # else:
            #     data.append(tittle[0])
            #     data.append(" ")   # 外文名留空

            rating = re.findall(findRat,item)[0]
            data.append(rating)

            judge = re.findall(findJudge,item)[0]
            data.append(judge)

            # inq = re.findall(findInq,item)[0]
            # if len(inq) != 0:
            #     inq = inq.replace("。","")
            #     data.append(inq)
            # else:
            #     data.append(" ")
            #
            # dataList.append(data)

    print(dataList)






# 得到指定一个URL网页的内容
def askURL(url):
    # 表示告诉豆服务器我们是什么样的机器（本质上是告诉浏览器我可以接受什么样的文件内容）
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    req = urllib.request.Request(url=url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# 保存数据
def savaData(savaPath):
    print("1")


if __name__ == '__main__':
    main()
