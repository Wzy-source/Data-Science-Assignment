import xlwt
def getIndex(key):
    index = 0
    list = ['乐','好','怒','哀','惧','恶','惊']
    for i in range(len(list)):
        if(key==list[i]):
            index = i
            break
    return index

dic = {
    '快乐': '乐',
    '安心': '乐',
    '尊敬': '好',
    '赞扬': '好',
    '相信': '好',
    '喜爱': '好',
    '祝愿': '好',
    '愤怒': '怒',
    '悲伤': '哀',
    '失望': '哀',
    '内疚': '哀',
    '思念': '哀',
    '慌张': '惧',
    '恐惧': '惧',
    '羞臊': '惧',
    '烦闷' :'恶',
    '憎恶' :'恶',
    '贬责' :'恶',
    '妒忌' :'恶',
    '怀疑' :'恶',
    '惊奇' :'惊'
}
with open('/Users/mac/PycharmProjects/BigHomework/Data Science Assignment/Moqi/ResultData/WeiboMentalityAll.txt',
          'r', encoding='utf-8') as f:
    text = f.read()
dataList = text.split()

totalData = []
monthData = []
for item in dataList:
    if (len(item) > 2):
        totalData.append(monthData)
        monthData = []
    else:
        monthData.append(dic[item])
totalData = totalData[1:]
p = 0
totalDataList = []
for item in totalData:
    monthDic = {}
    for i in item:
        if (i not in monthDic):
            monthDic[i] = 1
        else:
            monthDic[i] = monthDic[i] + 1
    totalDataList.append(monthDic)

book = xlwt.Workbook(encoding="utf-8")
sheet = book.add_sheet('sheet')  # 创建工作表
lineNum = 0
monthNum = 12



for item in totalDataList:  # item是字典
    sheet.write(lineNum, 0, monthNum)
    lineNum = lineNum + 1
    monthNum = monthNum - 1
    for key, value in item.items():
        sheet.write(lineNum, getIndex(key), key)
        sheet.write(lineNum + 1, getIndex(key), value)
    lineNum = lineNum + 4
book.save("心态词典数据.xls")
