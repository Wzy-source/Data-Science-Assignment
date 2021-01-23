from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re

def stop_words_list():
	stop_words = [line.strip() for line in open('D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\ThemeClassification\stop_words.txt',encoding='UTF-8').readlines()]
	return stop_words


def cut_with_stopwords(str):
	stopwords = stop_words_list()
	res = []
	cut_words = jieba.cut(str)
	for word in cut_words:
		if word not in stopwords and len(word) > 1:
			res.append(word)
	return " ".join(res)


if __name__ == "__main__":
	print("------------开始-------------")
	print("尝试将每篇新闻对应的文本向量降维后表示")
	#读取数据
	data = pd.read_excel('D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Train_Test\\train_kind_res.xls'
						 ,sheet_name=0,usecols=[2,3],nrows=3000)#先读10个试试
	word_list = [cut_with_stopwords(article) for article in data['内容']]
	count_vec = CountVectorizer(min_df=20)
	transformer = TfidfTransformer()

	freq_matrix = count_vec.fit_transform(word_list)
	tfidf = transformer.fit_transform(freq_matrix)
	#用每篇文章的tfidf作为文本特征
	#对tfidf进行降维

	x_tsne = TSNE(n_components=3,random_state=19).fit_transform(tfidf.toarray())
#	print([str(w) for w in x_tsne])
	#dataFrame无法在一个表格中存下一个list
	data['x'] = [w[0] for w in x_tsne]
	data['y'] = [w[1] for w in x_tsne]
	data['z'] = [w[2] for w in x_tsne]
	theme1 = []
	theme2 = []
	theme3 = []
	theme0 = []
	for w in data.iterrows():
		if w[1]['标签'] == 1:
			if(len(theme1)>400):
				continue
			theme1.append([w[1]['x'], w[1]['y'], w[1]['z']])
		if w[1]['标签'] == 2:
			theme2.append([w[1]['x'], w[1]['y'], w[1]['z']])
		if w[1]['标签'] == 3:
			theme3.append([w[1]['x'], w[1]['y'], w[1]['z']])
		if w[1]['标签'] == 0:
			theme0.append([w[1]['x'], w[1]['y'], w[1]['z']])
	fig = plt.figure()
	ax = Axes3D(fig)
	x1 = [w[0] for w in theme1]
	y1 = [w[1] for w in theme1]
	z1 = [w[2] for w in theme1]

	x2 = [w[0] for w in theme2]
	y2 = [w[1] for w in theme2]
	z2 = [w[2] for w in theme2]

	x3 = [w[0] for w in theme3]
	y3 = [w[1] for w in theme3]
	z3 = [w[2] for w in theme3]

	x0 = [w[0] for w in theme0]
	y0 = [w[1] for w in theme0]
	z0 = [w[2] for w in theme0]
	ax.scatter(x1,y1,z1, c='y')
	ax.scatter(x2,y2,z2, c='b')
	ax.scatter(x3,y3,z3, c='r')
	ax.scatter(x0,y0,z0, c='k')
	plt.show()
