import pandas as pd
import jieba
import jieba.analyse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans

count_vec = CountVectorizer()#词频特征提取
transformer = TfidfTransformer()#TF-IDF特征转化
kmeans_cluster = KMeans(n_clusters=4,random_state=19)#KMeans模型
def analyse_kmeans():
	print("尝试使用kmeans方法对文本进行聚类分析")
	#先读取数据
	#在训练文件中读取
	data = pd.read_excel("D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Train_Test\\train.xls", sheet_name=0,usecols=[0,1,4])
	#进行分词处理
	word_list = [cut_with_stopwords(article) for article in data['内容']]
#	print(word_list)
	#对切词文本进行词频统计
	freq_matrix = count_vec.fit_transform(word_list)
#	print(count_vec.get_feature_names())
#	print(freq_matrix.toarray())
	tfidf = transformer.fit_transform(freq_matrix)

	kmeans_cluster.fit(tfidf)
	data['标签'] = kmeans_cluster.labels_
	#对分类结果进行计数
	kind_cluster_count_f = open("D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Data_visualization\OfficialNewsVisualization\kccf.txt",
								"w+",encoding='utf-8')
	kind_dict = {}
	for label in kmeans_cluster.labels_:
		if label in kind_dict:
			kind_dict[label] += 1
		else:
			kind_dict[label] = 1
	for label in kind_dict:
		kind_cluster_count_f.write(str(label)+" "+str(kind_dict[label])+'\r')
#	print(data.head())
	kind_cluster_count_f.close()
	datagrp = data.groupby('标签')
	datacls = datagrp.agg(sum)
	print(datacls)
	cuttex = lambda x:cut_with_stopwords(x)
	dataclusters = datacls['内容'].apply(cuttex)

#	print(dataclusters)
	print("------------------训练集分类-------------------")
	key_list = []
	for item in dataclusters:
		print(jieba.analyse.extract_tags(item, topK=10))
		key_list.append(jieba.analyse.extract_tags(item, topK=1))
	data['分类'] = [map(kind,key_list) for kind in kmeans_cluster.labels_]
	data.to_excel('D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Train_Test\\train_kind_res.xls',index = False)
	my_test()


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


def map(kind_num,key_list):
	if '脱贫' in key_list[kind_num] :
		return '脱贫攻坚'
	if '抗击'in key_list[kind_num]:
		return '抗疫相关'
	if '中国'in key_list[kind_num]:
		return '国际相关'
	if'经济社会' or '经济'in key_list[kind_num]:
		return '经济相关'


def my_test():
	# 准备使用测试集进行测试
	# 测试集315篇文章
	test_data = pd.read_excel("D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Train_Test\\test.xls", sheet_name=0,
							  usecols=[0,1,4])
#	print(test_data.head())
	test_word_list = [cut_with_stopwords(article) for article in test_data['内容']]
	# 对切词文本进行词频统计
	test_freq_matrix = count_vec.transform(test_word_list)
	#	print(count_vec.get_feature_names())
	#	print(test_freq_matrix.toarray())
	tfidf = transformer.transform(test_freq_matrix)
	freq_dict = {}#用于记录测试集的分类计数
	test_kind_count = open("D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Data_visualization\OfficialNewsVisualization"
						   "\\count.txt","w+",encoding='utf-8')
	# 对测试数据进行预测
	test_data['预测'] = kmeans_cluster.predict(tfidf)
	for label in kmeans_cluster.predict(tfidf):
		if label in freq_dict:
			freq_dict[label] += 1
		else:
			freq_dict[label] = 1
	for label in freq_dict:
		test_kind_count.write(str(label)+" "+str(freq_dict[label])+'\r')
	test_kind_count.close()
#	print(test_data.head())
	t_datagrp = test_data.groupby('预测')
	t_datacls = t_datagrp.agg(sum)
#	print(t_datacls)
	cuttex = lambda x: cut_with_stopwords(x)
	t_dataclusters = t_datacls['内容'].apply(cuttex)

	#	print(dataclusters)
	print("------------------测试集分类-------------------")
	key_list = []
	for item in t_dataclusters:
		print(jieba.analyse.extract_tags(item, topK=10))
		key_list.append(jieba.analyse.extract_tags(item, topK=1))
	print(key_list)
	test_data['分类'] = [map(kind, key_list) for kind in kmeans_cluster.predict(tfidf)]
#	print(test_data)
	test_data.to_excel('D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Train_Test\\test_kin_res.xls',index=False)
	file = open('D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Train_Test\\predict_res.txt','w+',encoding='utf-8')
	index = 1
	for itr in test_data.iterrows():
#		print(itr[0])
		file.write("------第"+str(index)+"篇文章预测------\r")
		file.write("文章名：《"+itr[1]['文章名称']+'》 文章时间：'+str(itr[1]['时间'])+'\r')
		file.write(itr[1]['分类']+'\r'+str(itr[1]['内容'])+"\r\r")
		index += 1
	file.close()


if __name__ == '__main__':
	analyse_kmeans()
	#分析接口
