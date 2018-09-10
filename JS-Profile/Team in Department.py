# coding:utf-8
# 本脚本主要用于统计每个部门中所包含的团队名称

import sys

print '导入部门列表文件...\n'
print '导入用户原始数据2010-07.csv文件...\n'
f_dpt = open(r'2010-07-Department.csv', 'r')
f_cert = open(r'2010-07.csv', 'r')
f_dpt_lst = f_dpt.readlines()
f_cert_lst = f_cert.readlines()
f_dpt.close()
f_cert.close()
print '部门文件与原始数据文件导入完毕...\n'

print '建立原始部门名称列表...\n'
Department_lst = []
for dpt in f_dpt_lst:
    # dpt_lst = dpt.strip('\n').strip(',').split(',')
    if 'Department' in dpt:
        print '标题行跳过...\n'
        continue
    Department_lst.append(dpt) #写入了'\n'，因此后面需要使用strip('\n')变成纯字符串
print 'Department is ', Department_lst, '\t', len(Department_lst), '\n'
print '部门列表导入完毕...\n'

print '开始统计每个部门所属的团队...\n'
Team_in_Department_lst = []
Short_Record_lst = []
for dpt_str in Department_lst:
    Team_in_Dpt_tmp = []
    dpt = dpt_str.strip('\n').strip(',')
    # print 'dpt is ', dpt, '\n'
    # 原始数据基本格式：
    # employee_name,user_id,email,role,projects,business_unit,functional_unit,department,team,supervisor
    for line in f_cert_lst[0:-1]:
        line_lst = line.strip('\n').strip(',').split(',')
        # print 'line_lst[-3] is : ', line_lst[-3], '\n'
        # print 'line_lst is ', line_lst, '\n'
        # print 'dpt is ', dpt, '\n'
        # print 'line_lst[-3] is ', line_lst[-3], '\n'
        if len(line_lst) < 10:
            if line_lst not in Short_Record_lst:
                Short_Record_lst.append(line_lst)
                continue
        if dpt != line_lst[-3]:
            print dpt, 'and ', line_lst[-3], '\t', '部门字段不匹配，跳过...\n'
            continue
        else:
            # 首先判断部门为Free-dpt的情况
            # print 'Department 字段为: ', line_lst[-3], '\n'
            if dpt == 'Free-dpt':
                if line_lst[-3] == '':
                    if line_lst[-2] == '':
                        if 'Free-tm' not in Team_in_Dpt_tmp:
                            Team_in_Dpt_tmp.append('Free-tm')
                            continue
                    else:
                        if line_lst[-2] not in Team_in_Dpt_tmp:
                            Team_in_Dpt_tmp.append(line_lst[-2])
                            continue
                else:
                    continue
            # 如果不是空部门
            else:
                # 如果是空团队
                if line_lst[-2] == '':
                    if 'Free-tm' not in Team_in_Dpt_tmp:
                        Team_in_Dpt_tmp.append('Free-tm')
                        continue
                else:
                    if line_lst[-2] not in Team_in_Dpt_tmp:
                        Team_in_Dpt_tmp.append(line_lst[-2])
                        continue
    Team_in_Dpt_tmp.sort()
    Team_in_Department_lst.append(Team_in_Dpt_tmp)
print 'Team in Department is \n'
# for line in Team_in_Department_lst:
#     print line, '\n'
f_tm_in_dpt = open(r'2010-07-Team in Department.csv', 'w')
f_tm_in_dpt.write('Team in Department')
f_tm_in_dpt.write('\n')
i = 0
while i < len(Department_lst):
    f_tm_in_dpt.write(Department_lst[i].strip('\n'))
    f_tm_in_dpt.write(',')
    # f_tm_in_dpt.write('\n')
    for ele in Team_in_Department_lst[i]:
        f_tm_in_dpt.write(ele)
        f_tm_in_dpt.write(',')
    f_tm_in_dpt.write('\n')
    i += 1
f_tm_in_dpt.close()
print 'Team in Department文件已经写入完毕...\n'

for ele in Short_Record_lst:
    print ele, '\n'

sys.exit()








