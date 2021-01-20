# -*- coding:utf-8 -*-

'''
one embedding测试
在GTX960上，36s一轮
经过30轮迭代，训练集准确率为95.95%，测试集准确率为89.55%
Dropout不能用太多，否则信息损失太严重
'''

import numpy as np
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
abc = abc[abc >= min_count]
abc[:] = list(range(1, len(abc) + 1))
abc[''] = 0  # 添加空字符串用来补全
word_set = set(abc.index)


def doc2num(s, maxlen):
    s = [i for i in s if i in word_set]
    s = s[:maxlen] + [''] * max(0, maxlen - len(s))
    return list(abc[s])


all_['doc2num'] = all_[0].apply(lambda s: doc2num(s, maxlen))

# 手动打乱数据
idx = list(range(len(all_)))
np.random.shuffle(idx)
all_ = all_.loc[idx]

# 按keras的输入要求来生成数据
x = np.array(list(all_['doc2num']))
y = np.array(list(all_['label']))
y = y.reshape((-1, 1))  # 调整标签形状

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Embedding
from keras.layers import LSTM

# 建立模型
model = Sequential()
model.add(Embedding(len(abc), 256, input_length=maxlen))
model.add(LSTM(128))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

batch_size = 128
train_num = 15000

model.fit(x[:train_num], y[:train_num], batch_size=batch_size, epochs=30)
model.save("model5.h5")
model.evaluate(x[train_num:], y[train_num:], batch_size=batch_size)


def predict_one(s):  # 单个句子的预测函数
    s = np.array(doc2num(s, maxlen))
    s = s.reshape((1, s.shape[0]))
    return model.predict_classes(s, verbose=0)[0][0]


print(predict_one('今天天气真好'))
print(predict_one('今天天气不错'))
print(predict_one('今天天气好差'))
print(predict_one('今天天气糟透了'))
print(predict_one('我不讨厌这个天气'))

'''f=open('score5.txt','w+')
data=pd.read_excel('..\..\WzySpiderProject\\NewsHeadlines\PeopleWebSpider\疫情&抗疫相关新闻信息.xls',header=None,usecols=[4,4])
data['doc2num'] = data[4].apply(lambda s: doc2num(s, maxlen))
x=np.array(list(data['doc2num']))
result=model.predict(x)
print(result)
for num in result:
    f.write(str(num)+'\n')
f.close()
'''
