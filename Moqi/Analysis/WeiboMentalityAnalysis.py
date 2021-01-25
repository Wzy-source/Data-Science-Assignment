import Moqi.Analysis.DealWeiboData as WeiboData
import Moqi.SeparateWords.SeparateWords as SeparateWords
import jieba

'''心态词典映射'''
# 获取表格的数据，主结构是列表，列表里的每个元素是字典
def getDataList(table1):
    dataList = []
    for i in range(0, table1.nrows):
        perRowsDataDict = {'词语': table1.cell_value(i, 0), '词性种类': table1.cell_value(i, 1),
                           '词义数': table1.cell_value(i, 2), '词义序号': table1.cell_value(i, 3),
                           '情感分类': table1.cell_value(i, 4), '强度': table1.cell_value(i, 5),
                           '极性': table1.cell_value(i, 6)}
        dataList.append(perRowsDataDict)
    return dataList


mapList = ['快乐', '安心', '尊敬', '赞扬', '相信', '喜爱', '祝愿', '愤怒', '悲伤', '失望', '内疚', '思念', '慌张', '恐惧', '羞臊'
    , '烦闷', '憎恶', '贬责', '妒忌', '怀疑', '惊奇']


def transform(dic):
    tmp = dic.get('情感分类')
    if tmp == 'PA':
        return 0
    if tmp == 'PE':
        return 1
    if tmp == 'PD':
        return 2
    if tmp == 'PH':
        return 3
    if tmp == 'PG':
        return 4
    if tmp == 'PB':
        return 5
    if tmp == 'PK':
        return 6
    if tmp == 'NA':
        return 7
    if tmp == 'NB':
        return 8
    if tmp == 'NJ':
        return 9
    if tmp == 'NH':
        return 10
    if tmp == 'PF':
        return 11
    if tmp == 'NI':
        return 12
    if tmp == 'NC':
        return 13
    if tmp == 'NG':
        return 14
    if tmp == 'NE':
        return 15
    if tmp == 'ND':
        return 16
    if tmp == 'NN':
        return 17
    if tmp == 'NK':
        return 18
    if tmp == 'NL':
        return 19
    if tmp == 'PC':
        return 20


stopWordList = SeparateWords.createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')


def cutWords(commit):
    seg_list = jieba.cut(commit)
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
stopWordList = SeparateWords.createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
degreeWordsList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\all.txt')
for k in range(1, 8):
    weiboDataList = WeiboData.getDataList(k)
    f = open('..\ResultData\WeiboMentality' + str(k) + '.txt', 'w+')
    result = []

    for singleWeibo in weiboDataList:
        for commit in singleWeibo:
            tmp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            count = 0
            wordList = cutWords(commit)
            for i in range(0, len(wordList)):
                for j in range(0, len(dataList)):
                    if wordList[i] == dataList[j].get('词语'):
                        index = transform(dataList[j])
                        tmp[index] = tmp[index] + 1
                        count = count + 1
                        k = i
                        while k > 0:
                            k = k - 1
                            if wordList[k] in emotionWordList:
                                break
                            if wordList[k] in degreeWordList:
                                if wordList[k] in inverseWordList:
                                    tmp[index] = tmp[index] - 1
                                    print('存在否定词')
                                    count = count - 1
                                    continue
            if count > 0:
                maxTmp = max(tmp)
                indexMax = tmp.index(maxTmp)
                print(mapList[indexMax])
                f.write(mapList[indexMax] + '\n')
            else:
                result.append(-99)
                print('无效')
                f.write('无效\n')
        f.write('————————微博分割线————————\n')
        print('————————微博分割线————————')

