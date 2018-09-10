# coding:utf-8
# 本脚本根据Department作为指标统计每个部门中的用户列表
# 为了简便考虑，部门中不再考虑领导的影响，因为我们这里主要通过CPBs来建模工作满意度，
# 因此与部门角色、福利待遇等影响不大，更多是日常学习工作的互动交流影响

import sys

print '读入原始的CERT-2010-07.csv文件...\n'
f_cert = open(r'CERT4.2-2009-12.csv', 'r')
# f_cert = open(r'2010-07.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()
print '原始数据读入完毕...\n'

print '开始统计得到部门列表...\n'
# 原始数据基本格式：
# employee_name,user_id,email,role,projects,business_unit,functional_unit,department,team,supervisor
# CERT4.2中
# employee_name,user_id,email,role,business_unit,functional_unit,department,team,supervisor
Department_lst = []
for line in f_cert_lst:
    line_lst = line.strip('\n').strip(',').split(',')
    if 'user_id' in line_lst[1]:
        print '这是标题行，跳过...\n'
        continue
    if len(line_lst) == 9:
        if line_lst[-3] == '': # 不统计空部门
            continue
        Dpt_tmp = []
        Dpt_tmp.append(line_lst[4])
        Dpt_tmp.append(line_lst[5])
        Dpt_tmp.append(line_lst[6])
        if Dpt_tmp not in Department_lst:
            Department_lst.append(Dpt_tmp)
            continue
    if len(line_lst) == 8:
        # print '长度为8的记录为： ', line_lst, '\n'
        # sys.exit()
        if line_lst[-2] == '':
            continue
        Dpt_tmp = []
        Dpt_tmp.append(line_lst[4])
        Dpt_tmp.append(line_lst[5])
        Dpt_tmp.append(line_lst[6])
        if Dpt_tmp not in Department_lst:
            Department_lst.append(Dpt_tmp)
            continue
Department_lst.sort()
for one in Department_lst:
    print one, '\n'
print len(Department_lst), '\n'
# sys.exit()
# 去掉空部门后应当有22个部门
print '部门列表统计完毕...\t', len(Department_lst), '\n'

print '开始根据部门统计每个部门的用户...\n'
Department_Users = []
for dpt in Department_lst:
    Department_Users_tmp = []
    for line in f_cert_lst:
        line_lst = line.strip('\n').strip(',').split(',')
        if line_lst[1] == 'user_id':
            continue
        if len(line_lst) == 9:
            Dpt_tmp = []
            Dpt_tmp.append(line_lst[4])
            Dpt_tmp.append(line_lst[5])
            Dpt_tmp.append(line_lst[6])
            if Dpt_tmp == dpt:
                if line_lst[1] not in Department_Users_tmp:
                    Department_Users_tmp.append(line_lst[1])
                    continue
        else:
            if len(line_lst) == 8:
                Dpt_tmp = []
                Dpt_tmp.append(line_lst[4])
                Dpt_tmp.append(line_lst[5])
                Dpt_tmp.append(line_lst[6])
                if Dpt_tmp == dpt:
                    if line_lst[1] not in Department_Users_tmp:
                        Department_Users_tmp.append(line_lst[1])
                        continue
    Department_Users_tmp.sort()
    Department_Users.append(Department_Users_tmp)
print '部门用户统计完毕...\n'

print '开始写入Department_Users信息...\n'
f_dpt_users = open(r'CERT4.2-2009-12-New-DptUsers.csv', 'w')
i = 0
while i < len(Department_lst):
    f_dpt_users.write(str(Department_lst[i]).replace(',', '-'))
    f_dpt_users.write(',')
    for ele in Department_Users[i]:
        f_dpt_users.write(ele)
        f_dpt_users.write(',')
    f_dpt_users.write(str(len(Department_Users[i])))
    f_dpt_users.write('\n')
    i += 1
print '部门用户信息写入完毕...\n'
f_dpt_users.close()

sys.exit()
