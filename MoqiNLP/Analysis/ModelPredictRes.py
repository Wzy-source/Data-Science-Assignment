import nltk
import xlrd
import MoqiNLP.SeparateWords.SeparateWords as SeparateWords
import jieba
import joblib
import MoqiNLP.Analysis.DealWeiboData as WeiboData

stopwordslist = SeparateWords.createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
degreeWordsList = SeparateWords.createwordslist('..\WordsRepos\DegreeWords\\all.txt')
classifier = joblib.load('LogisticRegression.model')

for k in range(1, 8):
    weiboDataList = WeiboData.getDataList(k)
    f = open('..\ResultData\WeiboScore_2_' + str(k) + '.txt', 'w+',encoding='utf-8')
    for singleWeibo in weiboDataList:
        dealedData = []
        for sentence in singleWeibo:
            dicTmp = {}
            seg_list = jieba.cut(sentence)
            for word in seg_list:
                if word not in stopwordslist or word in degreeWordsList:
                    if word != '\t' and word != ' ' and (not word.isdigit()):
                        dicTmp.update({word: 'True'})
            dealedData.append(dicTmp)
        index = []
        for i in range(0, len(dealedData)):
            if len(dealedData[i]) < 2 or dealedData[i]=={'转发': 'True', '微博': 'True'}:
                index.append(i)
        if len(dealedData) > 0:
            pre = classifier.classify_many(dealedData)
            for i in range(0, len(pre)):
                if i in index:
                    f.write('无效\n')
                    print('无效')
                    continue
                f.write(pre[i] + '\n')
                print(pre[i])
        print('——————————单条微博分隔符——————————')
        f.write('——————————单条微博分隔符——————————\n')
    f.close()
