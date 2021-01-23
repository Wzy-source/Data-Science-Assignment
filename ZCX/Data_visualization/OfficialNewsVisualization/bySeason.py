from pyecharts.charts import Bar
import pandas as pd


if __name__ == '__main__':
	data1 = pd.read_excel("D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Train_Test\\train_kind_res.xls",
						  usecols=[1,4],sheet_name=0)
	data2 = pd.read_excel("D:\\2020DataScience\MyWork\Data-Science-Assignment\ZCX\Train_Test\\test_kin_res.xls",
						  usecols=[1,4],sheet_name=0)
	quater_sum = {}
	theme1 = {}#抗疫
	theme2 = {}#国际
	theme3 = {}#经济
	theme4 = {}#脱贫
	for itr in data1.iterrows():
		month = int(str(itr[1]['时间'])[5:7])
		if(month>=1 and month <=3):
			if '抗疫' in itr[1]['分类']:
				if'第一季度' in theme1:
					theme1['第一季度'] += 1
				else:
					theme1['第一季度'] = 1
			if '国际' in itr[1]['分类']:
				if'第一季度' in theme2:
					theme2['第一季度'] += 1
				else:
					theme2['第一季度'] = 1
			if '经济' in itr[1]['分类']:
				if'第一季度' in theme3:
					theme3['第一季度'] += 1
				else:
					theme3['第一季度'] = 1
			if '脱贫' in itr[1]['分类']:
				if'第一季度' in theme4:
					theme4['第一季度'] += 1
				else:
					theme4['第一季度'] = 1
			if '第一季度' not in quater_sum:
				quater_sum['第一季度'] = 1
			else:
				quater_sum['第一季度'] += 1
		if(month >=4 and month <= 6):
			if '抗疫' in itr[1]['分类']:
				if'第二季度' in theme1:
					theme1['第二季度'] += 1
				else:
					theme1['第二季度'] = 1
			if '国际' in itr[1]['分类']:
				if'第二季度' in theme2:
					theme2['第二季度'] += 1
				else:
					theme2['第二季度'] = 1
			if '经济' in itr[1]['分类']:
				if'第二季度' in theme3:
					theme3['第二季度'] += 1
				else:
					theme3['第二季度'] = 1
			if '脱贫' in itr[1]['分类']:
				if'第二季度' in theme4:
					theme4['第二季度'] += 1
				else:
					theme4['第二季度'] = 1
			if '第二季度' not in quater_sum:
				quater_sum['第二季度'] = 1
			else:
				quater_sum['第二季度'] += 1
		if (month >= 7 and month <= 9):
			if '抗疫' in itr[1]['分类']:
				if'第三季度' in theme1:
					theme1['第三季度'] += 1
				else:
					theme1['第三季度'] = 1
			if '国际' in itr[1]['分类']:
				if'第三季度' in theme2:
					theme2['第三季度'] += 1
				else:
					theme2['第三季度'] = 1
			if '经济' in itr[1]['分类']:
				if'第三季度' in theme3:
					theme3['第三季度'] += 1
				else:
					theme3['第三季度'] = 1
			if '脱贫' in itr[1]['分类']:
				if'第三季度' in theme4:
					theme4['第三季度'] += 1
				else:
					theme4['第三季度'] = 1
			if '第三季度' not in quater_sum:
				quater_sum['第三季度'] = 1
			else:
				quater_sum['第三季度'] += 1
		if (month >= 10 and month <= 12):
			if '抗疫' in itr[1]['分类']:
				if'第四季度' in theme1:
					theme1['第四季度'] += 1
				else:
					theme1['第四季度'] = 1
			if '国际' in itr[1]['分类']:
				if'第四季度' in theme2:
					theme2['第四季度'] += 1
				else:
					theme2['第四季度'] = 1
			if '经济' in itr[1]['分类']:
				if'第四季度' in theme3:
					theme3['第四季度'] += 1
				else:
					theme3['第四季度'] = 1
			if '脱贫' in itr[1]['分类']:
				if'第四季度' in theme4:
					theme4['第四季度'] += 1
				else:
					theme4['第四季度'] = 1
			if '第四季度' not in quater_sum:
				quater_sum['第四季度'] = 1
			else:
				quater_sum['第四季度'] += 1
	for itr in data2.iterrows():
		month = int(str(itr[1]['时间'])[5:7])
		if (month >= 1 and month <= 3):
			if '第一季度' not in quater_sum:
				quater_sum['第一季度'] = 1
			else:
				quater_sum['第一季度'] += 1
		if (month >= 4 and month <= 6):
			if '第二季度' not in quater_sum:
				quater_sum['第二季度'] = 1
			else:
				quater_sum['第二季度'] += 1
		if (month >= 7 and month <= 9):
			if '第三季度' not in quater_sum:
				quater_sum['第三季度'] = 1
			else:
				quater_sum['第三季度'] += 1
		if (month >= 10 and month <= 12):
			if '第四季度' not in quater_sum:
				quater_sum['第四季度'] = 1
			else:
				quater_sum['第四季度'] += 1

	bar = Bar()
	bar.add_xaxis([w for w in quater_sum])
	bar.add_yaxis('新闻总数',[quater_sum[w] for w in quater_sum])
	bar.render()

	bar2 = Bar()
	bar2.add_xaxis([w for w in quater_sum])
	bar2.add_yaxis('抗疫相关',[round(theme1[w]/quater_sum[w],3) for w in theme1])
	bar2.add_yaxis('国际相关',[round(theme2[w]/quater_sum[w],3)for w in theme2])
	bar2.add_yaxis('经济相关',[round(theme3[w]/quater_sum[w],3)for w in theme3])
	bar2.add_yaxis('脱贫攻坚',[round(theme4[w]/quater_sum[w],3)for w in theme4])
	bar2.render()
