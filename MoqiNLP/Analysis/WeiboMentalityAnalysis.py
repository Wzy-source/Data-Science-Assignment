import MoqiNLP.Analysis.DealWeiboData as WeiboData
import MoqiNLP.SeparateWords.SeparateWords as SeparateWords
import jieba

#��ȡ�������ݣ����ṹ���б��б����ÿ��Ԫ�����ֵ�
def getDataList(table1):
    dataList = []
    for i in range(0, table1.nrows):
        perRowsDataDict = {'����': table1.cell_value(i, 0), '��������': table1.cell_value(i, 1),
                           '������': table1.cell_value(i, 2), '�������': table1.cell_value(i, 3),
                           '��з���': table1.cell_value(i, 4), 'ǿ��': table1.cell_value(i, 5),
                           '����': table1.cell_value(i, 6)}
        dataList.append(perRowsDataDict)
    return dataList

# ����ÿ����дʵĻ�����
#def transform(dic):


stopWordList = SeparateWords.createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
def cutWords(commit):
    seg_list=jieba.cut(commit)
    outstr = []
    for word in seg_list:
        if word not in stopWordList or word in degreeWordsList:
            if word != '\t' and word != ' ' and (not word.isdigit()):
                outstr.append(word)
    return outstr


dataList = getDataList(SeparateWords.getDataTable('..\WordsRepos\EmotionWords\��дʻ㱾��.xlsx'))
emotionWordList = []
for dic in dataList:
    emotionWordList.append(dic.get('����'))
degreeWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\all.txt')
inverseWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\inverse.txt')
ishWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\ish1.txt')
moreWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\more2.txt')
mostWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\most4.txt')
veryWordList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\very3.txt')
stopWordList= SeparateWords.createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
degreeWordsList=SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\all.txt')
for k in range(7,8):
    weiboDataList = WeiboData.getDataList(k)
    f = open('..\ResultData\WeiboScore'+str(k)+'.txt', 'w+')
    result=[]
    tmp=[]
    for singleWeibo in weiboDataList:
        for commit in singleWeibo:
            score = 0
            count = 0
            wordList=cutWords(commit)
            for i in range(0, len(wordList)):
                for j in range(0, len(dataList)):
                    if wordList[i] == dataList[j].get('����'):
                        scoreTmp = transform(dataList[j])
                        k = i
                        while (k > 0):
                            k = k - 1
                            if wordList[k] in emotionWordList:
                                break
                            if wordList[k] in degreeWordList:
                                if wordList[k] in inverseWordList:
                                    scoreTmp = -scoreTmp
                                    print('���ڷ񶨴�')
                                    continue
                                if wordList[k] in ishWordList:
                                    scoreTmp = 0.8 * scoreTmp
                                    print('������΢���δ�')
                                    continue
                                if wordList[k] in moreWordList:
                                    scoreTmp = 1.2 * scoreTmp
                                    print('���ڸ����δ�')
                                    continue
                                if wordList[k] in mostWordList:
                                    scoreTmp = 2 * scoreTmp
                                    print('���������δ�')
                                    continue
                                if wordList[k] in veryWordList:
                                    scoreTmp = 1.5 * scoreTmp
                                    print('���ڷǳ����δ�')
                                    continue
                            if k == i - 3:
                                break
                        score = score * count + scoreTmp
                        if scoreTmp != 0:
                            count = count + 1
                        if count != 0:
                            score = score / count
            if count > 0:
                result.append(score)
                print('�÷�:' + str(score))
                f.write(str(score) + '\n')
            else:
                result.append(-99)
                print('��Ч')
                f.write('��Ч\n')
        f.write('����������������΢���ָ��ߡ���������������\n')
        print('����������������΢���ָ��ߡ���������������')