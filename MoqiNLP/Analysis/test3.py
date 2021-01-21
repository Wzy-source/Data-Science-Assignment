list=open('WeiboScore1.txt').readlines()
count=0
for num in list:
    if num=='无效\n':
        continue
    else:
       count=count+1
print(count)