# coding:utf-8
# 本脚本文件用于统计刻画CERT6.2中用户的离职情况

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
            print line_lst[1], '\n'
            print user_id, '\n'
            return 'Yes'
    return 'No'




# python列出目标目录下的所有文件
# 使用os.listdir()列出目录下文件
# 使用os.join拼接成文件的绝对路径
# 使用os.isfile判断绝对路径下的对象是否为文件，若是返回True，相对路径全部返回False
print '开始统计CERT6.2的LDAP文件列表...\n'
f_dir = os.listdir(r'S:\内部威胁\数据集\Cert-Data\r4.2\LDAP'.decode('utf-8'))
# f_dir = os.listdir(r'S:\内部威胁\数据集\Cert-Data\r6.2.tar\r6.2\LDAP'.decode('utf-8'))
Cert_file_lst =[]
for filename in f_dir:
    # File_path = join(r'S:\内部威胁\数据集\Cert-Data\r6.2.tar\r6.2\LDAP'.decode('utf-8'), filename)
    File_path = join(r'S:\内部威胁\数据集\Cert-Data\r4.2\LDAP'.decode('utf-8'), filename)
    print isfile(File_path), '\n'
    print File_path, '\n'
    Cert_file_lst.append(File_path.encode('utf-8'))
print len(f_dir), '\n'
for file in Cert_file_lst:
    print file, '\n'
print '目标源文件统计完毕...\n'

print '开始统计2009-12中所有用户的在职记录...\n'
# CERT-2010-06格式：
# employee_name,user_id,email,role,projects,business_unit,functional_unit,department,team,supervisor
Job_state = [] # 存储每个用户18个月的在职状态
print '开始读入标准源文件2009-12.csv...\n'
f_cert = open(r'CERT4.2-2009-12.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()
print '2009-12.csv读入完毕...\n'

print '开始分析每个用户的在职状态...\n'
i = 0
for user in f_cert_lst:
    User_job = [] # 临时存储每个用户的在职状态
    user_l = user.strip('\n').strip(',').split(',')
    if user_l[1] == 'user_id':
        continue
    for filename in Cert_file_lst:
        f = open(filename.decode('utf-8'), 'r')
        print filename, '\n'
        f_lst = f.readlines()
        # print 'f_lst[3] is ', f_lst[2], '\n'
        f.close()
        job_state = LocateUserId(user_l[1], f_lst)
        if job_state == 'Yes':
            User_job.append(1)
        if job_state == 'No':
            User_job.append(0)
    User_job.insert(0, user_l[1])
    Job_state.append(User_job)
    print i, '\t', user_l[1], '在职状态分析完毕..\n'
    print User_job, '\n'
    # print Job_state, '\n'
    i += 1
f_Job_State = open(r'CERT4.2-2009-12-JobState.csv', 'w')
for user in Job_state:
    for ele in user:
        f_Job_State.write(str(ele))
        f_Job_State.write(',')
    f_Job_State.write('\n')
    if user[0] in ['ACM2278', 'CMP2946', 'PLJ1771', 'CDE1846', 'MBG3183']:
        print user[0], '\t', user[1:], '\n'
f_Job_State.close()
print '在职状态写入完毕...\n'
sys.exit()


