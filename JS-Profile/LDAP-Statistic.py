# coding:utf-8
# 本脚本负责分析全部的CERT6.2-LDAP和CERT5.2-LDAP，从而得到4000个用户与2000个用户的全面的LDAP，避免单个LDAP中用户不足的情况
# 为了分析CERT6.2中周围同事在职状态对用户的影响，因此需要从全用户开始分析

import sys
import os
from os.path import isfile, join

# 定义一个查找函数
# 在职返回Yes，不在职返回No
def LocateUserId(user_id, file_lst):
    for line in file_lst:
        line_lst = line.strip('\n').strip(',').split(',')
        if line_lst[1] == 'user_id':
            continue
        # print 'LocateUserId is ', line_lst[1], '\n'
        # print line_lst, '\n'
        # print user_id, '\n'
        if line_lst[1] == user_id:
            # print line_lst[1], '\n'
            # print user_id, '\n'
            return line_lst
    return 'No'

# python列出目标目录下的所有文件
# 使用os.listdir()列出目录下文件
# 使用os.join拼接成文件的绝对路径
# 使用os.isfile判断绝对路径下的对象是否为文件，若是返回True，相对路径全部返回False
print '开始统计CERT6.2全部用户的LDAP文件列表...\n'
f_dir = os.listdir(r'S:\内部威胁\数据集\Cert-Data\r5.2\LDAP'.decode('utf-8'))
Cert_file_lst =[]
for filename in f_dir:
    File_path = join(r'S:\内部威胁\数据集\Cert-Data\r5.2\LDAP'.decode('utf-8'), filename)
    print isfile(File_path), '\n'
    print File_path, '\n'
    Cert_file_lst.append(File_path.encode('utf-8'))
print len(f_dir), '\n'
for file in Cert_file_lst:
    print file, '\n'
print '目标源文件统计完毕...\n'

print '读取全用户列表...\n'
f_psy = open(r'psychometric-5.2.csv', 'r')
f_psy_lst = f_psy.readlines()
f_psy.close()
print 'psychometric文件读取完毕...\n'

print '开始建立全用户LDAP...\n'
Users_LDAP = []
Users_Addtion = []
Cnt_user = 0
for psy in f_psy_lst[0:-1]:
    psy_lst = psy.strip('\n').strip(',').split(',')
    # employee_name,user_id,O,C,E,A,N
    # Nicholas Fletcher Pruitt,NFP2441,34,39,38,36,21
    if psy_lst[1] == 'user_id':
        continue
    User_LDAP = []
    for filename in Cert_file_lst:
        f = open(filename.decode('utf-8'), 'r')
        f_lst = f.readlines()
        f.close()
        ldap = LocateUserId(psy_lst[1], f_lst)
        if ldap == 'No':
            print filename, '没有该用户...\n'
            continue
        if ldap not in User_LDAP:
            User_LDAP.append(ldap)
            continue
    if len(User_LDAP) > 1:
        i = 0
        while i < len(User_LDAP):
            Users_LDAP.append(User_LDAP[i])
            Users_Addtion.append(User_LDAP[i])
            i += 1

    if len(User_LDAP) == 1:
        Users_LDAP.append(User_LDAP[0])
    print Cnt_user, '\t', psy_lst[1], 'LDAP建立完毕...\n'
    Cnt_user += 1
print 'Users_LDAP已经建立，准备写入新的LDAP文件...\n'

f_ldap = open(r'CERT6.2-LDAP-all.csv', 'w')
for line in Users_LDAP:
    # print line, '\n'
    for ele in line:
        f_ldap.write(str(ele))
        f_ldap.write(',')
    f_ldap.write('\n')
print 'CERT5.2-LDAP-all.csv写入完毕...\n'
print len(Users_LDAP), '\n', # Users_LDAP, '\n'
print len(Users_Addtion), '\n', # Users_Addtion, '\n'
sys.exit()

