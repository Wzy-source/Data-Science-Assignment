import Moqi.SeparateWords.SeparateWords as SeparateWords
'''简单测试一下词典，所得结果score1仅仅与词频有关,并未加有权重等'''

def getDataList(table1):
    # dataList为处理好的表格内容，以后方面使用，主结构为列表，每个元素为字典，每个字典存一行的标题等
    dataList = []
    for i in range(0, table1.nrows):
        perRowsDataDict = {'词语': table1.cell_value(i, 0), '词性种类': table1.cell_value(i, 1),
                           '词义数': table1.cell_value(i, 2), '词义序号': table1.cell_value(i, 3),
                           '情感分类': table1.cell_value(i, 4), '强度': table1.cell_value(i, 5),
                           '极性': table1.cell_value(i, 6)}
        dataList.append(perRowsDataDict)
    return dataList


def transform(i):
    if i == 0 or i == 3:
        return 0.01
    if i == 1:
        return 10
    if i == 2:
        return -10


if __name__ == '__main__':
    dataList = getDataList(SeparateWords.getDataTable('..\WordsRepos\EmotionWords\情感词汇本体.xlsx'))
    result = []
    f = open('score1.txt', 'w+')
    for article in SeparateWords.listOfDealedContent:
        score = 0
        count = 0
        for word in article:
            for i in range(0, len(dataList)):
                if word == dataList[i].get('词语'):
                    score = (score * count + transform(dataList[i].get('极性'))) / (count + 1)
                    count = count + 1
        if count > 5:
            result.append(score)
            print(score)
            f.write(str(score) + '\n')
        else:
            result.append(-99)
            print('无效')
            f.write('无效\n')
    f.close()
