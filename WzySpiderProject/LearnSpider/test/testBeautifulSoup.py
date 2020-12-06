# 对BeautifulSoup的理解

'''
- tag
- BeautifulSoup
- Comment
-
'''
import re

from bs4 import BeautifulSoup

file = open("./baidu.html", "rb")
html = file.read()  # 读出一个html文件，生成一个对象
bs = BeautifulSoup(html, "html.parser")  # 使用BeautifulSoup中的html.parser来解析该html文件
# print(type(bs))
# print(bs.name)
# print(bs.attrs)
# print("1"+"---" * 15)
# print(bs.a)  # 找到第一个标签及其内容拿出来，注意是标签和内容同时大眼，并且只打印第一个
# print(type(bs.a))
# print("2"+"---" * 15)
# print(bs.a.string)  # 找到第一个a标签其内容,但只是将内容拿出来，而不拿出标签
# print(type(bs.a.string))  # a 的类型是注释（Comment），是一个特殊的string
# print("3"+"---" * 15)
# print(bs.a.attrs) # 找到第一个a的属性，将其以字典的方式呈现

# 文档的查询
# print(bs.head.contents)  # 返回的是一个列表
# print("---" * 35)
# print(bs.head.contents[1])  # 返回的是一个列表某一个元素
# print("---" * 35)
# 文档的搜索（定位想要的内容）
# 字符串过滤，查找与字符串完全匹配的内容
t_list = bs.find_all("a")  # 查找所有的名字为"a"的标签（一定是标签！）
print(t_list)
# print("---" * 35)
f_list = bs.find_all(re.compile("a"))  # re.compile("a")编译一个正则表达式对象
print(f_list)  # 查找所有的名字里面含有"a"的标签（一定是标签！）（标签含有a，而不是标签是a）
# 传入一个函数来搜索，根据函数的要求来搜索


# kwards 参数 ，指定参数来进行搜索
# id 参数
g_list = bs.find_all(id="head")  # 指定参数来进行搜索
for i in g_list:
    print(i)

# text参数
h_list = bs.find_all(text=re.compile("\d"))  # 应用正则表达式来查找包含特定的文本内容（标签里的字符串）

for i in h_list:
    print(i)

# limit参数

k_list = bs.find_all("a", limit=3)  # 限定直接获取多少个

# class参数

p_list = bs.find_all(class_ = True)

# css选择器

print(bs.select('tittle'))