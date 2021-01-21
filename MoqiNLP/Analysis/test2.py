import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from keras.models import load_model

import pandas as pd

pos = pd.read_excel('..\WordsRepos\\EmotionWords\\pos.xls', header=None)
pos['label'] = 1
neg = pd.read_excel('..\WordsRepos\\EmotionWords\\neg.xls', header=None)
neg['label'] = 0
all_ = pos.append(neg, ignore_index=True)

maxlen = 200  # 截断字数
min_count = 20  # 出现次数少于该值的字扔掉。这是最简单的降维方法

content = ''.join(all_[0])
abc = pd.Series(list(content)).value_counts()
print(abc)
abc = abc[abc >= min_count]
abc[:] = list(range(1, len(abc) + 1))
abc[''] = 0  # 添加空字符串用来补全
word_set = set(abc.index)


def doc2num(s, maxlen):
    s = [i for i in s if i in word_set]
    print(s)
    s = s[:maxlen] + [''] * max(0, maxlen - len(s))
    print(s)
    print(list(abc[s]))
    return list(abc[s])


def predict_one(s):  # 单个句子的预测函数
    s = np.array(doc2num(s, maxlen))
    print(s)
    s = s.reshape((1, s.shape[0]))
    return model.predict_classes(s, verbose=0)[0][0]


model = load_model('model5.h5')

print(predict_one('我讨厌你'))

