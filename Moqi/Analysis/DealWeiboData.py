import xlrd


def getDataTable(path):
    # 得到文件表格
    # 地址'D:\GithubRepos\Data-Science-Assignment\WzySpiderProject\\NewsHeadlines\PeopleWebSpider\疫情&抗疫相关新闻信息.xls'
    dataTables = xlrd.open_workbook(path)
    # 获得sheet1
    listOfTableName = dataTables.sheet_names()
    table1 = dataTables.sheet_by_name(listOfTableName[0])
    return table1


def getComments(table):
    dataList = []
    tmplist = []
    for i in range(1, table.nrows):
        for j in range(6, 6 + int(table.cell_value(i, 5))):
            tmplist.append(table.cell_value(i, j))
        dataList.append(tmplist)
        tmplist = []
    return dataList


def getDataList(num):
    dataTable = getDataTable('..\..\WzySpiderProject\WeiboSpider\\微博id：健康中国(热门含评论)' + str(num) + '.xls')
    dataList = getComments(dataTable)
    return dataList


def getTimeList(num):
    table = getDataTable('..\..\WzySpiderProject\WeiboSpider\\微博id：健康中国(热门含评论)' + str(num) + '.xls')
    timeList=[]
    tmpList=[]
    for i in range(1, table.nrows):
        tmpList.append(table.cell_value(i,4))
        tmpList.append(table.cell_value(i,5))
        timeList.append(tmpList)
        tmpList=[]
    return timeList
