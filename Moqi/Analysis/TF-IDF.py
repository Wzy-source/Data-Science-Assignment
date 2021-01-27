import math
import operator

import xlrd
import jieba
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')         #改变标准输出的默认编码


def createwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


stopwordslist = createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
degreeWordsList = createwordslist('..\WordsRepos\DegreeWords\\all.txt')


def dealData(path):
    dataTables = xlrd.open_workbook(path, encoding_override='utf-8')
    listOfTableName = dataTables.sheet_names()
    table1 = dataTables.sheet_by_name(listOfTableName[0])
    dataList = []
    listOfContent = []
    for i in range(1, table1.nrows):
        for j in range(6, 6 + int(table1.cell_value(i, 5))):
            listOfContent.append(str(table1.cell_value(i, j)))

    for contentOfPerArticle in listOfContent:
        seg_list = jieba.cut(contentOfPerArticle)
        outStr = []
        for word in seg_list:
            if word not in stopwordslist or word in degreeWordsList:
                if word != '\t' and word != ' ' and (not word.isdigit()):
                    outStr.append(word)
        dataList.append(outStr)
    return dataList


dataList = []
for i in range(1, 8):
    dataList = dataList + dealData('..\..\WzySpiderProject\WeiboSpider\\微博id：健康中国(热门含评论)' + str(i) + '.xls')
dataTmp = []
for items in dataList:
    for item in items:
        dataTmp.append(item)
allWords = set(dataTmp)


def idf(corpus):
    idfs = {}
    d = 0.0
    # 统计词出现次数
    for doc in corpus:
        d += 1
        counted = []
        for word in doc:
            if not word in counted:
                counted.append(word)
                if word in idfs:
                    idfs[word] += 1
                else:
                    idfs[word] = 1

    # 计算每个词逆文档值
    for word in idfs:
        idfs[word] = math.log(d / (1 + float(idfs[word])))

    return idfs


f = open('..\\ResultData\\TF-IDF.txt', 'w+', encoding='utf-8')
idfs = idf(dataList)
for doc in dataList:
    tfs = []
    tfidfs = {}
    for word in doc:
        if word in tfs:
            tfidfs[word] += 1
        else:
            tfidfs[word] = 1
            tfs.append(word)
    for word in tfidfs:
        tfidfs[word] *= idfs[word]
    swd = sorted(tfidfs.items(), key=operator.itemgetter(1), reverse=True)
    if len(swd) < 5:
        f.write('无效\n')
        print('无效')
    else:
        f.write(str(swd[0][0]) + ' ' + str(swd[1][0]) + ' ' + str(swd[2][0]) + '\n')
        print(str(swd[0][0]) + ' ' + str(swd[1][0]) + ' ' + str(swd[2][0]))
