from __future__ import absolute_import #导入3.x的特征函数
from __future__ import print_function

import pandas as pd #导入Pandas
import numpy as np #导入Numpy
import jieba #导入结巴分词
from keras.preprocessing import sequence
from keras.optimizers import SGD, RMSprop, Adagrad
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
import MoqiNLP.Analysis.LSTM as LSTM
import OneEmbedding

data=pd.read_excel('..\..\WzySpiderProject\\NewsHeadlines\PeopleWebSpider\疫情&抗疫相关新闻信息.xls',header=None,usecols=[4,4])
cw = lambda x: list(jieba.cut(x)) #定义分词函数
data['words'] = data[4].apply(cw)
d2v_train = pd.concat([data['words']], ignore_index = True)

w = [] #将所有词语整合在一起
for i in d2v_train:
    w.extend(i)

dict = pd.DataFrame(pd.Series(w).value_counts()) #统计词的出现次数
print(dict)
del w,d2v_train
dict['id']=list(range(1,len(dict)+1))

get_sent = lambda x: list(dict['id'][x])
data['sent'] = data['words'].apply(get_sent) #速度太慢
print(data['sent'])

maxlen = 50

print("Pad sequences (samples x time)")
data['sent'] = list(sequence.pad_sequences(data['sent'], maxlen=maxlen))

xt = np.array(list(data['sent']))
f=open('score3.txt','w+')
result=LSTM.model.predict(xt)
print(result)
for num in result:
    f.write(str(num)+'\n')
f.close()