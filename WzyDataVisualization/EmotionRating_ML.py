f = open('EmotionRating_ML.txt', 'r')
line = f.readline()
totalData = []
monthData = []
while line:
    try:
        monthData.append(float(line[:-1]))
        # print(line[:-1])
    except:
        totalData.append(monthData)
        monthData = []
        # print(line[:-1])
    line = f.readline()
totalData = totalData[1:]

monthNum = 12

for item in totalData:
    posSum = 0
    negSum = 0
    print("----{}----".format(monthNum))
    for score in item:
        if score == 1:
            posSum = posSum + 1
        else:
            negSum = negSum + 1
    print("pos:{}".format(posSum))
    print("neg:{}".format(negSum))
    monthNum = monthNum - 1

