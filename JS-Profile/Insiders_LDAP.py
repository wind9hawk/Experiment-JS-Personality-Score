# coding:utf-8
# 本脚本用于依据insiders目录，依次匹配目标LDAP(CERT5.2-2010-09.csv)，得到其中所包含的insiders列表

import sys
import os
import re

print '先从指定目录读取insiders...\n'
Insiders_Dir = [r'S:\内部威胁\数据集\Cert-Data\answers\r5.2-1'.decode('utf-8'), r'S:\内部威胁\数据集\Cert-Data\answers\r5.2-2'.decode('utf-8'), r'S:\内部威胁\数据集\Cert-Data\answers\r5.2-3'.decode('utf-8'), r'S:\内部威胁\数据集\Cert-Data\answers\r5.2-4'.decode('utf-8')]
# Insiders文件格式：r5.2-2-BYO1846
Insiders_lst = []
# pattern = re.compile('-.-.*')
for insider_dir in Insiders_Dir:
    filenames = os.listdir(insider_dir)
    for filename in filenames:
        # file_match = pattern.search(filename)
        # print file_match.group(), '\n'
        # print filename, '\n'
        # 由于命名十分规范，因而可以直接使用字符串分片提取用户名
        insider_nm = filename.strip('.csv')[-7:]
        print filename.strip('.csv')[-7:], '\n'
        if insider_nm not in Insiders_lst:
            Insiders_lst.append(insider_nm)
            print insider_nm, 'has been added...\n'
print len(Insiders_lst), '\n'
print 'CERT5.2 Insiders列表收集完毕...\n'

print '开始从CERT-2009-10.csv中匹配Insiders...\n'
f_cert = open(r'CERT5.2-2009-12.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()
Insiders_in_file = []
for line in f_cert_lst:
    line_lst = line.strip('\n').strip(',').split(',')
    if line_lst[1] == 'user_id':
        continue
    if line_lst[1] in Insiders_lst:
        print line_lst[1], '\n'
        if line_lst[1] not in Insiders_in_file:
            Insiders_in_file.append(line_lst[1])
for user in Insiders_in_file:
    print user, '\n'
print 'Insiders_in_file :', len(Insiders_in_file), '\n'
f_insiders = open(r'CERT5.2-2009-12-Insiders.csv', 'w')
for user in Insiders_in_file:
    f_insiders.write(user)
    f_insiders.write('\n')
print 'CERT5.2-2010-09中Insiders统计完毕...\n'
f_insiders.close()
sys.exit()





