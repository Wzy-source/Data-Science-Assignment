import matplotlib.pyplot as plt
import jieba
import wordcloud
import numpy as np
import pandas as pd
from PIL import Image

def cut(text):
	word_list = []
	stop_word = stop_words_list()
	for w in jieba.cut(text):
		if len(w) > 1 and w not in stop_word:
			word_list.append(w)
	return " ".join(word_list)

def stop_words_list():
	stop_words = [line.strip() for line in open('D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\ThemeClassification\stop_words.txt',encoding='UTF-8').readlines()]
	return stop_words

if __name__ == '__main__':
	data = pd.read_excel('D:\\2020DataScience\officialReports.xls',usecols=[4])
	text = " ".join([cut(w[1]['内容']) for w in data.iterrows()])
	image = np.array(Image.open('D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Data_visualization\OfficialNewsVisualization\china_map.jpg'))
	wc = wordcloud.WordCloud(scale=4,font_path='D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Data_visualization\OfficialNewsVisualization\\vista.ttf',
							 mask=image,max_font_size=40,background_color='white')
	wc.generate(text)
	wc.to_file(r"word_cloud.png")
