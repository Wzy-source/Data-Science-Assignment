import xlwt

# workbook = xlwt.Workbook(encoding="utf-8")  #创建workbook对象
# worksheet = workbook.add_sheet('sheet1')   # 创建工作表
# worksheet.write(0,0,"hello")  # 写入数据，第一个参数是行，第二个参数是列
# workbook.save('student.xls')


workbook = xlwt.Workbook(encoding='utf-8')
worksheet  = workbook.add_sheet('sheet1')
for i in range(0,9):
    for j in range(0,i+1):
        k = i*j
        worksheet.write(i,j,k)

workbook.save('student.xls')
