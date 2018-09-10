# coding:utf-8
# 本脚本主要用于分析比较CERT中用户的Department与Team间的关系，从现有数据分析，不同的Department下包含几乎相同的Team；
# 此外，本脚本还要分析supervisor同用户、Department以及Team间的关系
# 为此，首先任意选择一个Department与其包含的Team，计算同时具有上述两个团队属性的用户集合，与单独计算的Team用户集合比较，以验证
# Department与Team间的关系
# 第二步，按一个Supervisor统计所有属于该Supervisor的用户，与Team进行比较，判断是否该Supervisor与Team对应；

# 测试用例：
# Department: 5 - Security
# Team: 8 - ElectronicSecurity
# Supervisor: Madison Charissa Malone
# Team(User):
# 8 - ElectronicSecurity,
# Supervisor: MCM2375,
# NFP2441,LRK2426,BPD2437,GCP2425,JPS2432,CBW2427,
# KAP2430,RMO2439,PRH2431,DLM2440,RCB2424,CAG2442,ADS2428,RSV2438,MCM2375,YKM2435,KCC2434,SHM2429,
# RIS2436,DXM2433,
# Count:21.


import sys

print '比较分析CERT中部门与团队关系，读入原始数据集2010-07.csv..\n'
f_ldap = open(r'2010-07.csv'.decode('utf-8'), 'r')
f_ldap_lst = f_ldap.readlines()
f_ldap.close()
print '原始数据文件读取完毕...\n'

print '开始统计所属于5 - Security部门同时隶属于4 - AssemblyDept团队的用户...\n'
Department_user_lst = []
Team_lst = []
# Team_P_lst = []
# Team_M_lst = []
Leader_user_lst = []
Department_lst = []
Short_Rcd_lst = []
# 原始数据基本格式：
# employee_name,user_id,email,role,projects,business_unit,functional_unit,department,team,supervisor
for line in f_ldap_lst:
    line_lst = line.strip('\n').strip(',').split(',')
    if len(line_lst) < 10:
        Short_Rcd_lst.append(line_lst)
        continue
    # if '4 - AssemblyDept' in line_lst:
        # print line_lst, '\n'
    if 'department' not in line_lst[-3] and line_lst[-3] not in Department_lst:
        if line_lst[-3] == '':
            if 'Free-dpt' not in Department_lst:
                Department_lst.append('Free-dpt')
        else:
            Department_lst.append(line_lst[-3])
    if line_lst[-2] not in Team_lst and 'team' not in line_lst[-2]:
        if line_lst[-2] == '':
            if 'Free-tm' not in Team_lst:
                Team_lst.append('Free-tm')
        else:
            Team_lst.append(line_lst[-2])
    if line_lst[-2] == '' or line_lst[-3] == '':
        if line_lst not in Short_Rcd_lst:
            # continue
            Short_Rcd_lst.append(line_lst)

    # if '5 - Security' in line_lst[-3] and '4 - AssemblyDept' in line_lst[-2]:
        # Department_user_lst.append(line_lst[1])
        # Leader_user_lst.append(line_lst[-1])
        # if 'Peter Nicholas Livingston' in line_lst[-1]:
        #     Team_P_lst.append(line_lst[1])
        # if 'Madison Charissa Malone' in line_lst[-1]:
        #     Team_M_lst.append(line_lst[1])
print '同时数据指定部门与团队的用户统计完毕，其结果为...\n'
# print 'Users in Department and Team is ', Department_user_lst, '\t', '总共有 ', len(Department_user_lst), '\n'
# print 'Supervisor is ', set(Leader_user_lst), '\n'
Department_lst.sort()
Team_lst.sort()
print Department_lst, '\n'
f_dpt = open(r'2010-07-Department.csv', 'w')
f_tm = open(r'2010-07-Team.csv', 'w')
f_dpt.write('Department is ')
f_dpt.write('\n')
f_tm.write('Team is ')
f_tm.write('\n')
for ele in Department_lst:
    f_dpt.write(ele)
    f_dpt.write('\n')
for ele in Team_lst:
    f_tm.write(ele)
    f_tm.write('\n')
f_dpt.close()
f_tm.close()
# print 'Team list is ', Team_lst, '\t', len(Team_lst), '\n'
# print 'M lead ', Team_M_lst, '\t', len(Team_M_lst), '\n'
# print 'P lead ', Team_P_lst, '\t', len(Team_P_lst), '\n'
# for ele in Team_lst:
    # print ele, '\n'
# f_dpt = open(r'Department_201007.csv', 'w')
# Department_lst.sort()
# for ele in Department_lst:
    # f_dpt.write(str(ele))
    # f_dpt.write('\n')
# f_dpt.close()
f_Short = open(r'Short-Record.csv', 'w')
f_Short.write('不规范记录')
f_Short.write('\n')
for ele in Short_Rcd_lst:
    for char in ele:
        f_Short.write(char)
        f_Short.write(',')
    f_Short.write('\n')
f_Short.close()

sys.exit()



