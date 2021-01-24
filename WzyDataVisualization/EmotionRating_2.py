f = open('EmotionRating_2.txt', 'r')
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
    posNum = 0
    negNum = 0
    posSum = 0.0
    negSum = 0.0
    print("----{}----".format(monthNum))
    for score in item:
        if score > 10.0:
            score = 10.0
        if score < -10.0:
            score = -10.0
        if score >= 0:
            posSum = posSum + score
            posNum = posNum + 1
        else:
            negSum = negSum + score
            negNum = negNum + 1
    print("posNum:{}".format(posNum))
    print("negNum:{}".format(negNum))
    print("posScore:{}".format(posSum / posNum))
    print("negScore:{}".format((-1) * negSum / negNum))
    
    monthNum = monthNum - 1
