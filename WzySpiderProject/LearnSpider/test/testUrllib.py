import urllib.request

# 获取一个get请求
# response = urllib.request.urlopen("https://www.baidu.com/")  # response对象
# print(response)
# print(response.read())  # 读取对象内容
# print(response.read().decode('utf-8'))  # 读取对象内容，并进行utf-8的解码


# response = urllib.request.urlopen("https://www.baidu.com/")
# print(response.status) # 返回200状态码
# 如果返回的是418，说明对方已经发现了自己是爬虫了

# 如果要伪装成浏览器，还需要伪装信息，即浏览器参数
#url = "https://movie.douban.com"
# request = urllib.request.Request(url=url,data=data,headers=header,method="POST")


# 超时处理
# try:
#     response = urllib.request.urlopen("https://www.baidu.com/",timeout=0.01)
#     print(response.read().decode('utf-8'))
# except:
#     print('time out')


# response = urllib.request.urlopen("http://www.baidu.com")
#  print(response.status)
# print(response.getheader("Server"))




#如何伪装？：往header中加内容
url = "https://www.douban.com"
headers = {
    "User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
}
data = bytes(urllib.parse.urlencode({"name":"eric"}),encoding="utf-8")
#封装请求对象
req = urllib.request.Request(url=url,headers=headers)

#获取相应
response = urllib.request.urlopen(req)
print(response.read().decode("utf-8"))


