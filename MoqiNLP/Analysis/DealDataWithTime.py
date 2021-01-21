import MoqiNLP.Analysis.DealWeiboData as DealWeiboData
for k in range(1,8):
    f1 = open('..\ResultData\WeiboScore' + str(k) + '.txt', 'r')
    f2 = open('..\ResultData\WeiboScore' + str(k) + 'WithTime.txt', 'w+')
    dataList = f1.readlines()
    timeList = DealWeiboData.getTimeList(k)
    strTmp = timeList[0][0][0:2]
    f2.write('——————————' + strTmp + '月——————————\n')
    i = 0
    j = 0
    while j < len(dataList):
        while timeList[i][0][0:2] == strTmp:
            if dataList[j].startswith('无效'):
                j = j + 1
                continue
            if dataList[j].startswith('——'):
                j = j + 1
                i = i + 1
                if i == len(timeList):
                    break
                continue
            f2.write(dataList[j].strip() + '\n')
            j = j + 1
        if i == len(timeList):
            break
        strTmp = timeList[i][0][0:2]
        f2.write('——————————' + strTmp + '月——————————\n')
