# coding:utf-8
import sys

f_cert = open(r'2010-07.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()

New_Dpt = []
for line in f_cert_lst:
# employee_name,user_id,email,role,projects,business_unit,functional_unit,department,team,supervisor
    line_lst = line.strip('\n').strip(',').split(',')
    if line_lst[1] == 'user_id':
        continue
    if len(line_lst) < 9:
        continue
    New_Dpt_tmp = []
    New_Dpt_tmp.append(line_lst[5])
    New_Dpt_tmp.append(line_lst[6])
    New_Dpt_tmp.append(line_lst[7])
    if New_Dpt_tmp not in New_Dpt:
        New_Dpt.append(New_Dpt_tmp)
    continue
New_Dpt.sort()
for one in New_Dpt:
    print one, '\n'
for one in New_Dpt:
    for other in New_Dpt:
        if one != other:
            if one[2] == other[2]:
                print 'one is ', one, '\n'
                print 'other is ', other, '\n'
                continue


sys.exit()



