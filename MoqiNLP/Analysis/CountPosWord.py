from numpy import double
'''用于数结果的，主要怕出现高于10分的'''
f=open('..\ResultData\WeiboScore5.txt', 'r')
positive=0
negative=0
list=f.readlines()
max=0
min=0
for i in range (0, len(list)):
    if list[i].startswith('——') or list[i].startswith('无效'):
        continue
    if(double(list[i].strip())>0):
        positive=positive+1
    elif(double(list[i].strip())<0):
        negative=negative+1

    '''if double(score.strip())>max:
        max=double(score.strip())
    if double(score.strip())<min:
        min=double(score.strip())'''

print('positive:',positive)
print('negative:',negative)

f=open('..\ResultData\WeiboScore_1_5.txt', 'r')
positive=0
negative=0
list=f.readlines()
max=0
min=0
for i in range (0, len(list)):
    if list[i].startswith('——') or list[i].startswith('无效'):
        continue
    if(double(list[i].strip())>0):
        positive=positive+1
    elif(double(list[i].strip())<0):
        negative=negative+1

    '''if double(score.strip())>max:
        max=double(score.strip())
    if double(score.strip())<min:
        min=double(score.strip())'''

print('positive:',positive)
print('negative:',negative)