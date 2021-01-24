
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import jieba
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA

def word_cut(txt):
	res = []
	cut_words = jieba.cut(txt)
	for word in cut_words:
		if len(str(word)) > 1:
			res.append(word)
	return " ".join(res)

if __name__ == '__main__':
	data1 = pd.read_excel('D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Data_visualization\WeiboCommentVisualization\comment7.xls')
	label_txt = open('D:\\2020DataScience\MyWork\Data-Science-Assignment\MoqiNLP\ResultData\WeiboScore_2_7.txt','r',encoding='utf-8')
	label = []
	for line in label_txt.readlines():
		mental = line.strip('\n')
		if 'n' in mental:
			label.append('neg')
		if 'p' in mental:
			label.append('pos')
		if '无'in mental:
			label.append('无效')
#	print(label)#记录每条微博评论的情感
#	print(data1.head())
	comment_list = []
	count_vec = CountVectorizer()
	transformer = TfidfTransformer()
	for itr in data1.iterrows():
		comment_num = itr[1]['评论数']
		#评论从第六列开始
		for i in range(0, comment_num):
			comment_list.append(itr[1][i+6])
#	成功，两者数量可以匹配
#	print("标签的个数"+str(len(label)))
#	print("评论的个数"+str(len(comment_list)))
	print(comment_list)
	word_list = [word_cut(comment) for comment in comment_list]
	freq_matrix = count_vec.fit_transform(word_list)
	tfidf = transformer.fit_transform(freq_matrix)
#	x_tsne = TSNE(n_components=3, random_state=19).fit_transform(tfidf.toarray())
	x_tsne = PCA(n_components=3,random_state=19).fit_transform(tfidf.toarray())
#	print(x_tsne)
	pos_dimension = []
	neg_dimension = []
	invalid_dimension = []
	for i in range(0,len(comment_list)):
		if 'n' in label[i]:
			neg_dimension.append([x_tsne[i][0],x_tsne[i][1],x_tsne[i][2]])
		if 'p' in label[i]:
			pos_dimension.append([x_tsne[i][0],x_tsne[i][1],x_tsne[i][2]])
		if '无' in label[i]:
			invalid_dimension.append([x_tsne[i][0],x_tsne[i][1],x_tsne[i][2]])

	x1 = [w[0] for w in pos_dimension]
	y1 = [w[1] for w in pos_dimension]
	z1 = [w[2] for w in pos_dimension]

	x2 = [w[0] for w in neg_dimension]
	y2 = [w[1] for w in neg_dimension]
	z2 = [w[2] for w in neg_dimension]

	x3 = [w[0] for w in invalid_dimension]
	y3 = [w[1] for w in invalid_dimension]
	z3 = [w[2] for w in invalid_dimension]
	fig = plt.figure()
	ax = Axes3D(fig)
	print(pos_dimension)
	ax.scatter(x1,y1,z1 ,c='r')#红色表示积极
	ax.scatter(x2,y2,z2, c='b')# 蓝色表示消极
	ax.scatter(x3,y3,z3, c='w')#白色表示无效
	plt.show()

