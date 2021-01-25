import numpy as np
import pandas as pd
'''失败了'''
pos = pd.read_excel('..\WordsRepos\\EmotionWords\\positive.xls', header=None)
pos['label'] = 1
neg = pd.read_excel('..\WordsRepos\\EmotionWords\\negative.xls', header=None)
neg['label'] = 0
all_ = pos.append(neg, ignore_index=True)

for i in range(0, len(all_[0])):
    all_[0][i]=str(all_[0][i])


maxlen = 200
min_count = 20
content = ''.join(all_[0])
abc = pd.Series(list(content)).value_counts()
abc = abc[abc >= min_count]
abc[:] = list(range(1, len(abc) + 1))
abc[''] = 0
word_set = set(abc.index)


def doc2num(s, maxlen):
    s = [i for i in s if i in word_set]
    s = s[:maxlen] + [''] * max(0, maxlen - len(s))
    return list(abc[s])


all_['doc2num'] = all_[0].apply(lambda s: doc2num(s, maxlen))

idx = list(range(len(all_)))
np.random.shuffle(idx)
all_ = all_.loc[idx]

x = np.array(list(all_['doc2num']))
y = np.array(list(all_['label']))
y = y.reshape((-1, 1))

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Embedding
from keras.layers import LSTM

model = Sequential()
model.add(Embedding(len(abc), 676, input_length=maxlen))
model.add(LSTM(256))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

batch_size = 128
train_num = 15000

model.fit(x[:train_num], y[:train_num], batch_size=batch_size, epochs=10)
model.save("modelv2.0.h5")
model.evaluate(x[train_num:], y[train_num:], batch_size=batch_size)


def predict_one(s):
    s = np.array(doc2num(s, maxlen))
    s = s.reshape((1, s.shape[0]))
    return model.predict_classes(s, verbose=0)[0][0]


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
