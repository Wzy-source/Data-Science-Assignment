import jieba
import xlrd


# 创建停用词list
def createwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


def getDataTable(path):
    #得到文件表格
    #地址'D:\GithubRepos\Data-Science-Assignment\WzySpiderProject\\NewsHeadlines\PeopleWebSpider\疫情&抗疫相关新闻信息.xls'
    dataTables = xlrd.open_workbook(path)
    #获得sheet1
    listOfTableName=dataTables.sheet_names();
    table1=dataTables.sheet_by_name(listOfTableName[0])
    return table1

def getDataList(table1):
    #dataList为处理好的表格内容，以后方面使用，主结构为列表，每个元素为字典，每个字典存一行的标题等
    dataList=[]
    for i in range(0,table1.nrows):
        perRowsDataDict={'标题':table1.cell_value(i,0),'时间':table1.cell_value(i,1),
                         '来源':table1.cell_value(i,2),'网址':table1.cell_value(i,3),'内容':table1.cell_value(i,4)}
        dataList.append(perRowsDataDict)
    return dataList

def separateContent(dataList):
    #所有内容的列表,元素是一个整字符串
    listOfContent=[]
    for i in range(0,len(dataList)):
        listOfContent.append(dataList[i]['内容'])

    #将内容列表中的所有字符串进行分词，并存入新列表
    listOfDealedContent=[]
    stopwordslist1=createwordslist('..\WordsRepos\StopWords\cn_stopwords.txt')
    degreeWordsList=createwordslist('..\WordsRepos\DegreeWords\\all.txt')
    for contentOfPerArticle in listOfContent:
        seg_list = jieba.cut(contentOfPerArticle)
        outstr=[]
        for word in seg_list:
            if word not in stopwordslist1 or word in degreeWordsList:
                if word != '\t' and word!=' ' and (not word.isdigit()):
                    outstr.append(word)
        listOfDealedContent.append(outstr)
    return listOfDealedContent

#主程序部分
table=getDataTable('..\..\WzySpiderProject\\NewsHeadlines\PeopleWebSpider\疫情&抗疫相关新闻信息.xls')
dataList=getDataList(table)
listOfDealedContent=separateContent(dataList)