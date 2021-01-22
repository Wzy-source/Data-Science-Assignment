import numpy as np
import pandas as pd
import jieba
from keras.models import load_model

pos = pd.read_excel('..\WordsRepos\\EmotionWords\\positive.xls', header=None)
pos['label'] = 1
neg = pd.read_excel('..\WordsRepos\\EmotionWords\\negative.xls', header=None)
neg['label'] = 0
all_ = pos.append(neg, ignore_index=True)

for i in range(0, len(all_[0])):
    all_[0][i]=str(all_[0][i])


all_['words'] = all_[0].apply(lambda s: list(jieba.cut(s)))  # 调用结巴分词

maxlen = 150  # 截断词数
min_count = 5  # 出现次数少于该值的词扔掉。这是最简单的降维方法

content = []
for i in all_['words']:
    content.extend(i)

abc = pd.Series(content).value_counts()
abc = abc[abc >= min_count]
abc[:] = list(range(1, len(abc) + 1))
abc[''] = 0  # 添加空字符串用来补全
word_set = set(abc.index)


def doc2num(s, maxlen):
    s = [i for i in s if i in word_set]
    s = s[:maxlen] + [''] * max(0, maxlen - len(s))
    return list(abc[s])

def predict_one(s):  # 单个句子的预测函数
    s = np.array(doc2num(list(jieba.cut(s)), maxlen))
    s = s.reshape((1, s.shape[0]))
    return model.predict_classes(s, verbose=0)[0][0]


model=load_model('modelv1.5.h5')