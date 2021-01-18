from numpy import double

f=open('score1.txt', 'r')
positive=0
negative=0
list=f.readlines()
for score in list:
    if(score=='无效\n'):
        continue
    if(double(score.strip())>5):
        positive=positive+1
    elif(double(score.strip())<0):
        negative=negative+1

print(positive)
print(negative)