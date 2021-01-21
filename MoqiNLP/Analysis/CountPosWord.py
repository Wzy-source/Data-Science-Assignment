from numpy import double
'''用于数结果的，主要怕出现高于10分的'''
f=open('..\ResultData\WeiboScore1.txt', 'r')
positive=0
negative=0
list=f.readlines()
max=0
min=0
for score in list:
    if score.startswith('——') or score.startswith('无效'):
        continue
    if(double(score.strip())>0):
        positive=positive+1
    elif(double(score.strip())<0):
        negative=negative+1

    if double(score.strip())>max:
        max=double(score.strip())
    if double(score.strip())<min:
        min=double(score.strip())

print(positive)
print(negative)
print(max)
print(min)