f = open('..\ResultData\WeiboMentalityAll.txt','w+')

for k in range(1, 8):
    f2 = open('..\ResultData\WeiboMentality' + str(k) + 'WithTime.txt', 'r')
    listTmp = f2.readlines()
    for item in listTmp:
        f.write(item.strip()+'\n')

f.close()