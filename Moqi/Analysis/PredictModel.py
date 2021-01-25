import nltk
import jieba
import xlrd
import Moqi.SeparateWords.SeparateWords as SeparateWords
from random import shuffle
import joblib
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression

'''机器学习部分，代码参考
https://blog.csdn.net/qq_38233659/article/details/91963866?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-3.control
'''
stopwordslist = SeparateWords.createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
degreeWordsList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\all.txt')


# 处理数据
def dealData(path):
    dataTables = xlrd.open_workbook(path)
    listOfTableName = dataTables.sheet_names()
    table1 = dataTables.sheet_by_name(listOfTableName[0])
    pos_review = []
    listOfContent = []
    for i in range(0, table1.nrows):
        listOfContent.append(str(table1.cell_value(i, 0)))

    for contentOfPerArticle in listOfContent:
        seg_list = jieba.cut(contentOfPerArticle)
        outstr = []
        for word in seg_list:
            if word not in stopwordslist or word in degreeWordsList:
                if word != '\t' and word != ' ' and (not word.isdigit()):
                    outstr.append(word)
        pos_review.append(outstr)
    return pos_review


# 初始数据
posReview = dealData('..\WordsRepos\\EmotionWords\\positive.xls') + dealData(
    '..\WordsRepos\\EmotionWords\\positive.xls')
negReview = dealData('..\WordsRepos\\EmotionWords\\negative.xls') + dealData(
    '..\WordsRepos\\EmotionWords\\negative.xls')
posReview = posReview[0:40000]
negReview = negReview[0:32000]


# 将数据特征化
def buildFeatures():
    posWords = []
    negWords = []

    for items in posReview:
        for item in items:
            posWords.append(item)

    for items in negReview:
        for item in items:
            negWords.append(item)

    wordFd = nltk.FreqDist()
    condWordFd = nltk.ConditionalFreqDist()
    # 数词频
    for word in posWords:
        wordFd[word] += 1
        condWordFd['pos'][word] += 1

    for word in negWords:
        wordFd[word] += 1
        condWordFd['neg'][word] += 1

    posWordCount = condWordFd['pos'].N()
    negWordCount = condWordFd['neg'].N()
    totalWordCount = posWordCount + negWordCount
    wordScores = {}

    # 计算每个词的卡方量
    for word, freq in wordFd.items():
        posScore = nltk.BigramAssocMeasures.chi_sq(condWordFd['pos'][word], (freq, posWordCount),
                                                   totalWordCount)
        negScore = nltk.BigramAssocMeasures.chi_sq(condWordFd['neg'][word], (freq, negWordCount),
                                                   totalWordCount)
        wordScores[word] = posScore + negScore

    bestVals = sorted(wordScores.items(), key=lambda item: item[1], reverse=True)[:2000]
    bestWords = set([w for w, s in bestVals])
    feature = dict([(word, True) for word in bestWords])
    posFeatures = []

    # 改为可以用于训练的格式
    for items in posReview:
        a = {}
        for item in items:
            if item in feature.keys():
                a[item] = 'True'
        posWords = [a, 'pos']
        posFeatures.append(posWords)
    negFeatures = []
    for items in negReview:
        a = {}
        for item in items:
            if item in feature.keys():
                a[item] = 'True'
        negWords = [a, 'neg']
        negFeatures.append(negWords)
    return posFeatures, negFeatures


posFeatures, negFeatures = buildFeatures()

shuffle(posFeatures)

shuffle(negFeatures)

train = posFeatures[1000:] + negFeatures[1000:]

test = posFeatures[:1000] + negFeatures[:1000]

data, tag = zip(*test)


def score(classifier):

    classifier = nltk.SklearnClassifier(classifier)
    classifier.train(train)
    joblib.dump(classifier, 'LogisticRegression.model')
    pred = classifier.classify_many(data)
    n = 0
    s = len(pred)
    for i in range(0, s):
        if pred[i] == tag[i]:
            n = n + 1
    return n / s


# print('accuracy is %f' % score(BernoulliNB()))

print('accuracy is  %f' % score(LogisticRegression()))
