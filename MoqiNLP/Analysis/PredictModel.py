import nltk
import jieba
import xlrd
import MoqiNLP.SeparateWords.SeparateWords as SeparateWords
from random import shuffle
import joblib

stopwordslist = SeparateWords.createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
degreeWordsList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\all.txt')


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


pos_review = dealData('..\WordsRepos\\EmotionWords\\positive.xls')+dealData('..\WordsRepos\\EmotionWords\\positive.xls')
neg_review = dealData('..\WordsRepos\\EmotionWords\\negative.xls')+dealData('..\WordsRepos\\EmotionWords\\negative.xls')
pos_review=pos_review[0:40000]
neg_review=neg_review[0:32000]

def jieba_feature(number):
    posWords = []
    negWords = []

    for items in pos_review:  # 把集合的集合变成集合
        for item in items:
            posWords.append(item)

    for items in neg_review:
        for item in items:
            negWords.append(item)

    word_fd = nltk.FreqDist()  # 可统计所有词的词频

    cond_word_fd = nltk.ConditionalFreqDist()  # 可统计积极文本中的词频和消极文本中的词频

    for word in posWords:
        word_fd[word] += 1

        cond_word_fd['pos'][word] += 1

    for word in negWords:
        word_fd[word] += 1

        cond_word_fd['neg'][word] += 1

    pos_word_count = cond_word_fd['pos'].N()  # 积极词的数量

    neg_word_count = cond_word_fd['neg'].N()  # 消极词的数量

    total_word_count = pos_word_count + neg_word_count

    word_scores = {}  # 包括了每个词和这个词的信息量

    for word, freq in word_fd.items():
        pos_score = nltk.BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count),
                                                    total_word_count)  # 计算积极词的卡方统计量，这里也可以计算互信息等其它统计量

        neg_score = nltk.BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count),
                                                    total_word_count)  # 同理

        word_scores[word] = pos_score + neg_score  # 一个词的信息量等于积极卡方统计量加上消极卡方统计量

    best_vals = sorted(word_scores.items(), key=lambda item: item[1], reverse=True)[
                :number]  # 把词按信息量倒序排序。number是特征的维度，是可以不断调整直至最优的

    best_words = set([w for w, s in best_vals])

    return dict([(word, True) for word in best_words])


def build_features():
    feature = jieba_feature(300)  # 结巴分词
    posFeatures = []

    for items in pos_review:

        a = {}

        for item in items:

            if item in feature.keys():
                a[item] = 'True'

        posWords = [a, 'pos']  # 为积极文本赋予"pos"

        posFeatures.append(posWords)

    negFeatures = []

    for items in neg_review:

        a = {}

        for item in items:

            if item in feature.keys():
                a[item] = 'True'

        negWords = [a, 'neg']  # 为消极文本赋予"neg"

        negFeatures.append(negWords)

    return posFeatures, negFeatures


posFeatures, negFeatures = build_features()  # 获得训练数据

shuffle(posFeatures)  # 把文本的排列随机化

shuffle(negFeatures)  # 把文本的排列随机化

train = posFeatures[1000:] + negFeatures[1000:]  # 训练集(80%)

test = posFeatures[:1000] + negFeatures[:1000]  # 预测集(验证集)(20%)

data, tag = zip(*test)  # 分离测试集合的数据和标签，便于验证和测试


def score(classifier):
    classifier = nltk.SklearnClassifier(classifier)  # 在nltk中使用scikit-learn的接口

    classifier.train(train)  # 训练分类器
    joblib.dump(classifier,'LogisticRegression.model')
    pred = classifier.classify_many(data)  # 对测试集的数据进行分类，给出预测的标签

    n = 0

    s = len(pred)

    for i in range(0, s):

        if pred[i] == tag[i]:
            n = n + 1

    return n / s  # 对比分类预测结果和人工标注的正确结果，给出分类器准确度


import sklearn

from nltk.classify.scikitlearn import SklearnClassifier

from sklearn.svm import SVC, LinearSVC, NuSVC

from sklearn.naive_bayes import MultinomialNB, BernoulliNB

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score

#print('BernoulliNB`s accuracy is %f' % score(BernoulliNB()))

#print('MultinomiaNB`s accuracy is %f' % score(MultinomialNB()))

print('LogisticRegression`s accuracy is  %f' % score(LogisticRegression()))

#print('SVC`s accuracy is %f' % score(SVC()))

#print('LinearSVC`s accuracy is %f' % score(LinearSVC()))

#print('NuSVC`s accuracy is %f' % score(NuSVC()))
