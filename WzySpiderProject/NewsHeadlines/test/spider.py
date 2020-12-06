import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 网页源码的获取
from bs4 import BeautifulSoup
import xlwt

# find 的部分
findTittle = re.compile(r' target="_blank">(.*?)</a>')
findTime = re.compile(r'</a> (.*?)<br/>')


#
def main():
    baseURL = "http://opinion.people.com.cn/GB/8213/49160/49219/index"
    getData(baseURL)


def getData(baseURL):
    dataList = []
    for i in range(0, 8):
        url = baseURL + str(i + 1) + ".html"
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all(class_="abl"):

            data = []
            item = str(item)

            tittle = re.findall(findTittle, item)
            if (len(tittle) == 1):
                data.append(tittle[0])

            # time = re.findall(findTime, item)
            # if (len(time) == 1):
            #     data.append(time[0])
            dataList.append(data)

    saveData(dataList)


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    req = urllib.request.Request(url=url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("GB2312", "ignore")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print("code出错")
        if hasattr(e, "reason"):
            print("reason出错")

    return html


def saveData(dataList):
    print(len(dataList))
    workbook = xlwt.Workbook(encoding='GB2312')
    worksheet = workbook.add_sheet('sheet1')
    col = ("文章名称", "发布时间",)
    for i in range(0, 2):
        worksheet.write(0, i, col[i])
    for i in range(0, 357):
        data = dataList[i]
        worksheet.write(i+1, 0, data[0])
        # worksheet.write(i, 1, data[1])
    workbook.save("人名日报时评.xls")


if __name__ == '__main__':
    main()
