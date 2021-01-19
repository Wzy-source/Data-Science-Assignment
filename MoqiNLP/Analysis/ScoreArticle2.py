import MoqiNLP.SeparateWords.SeparateWords as SeparateWords

'''加有权重，否定词，程度词的词语情感分析'''
'''基础满分10分，程度词最高可乘2，否定词直接变号'''
'''最终有效数据3000条左右，结果存在score2中'''

#获取表格的数据，主结构是列表，列表里的每个元素是字典
def getDataList(table1):
    dataList = []
    for i in range(0, table1.nrows):
        perRowsDataDict = {'词语': table1.cell_value(i, 0), '词性种类': table1.cell_value(i, 1),
                           '词义数': table1.cell_value(i, 2), '词义序号': table1.cell_value(i, 3),
                           '情感分类': table1.cell_value(i, 4), '强度': table1.cell_value(i, 5),
                           '极性': table1.cell_value(i, 6)}
        dataList.append(perRowsDataDict)
    return dataList


# 计算每个情感词的基础分
def transform(dic):
    if (int(dic.get('极性')) == 0 or int(dic.get('极性')) == 3):
        return 0.0
    score = (dic.get('强度') + 1)
    if int(dic.get('极性')) == 2:
        return -1 * score
    return score


if __name__ == '__main__':
    #将所有词库转换成列表备用
    dataList = getDataList(SeparateWords.getDataTable('..\WordsRepos\EmotionWords\情感词汇本体.xlsx'))
    emotionWordList = []
    for dic in dataList:
        emotionWordList.append(dic.get('词语'))
    degreeWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\all.txt')
    inverseWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\inverse.txt')
    ishWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\ish1.txt')
    moreWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\more2.txt')
    mostWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\most4.txt')
    veryWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\very3.txt')

    '''主要流程：对每篇文章的分词结果进行操作，寻找情感词，并寻找情感词前面是否有修饰词、否定词等，并根据内容进行打分
    另外，每个情感词根据情感强烈程度也有一定的分值，称为基础分。最后将文章中所有情感词分数求平均值，得到最终分数。
    对于文章中情感词少于5的，我们认为样本太少，数据无效（这个数字不能再大了，5就已经筛出1700条无效数据了）
    未来如果有时间，可以考虑使用一个更加科学的方法对情感词分数进行处理（不用均值判分），得到更加合理的结果'''
    result = []
    f = open('score2.txt', 'w+')
    articlenum = 1
    for article in SeparateWords.listOfDealedContent:
        score = 0
        count = 0
        print('——————第' + str(articlenum) + '篇文章——————')
        articlenum = articlenum + 1
        for i in range(0, len(article)):
            for j in range(0, len(dataList)):
                if article[i] == dataList[j].get('词语'):
                    scoreTmp = transform(dataList[j])
                    k = i
                    while (k > 0):
                        k = k - 1
                        if article[k] in emotionWordList:
                            break
                        if article[k] in degreeWordList:
                            if article[k] in inverseWordList:
                                scoreTmp = -scoreTmp
                                print('存在否定词')
                                continue
                            if article[k] in ishWordList:
                                scoreTmp = 0.8 * scoreTmp
                                print('存在轻微修饰词')
                                continue
                            if article[k] in moreWordList:
                                scoreTmp = 1.2 * scoreTmp
                                print('存在更修饰词')
                                continue
                            if article[k] in mostWordList:
                                scoreTmp = 2 * scoreTmp
                                print('存在最修饰词')
                                continue
                            if article[k] in veryWordList:
                                scoreTmp = 1.5 * scoreTmp
                                print('存在非常修饰词')
                                continue
                        if (k == i - 3):
                            break
                    score = score * count + scoreTmp
                    if scoreTmp != 0:
                        count = count + 1
                    if count != 0:
                        score = score / count
        if count > 5:
            result.append(score)
            print('得分:' + str(score))
            f.write(str(score) + '\n')
        else:
            result.append(-99)
            print('无效')
            f.write('无效\n')
    f.close()
