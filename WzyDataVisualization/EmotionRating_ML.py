f = open('EmotionRating_ML.txt', 'r')
line = f.readline()
totalData = []
monthData = []
while line:
    if(not line[:-1].isnumeric()):
        monthData.append(line[:-1])
        # print(line[:-1])
    else:
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
        if score == 'pos':
            posSum = posSum + 1
        else:
            negSum = negSum + 1
    print("pos:{}".format(posSum))
    print("neg:{}".format(negSum))
    monthNum = monthNum - 1

