import numpy as np
import pandas as pd
import jieba
from keras.models import load_model
import xlrd

pos = pd.read_excel('..\WordsRepos\\EmotionWords\\pos.xls', header=None)
pos['label'] = 1
neg = pd.read_excel('..\WordsRepos\\EmotionWords\\neg.xls', header=None)
neg['label'] = 0
all_ = pos.append(neg, ignore_index=True)

maxlen = 200  # 截断字数
min_count = 20  # 出现次数少于该值的字扔掉。这是最简单的降维方法

content = ''.join(all_[0])
abc = pd.Series(list(content)).value_counts()
abc = abc[abc >= min_count]
abc[:] = list(range(1, len(abc) + 1))
abc[''] = 0  # 添加空字符串用来补全
word_set = set(abc.index)


def doc2num(s, maxlen):
    s = [i for i in s if i in word_set]
    s = s[:maxlen] + [''] * max(0, maxlen - len(s))
    return list(abc[s])


def predict_one(s):  # 单个句子的预测函数
    s = np.array(doc2num(s, maxlen))
    s = s.reshape((1, s.shape[0]))
    return model.predict_classes(s, verbose=0)[0][0]


model = load_model('model5.h5')

dataTables = xlrd.open_workbook('..\WordsRepos\\EmotionWords\\neg.xls')
listOfTableName = dataTables.sheet_names()
table1 = dataTables.sheet_by_name(listOfTableName[0])
dataList = []
total = 0
right = 0
for i in range(0, table1.nrows):
    dataList.append(table1.cell_value(i, 0))
for comment in dataList:
    comment = str(comment)
    total = total + 1
    res = predict_one(comment)
    print(res)
    if res == 0:
        right = right + 1
    if total == 5000:
        break
print(right / total)
