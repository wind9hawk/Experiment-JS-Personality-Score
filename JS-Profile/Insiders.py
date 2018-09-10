# coding:utf-8
import sys
import os

f_insiders = open(r'insiders.csv', 'r')
f_insiders_lst = f_insiders.readlines()
f_insiders.close()

Insiders_1 = []
Insiders_2 = []
Insiders_3 = []
for line in f_insiders_lst:
    line_lst = line.strip('\n').strip(',').split(',')
    # dataset	scenario	details	user	start	end
    #2	1	r2.csv	ONS0995	3/6/2010 1:41:56	3/20/2010 8:10:12
    if line_lst[0] != '4.2':
        print '非指定数据集...\n'
        continue
    if line_lst[1] == '1':
        Insiders_1.append(line_lst[3])
    if line_lst[1] == '2':
        Insiders_2.append(line_lst[3])
    if line_lst[1] == '3':
        Insiders_3.append(line_lst[3])
    continue
print 'Insiders-1 length is ', len(Insiders_1), '\n'
f_insiders_w = open(r'CERT4.2-Insiders.csv', 'w')
f_insiders_w.write('Insiders_1')
f_insiders_w.write(',')
for user in Insiders_1:
    f_insiders_w.write(user)
    f_insiders_w.write(',')
f_insiders_w.write('\n')
f_insiders_w.write('Insiders_2')
f_insiders_w.write(',')
for user in Insiders_2:
    f_insiders_w.write(user)
    f_insiders_w.write(',')
f_insiders_w.write('\n')
f_insiders_w.write('Insiders_3')
f_insiders_w.write(',')
for user in Insiders_3:
    f_insiders_w.write(user)
    f_insiders_w.write(',')
f_insiders_w.write('\n')
f_insiders_w.close()
print 'CERT Insiders 文件写入完成...\n'
sys.exit()



