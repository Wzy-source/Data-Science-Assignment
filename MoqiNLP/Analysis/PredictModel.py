import nltk
import jieba
import xlrd
import MoqiNLP.SeparateWords.SeparateWords as SeparateWords
from random import shuffle
import joblib
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression

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


pos_review = dealData('..\WordsRepos\\EmotionWords\\positive.xls') + dealData(
    '..\WordsRepos\\EmotionWords\\positive.xls')
neg_review = dealData('..\WordsRepos\\EmotionWords\\negative.xls') + dealData(
    '..\WordsRepos\\EmotionWords\\negative.xls')
pos_review = pos_review[0:40000]
neg_review = neg_review[0:32000]


def build_features():
    posWords = []
    negWords = []

    for items in pos_review:
        for item in items:
            posWords.append(item)

    for items in neg_review:
        for item in items:
            negWords.append(item)

    word_fd = nltk.FreqDist()
    cond_word_fd = nltk.ConditionalFreqDist()

    for word in posWords:
        word_fd[word] += 1
        cond_word_fd['pos'][word] += 1

    for word in negWords:
        word_fd[word] += 1
        cond_word_fd['neg'][word] += 1

    pos_word_count = cond_word_fd['pos'].N()
    neg_word_count = cond_word_fd['neg'].N()
    total_word_count = pos_word_count + neg_word_count
    word_scores = {}

    for word, freq in word_fd.items():
        pos_score = nltk.BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count),
                                                    total_word_count)
        neg_score = nltk.BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count),
                                                    total_word_count)
        word_scores[word] = pos_score + neg_score

    best_vals = sorted(word_scores.items(), key=lambda item: item[1], reverse=True)[:2000]
    best_words = set([w for w, s in best_vals])
    feature = dict([(word, True) for word in best_words])
    posFeatures = []

    for items in pos_review:
        a = {}
        for item in items:
            if item in feature.keys():
                a[item] = 'True'
        posWords = [a, 'pos']
        posFeatures.append(posWords)
    negFeatures = []
    for items in neg_review:
        a = {}
        for item in items:
            if item in feature.keys():
                a[item] = 'True'
        negWords = [a, 'neg']
        negFeatures.append(negWords)
    return posFeatures, negFeatures


posFeatures, negFeatures = build_features()

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


#print('accuracy is %f' % score(BernoulliNB()))

print('accuracy is  %f' % score(LogisticRegression()))
