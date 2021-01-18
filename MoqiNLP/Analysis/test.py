f=open('score2.txt')
list=f.readlines()

count=0
for word in list:
    if word=='无效\n':
       count=count+1
print(count)