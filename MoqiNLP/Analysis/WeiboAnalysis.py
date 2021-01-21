import MoqiNLP.Analysis.DealWeiboData as WeiboData
import MoqiNLP.SeparateWords.SeparateWords as SeparateWords
import jieba

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

stopWordList = SeparateWords.createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
def cutWords(commit):
    seg_list=jieba.cut(commit)
    outstr = []
    for word in seg_list:
        if word not in stopWordList or word in degreeWordsList:
            if word != '\t' and word != ' ' and (not word.isdigit()):
                outstr.append(word)
    return outstr


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
stopWordList= SeparateWords.createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
degreeWordsList=SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\all.txt')
for k in range(3,4):
    weiboDataList = WeiboData.getDataList(k)
    f = open('WeiboScore'+str(k)+'.txt', 'w+')
    result=[]
    tmp=[]
    for singleWeibo in weiboDataList:
        for commit in singleWeibo:
            score = 0
            count = 0
            wordList=cutWords(commit)
            for i in range(0, len(wordList)):
                for j in range(0, len(dataList)):
                    if wordList[i] == dataList[j].get('词语'):
                        scoreTmp = transform(dataList[j])
                        k = i
                        while (k > 0):
                            k = k - 1
                            if wordList[k] in emotionWordList:
                                break
                            if wordList[k] in degreeWordList:
                                if wordList[k] in inverseWordList:
                                    scoreTmp = -scoreTmp
                                    print('存在否定词')
                                    continue
                                if wordList[k] in ishWordList:
                                    scoreTmp = 0.8 * scoreTmp
                                    print('存在轻微修饰词')
                                    continue
                                if wordList[k] in moreWordList:
                                    scoreTmp = 1.2 * scoreTmp
                                    print('存在更修饰词')
                                    continue
                                if wordList[k] in mostWordList:
                                    scoreTmp = 2 * scoreTmp
                                    print('存在最修饰词')
                                    continue
                                if wordList[k] in veryWordList:
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
            if count > 0:
                result.append(score)
                print('得分:' + str(score))
                f.write(str(score) + '\n')
            else:
                result.append(-99)
                print('无效')
                f.write('无效\n')
        f.write('————————微博分割线————————\n')
        print('————————微博分割线————————')