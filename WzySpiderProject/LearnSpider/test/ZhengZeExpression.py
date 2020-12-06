# 正则表达式：字符串模式：判断字符串是否符合一定的标准

import re

# 创建模式对象
pat = re.compile("AA")  # 此处的AA是正则表达式，
# search方法进行比对查找
pat.search("CBA")  # arg：被校验的内容
# 没有模式对象
m = re.search("asd","Aasd") # 前面的字符串是模板，后面的字符串是被校验的对象
print(m)



p = re.findall("[A-Z]+Das","ASDasDFGaGHJa")  # 前面的字符串是规则，后面的字符擦混是被校验的字符串
# 返回所有符合条件的字符串,放到列表中
print(p)



# sub用于替换
print(re.sub("a","A","asdfgh")) # 在第三个字符串中找到小a，用A来替换
#类似的思路：把换行替换为一行


# 建议再正则表达式中，被比较的字符串前面加上r，不用担心转义字符的问题
a= r"\asd"



