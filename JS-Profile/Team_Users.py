# coding:utf-8
# 本脚本用于统计CERT-0-07中各个团队中用户的分布
# 每个部门中属于Free-tm的用户不予考虑

import sys

print '团队用户统计开始...\n'
f_cert = open(r'CERT4.2-2009-12.csv', 'r')
# f_cert = open(r'2010-07.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()
print '文件读入完毕...\n'

print '先统计团队名称...\n'
Team_Users_lst = []
Team_Nm_lst = []
# 原始数据基本格式：
# employee_name,user_id,email,role,projects,business_unit,functional_unit,department,team,supervisor
for line in f_cert_lst:
    line_lst = line.strip('\n').strip(',').split(',')
    if 'user_id' == line_lst[1]:
        print '标题行，跳过...\n'
        continue
    if len(line_lst) == 9:
        # 正常记录
        Dpt_tmp = []
        # 按顺序；拼接成标准团队名称
        Dpt_tmp.append(line_lst[4])
        Dpt_tmp.append(line_lst[5])
        Dpt_tmp.append(line_lst[6])
        Dpt_tmp.append(line_lst[7])
        # 没有空部门，但是有空团队
        if Dpt_tmp not in Team_Nm_lst:
            if line_lst[-2] != '':  # 不记录空团队
                Team_Nm_lst.append(Dpt_tmp)
                continue
    if len(line_lst) == 8:
        if line_lst[-1] != '':
            Dpt_tmp = []
            Dpt_tmp.append(line_lst[4])
            Dpt_tmp.append(line_lst[5])
            Dpt_tmp.append(line_lst[6])
            Dpt_tmp.append(line_lst[7])
            if Dpt_tmp not in Team_Nm_lst:
                Team_Nm_lst.append(Dpt_tmp)
                continue
print '团队名称统计完毕...\n'
print '总共有 ', len(Team_Nm_lst), '\n'
Team_Nm_lst.sort()

Leader_lst = []
for team in Team_Nm_lst:
    Team_users_tmp = []
    Leader_tmp = []
    # 原始数据基本格式：
    # employee_name,user_id,email,role,projects,business_unit,functional_unit,department,team,supervisor
    # CERT4.2中没有Projects字段：
    # employee_name,user_id,email,role,business_unit,functional_unit,department,team,supervisor
    for line in f_cert_lst[0:-1]:
        line_lst = line.strip('\n').strip(',').split(',')
        # print 'line_lst is ', line_lst, '\n'
        #if len(line_lst) == 10:
        if len(line_lst) == 9:
            Dpt_tmp = []
            Dpt_tmp.append(line_lst[4])
            Dpt_tmp.append(line_lst[5])
            Dpt_tmp.append(line_lst[6])
            Dpt_tmp.append(line_lst[7])
            if line_lst[-2] != '' and Dpt_tmp == team:
                Team_users_tmp.append(line_lst[1])
                Leader_tmp.append(line_lst[-1]) # 有重复的写入领导列表，便于后期计算次数以决定到底谁是领导者
                continue
        if len(line_lst) == 8:
            Dpt_tmp = []
            Dpt_tmp.append(line_lst[4])
            Dpt_tmp.append(line_lst[5])
            Dpt_tmp.append(line_lst[6])
            Dpt_tmp.append(line_lst[7])
            if line_lst[-1] != '' and Dpt_tmp == team:
                Team_users_tmp.append(line_lst[1])
                # 此时无领导者
                continue
        # 当有多个领导者时，选择最多的那个作为领导
        # 由于团队中可能领导的领导也在列表中，然而团队中只有领导一人的领导不同，因而可以直接计算领导列表中各项的次数
        # 选取最大的即可
    # print 'Leader_tmp is ', Leader_tmp, '\n'
    Leader_set = set(Leader_tmp)
    print 'team is', team, '\n'
    Cnt_lst = [0] * len(Leader_set)
    i = 0
    while i < len(Leader_set):
        Cnt_lst[i] = Leader_tmp.count(list(Leader_set)[i])
        # print 'Cnt_lst[i] is ', Cnt_lst[i], '\n'
        i += 1
    leader = list(Leader_set)[Cnt_lst.index(max(Cnt_lst))]
    print 'leader is ', leader, '\n'
    Leader_lst.append(leader)
    print 'Team_users_tmp is ', Team_users_tmp, '\n'
    Team_Users_lst.append(Team_users_tmp)
print '团队用户统计完成，开始写入文件...\n'

print '写入文件...\n'
f_team_usr = open(r'CERT4.2-2009-12-New-TeamUsers.csv', 'w')
i = 0
while i < len(Team_Nm_lst):
    f_team_usr.write(str(Team_Nm_lst[i]).replace(',', '-'))
    f_team_usr.write(',')
    f_team_usr.write(Leader_lst[i])
    f_team_usr.write(',')
    for user in Team_Users_lst[i]:
        f_team_usr.write(str(user))
        f_team_usr.write(',')
    f_team_usr.write(str(len(Team_Users_lst[i])))
    f_team_usr.write('\n')
    i += 1
print '文件写入完毕...\n'
f_team_usr.close()

sys.exit()






