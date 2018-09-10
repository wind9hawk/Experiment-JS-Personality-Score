# coding:utf-8
# 本脚本主要根据提取的JS特征文件，计算每个用户的JS分数；
# 每个用户的JSS分数保存格式为[user_id, Personality_Score, CPBs_Score, JSS]
# 所得结果存在在文件CERT6.2-2010-07-JSS.csv

import sys
import numpy as np
import math
from sklearn.preprocessing import scale
from sklearn.preprocessing import MinMaxScaler

print '计算每个用户的JSS分数...\n'
print '提取原始JS特征数据...\n'
f_cert = open(r'2010-07-18JS.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()
print '原始数据提取完毕...\n'

print '开始分隔原始数据列表...\n'
JS_users_lst = []  # 存储用户的JSS分数
Users_lst = []  # 存储user_id
# user_id,O_Score,C_Score,E_Score,A_Score,N_Score,
# Team_CPB-I-mean,Team_CPB-O-mean,Users-less-mean-A,Users-less-AC, Users-less-mean-C, Team_CPB-I-median,Team_CPB-O-median,
# Dpt-CPB-I-mean,Dpt_CPB-O-mean,Dpt_CPB-I-median,Dpt_CPB-O-median,
# Leader_CPB-I,Leader_CPB-O
for line in f_cert_lst:
    JS_user_tmp = [] # 用于存储用户的JS特征
    line_lst = line.strip('\n').strip(',').split(',')
    print line_lst, '\n'
    if line_lst[0] == 'user_id':
        continue
    Users_lst.append(line_lst[0])
    i = 1
    print len(line_lst), '\n'
    while i < len(line_lst):
        # 开始先不统计低于Ａ与Ｃ均值的用户数量
        # if i == 8 or i == 9:
            # i += 1
            # continue
        # if i == 10 or i == 11: # 略过了中位数
        #     i += 1
        #     continue
        # if i == 14 or i == 15: # 略过了部门的中位数
        #     i += 1
        #     continue
        JS_user_tmp.append(float(line_lst[i]))
        i += 1
    JS_users_lst.append(JS_user_tmp)
print '数据分隔完成...\t开始计算JSS分数\n'
print '数据示例： ', JS_users_lst[1], '\n'

print 'JSS基本分数计算...\n'
# 根据2002的研究结果，OCEAN与JS的关联度为：
# N:-0.29, E:0.25, O:0.02, A:0.17, C:0.26;
# 或者根据CERT参考的文章的数据：
# A：0.31, C:0.22, -N:0.23, E:0.08, O:0.08
# JS特征中的顺序为OCEAN
# 为了体现用户间的区别，在计算JSS前对特征进行了列标准化
# JS_users_lst = scale(JS_users_lst, axis=0)
# JS_users_nor_lst = MinMaxScaler().fit_transform(JS_users_lst)
# JS_users_lst = MinMaxScaler().fit_transform(JS_users_lst)
# JSS-Basic和JSS-Env分别计算，JSS-Env又分为团队-部门-领导者三项，初始赋予权重为0.5，0.2，0.3
JSS_users_lst = []
JSS_Evn_lst = [] #用于存储全局的JSS_Env变量，以进行归一化
i = 0
while i < len(JS_users_lst):
    # JSS_user_tmp = [] # 用于存储用户的JSS分数
    # JSS_user_tmp.append(Users_lst[i]) # 写入第一个字段用户id
    # 首先计算OCEAN的基本分数
    # O_Score,C_Score,E_Score,A_Score,N_Score,
    # 首先根据2002年的数据计算
    # JSS_Basic = 0.02 * JS_users_lst[i][0] + 0.26 * JS_users_lst[i][1] + 0.25 * JS_users_lst[i][2] + 0.17 * JS_users_lst[i][3] + (-0.29) * JS_users_lst[i][4]
    # 根据CERT的参考文献计算
    # JSS_Basic = 0.08 * JS_users_lst[i][0] + 0.22 * JS_users_lst[i][1] + 0.08 * JS_users_lst[i][2] + 0.31 * JS_users_lst[i][3] + (-0.23) * JS_users_lst[i][4]
    JSS_Basic = JS_users_lst[i][0] + JS_users_lst[i][1] + JS_users_lst[i][2] + JS_users_lst[i][3] - JS_users_lst[i][4]
    # JSS_Basic = 0.08 * JS_users_lst[i][0] * (0.22 * JS_users_lst[i][1]) * (0.08 * JS_users_lst[i][2]) * (0.31 * JS_users_lst[i][3]) * ((-0.23) * JS_users_lst[i][4]
    print Users_lst[i], 'JSS基本分数计算完毕...\nt', JSS_Basic, '\n'
    # 首先计算团队的CPB-I与CPB-O影响
    w1 = 1
    w2 = 1
    w3 = 1
    # Team_CPB-I-mean * Users-less-mean-A
    JSS_team_CPB_I = JS_users_lst[i][5] * JS_users_lst[i][7]
    # Team_CPB-O-mean * Users-less-mean-A and C
    JSS_team_CPB_O = JS_users_lst[i][6] * JS_users_lst[i][8]
    JSS_dpt_CPBs = JS_users_lst[i][12] + JS_users_lst[i][13]
    JSS_Leader_CPBs = JS_users_lst[i][-1] + JS_users_lst[i][-2]
    JSS_Env = w1 * (JSS_team_CPB_I + JSS_team_CPB_O) + w2 * JSS_dpt_CPBs + w3 * JSS_Leader_CPBs
    JSS_Evn_lst.append(JSS_Env)
    i += 1
    continue
    # 计算环境影响因子
    # CPB_sum = 0.0
    # CPB_norm = 0.0
    # j = 5
    # while j < len(JS_users_lst[i]):
        # CPB_sum += JS_users_lst[i][j]
        # CPB_norm += pow(JS_users_lst[i][j], 2)
        # j += 1
    # CPB_norm = np.sqrt(CPB_norm)
    # JSS_Evn = CPB_sum / CPB_norm
    # JSS_Evn = CPB_sum
JS_Env_max_min_lst = MinMaxScaler().fit_transform(JSS_Evn_lst)

i = 0
while i < len(JS_users_lst):
    JSS_user_tmp = [] # 用于存储用户的JSS分数
    JSS_user_tmp.append(Users_lst[i]) # 写入第一个字段用户id
    JSS_Basic = JS_users_lst[i][0] + JS_users_lst[i][1] + JS_users_lst[i][2] + JS_users_lst[i][3] - JS_users_lst[i][4]
    # JSS_Basic = 0.08 * JS_users_lst[i][0] * (0.22 * JS_users_lst[i][1]) * (0.08 * JS_users_lst[i][2]) * (0.31 * JS_users_lst[i][3]) * ((-0.23) * JS_users_lst[i][4]
    print Users_lst[i], 'JSS基本分数计算完毕...\nt', JSS_Basic, '\n'
    JSS_user_tmp.append(JSS_Basic)
    JSS_user_tmp.append(JS_Env_max_min_lst[i])
    JSS = (2 - JS_Env_max_min_lst[i]) * JSS_Basic
    # JSS = JSS_Basic + JSS_Evn
    JSS_user_tmp.append(JSS)
    JSS_users_lst.append(JSS_user_tmp)
    i += 1
# JS_users_nor_lst = MinMaxScaler().fit_transform(JS_users_lst)
print '全部用户的JSS分数计算完毕...\n'
print '示例： ', JSS_users_lst[1], '\n'

print '将结果写入CERT6.2-2010-07-JSS.csv文件...\n'
f_JSS = open(r'CERT6.2-2010-07-JSS-new1-Sort.csv', 'w')
# 先写入标题行
f_JSS.write('user_id')
f_JSS.write(',')
f_JSS.write('JSS_Basic')
f_JSS.write(',')
f_JSS.write('JSS_Evn')
f_JSS.write(',')
f_JSS.write('JSS')
f_JSS.write('\n')
JSS_users_sort_lst = sorted(JSS_users_lst, key=lambda x: x[3], reverse=False)
i = 0
for user in JSS_users_sort_lst:
    for ele in user:
        f_JSS.write(str(ele))
        f_JSS.write(',')
    f_JSS.write('\n')
f_JSS.close()
print '文件写入完毕...\n'

print '单独输出五个攻击者的标准化与归一化数据...\n'
# ACM2278:2535
# CMP2946:71
# PLJ1771:2740
# CDE1846:1256
# MBG3183:1420
sys.exit()

i = 0
while i < len(JS_users_lst):
    if Users_lst[i] == 'ACM2278':
        print Users_lst[i], ':', JS_users_lst[i], '\n'
        print Users_lst[i], ' nor: ', JS_users_nor_lst[i], '\n'
        print Users_lst[i], ' std: ', JS_users_std_lst[i], '\n'
        i += 1
        continue
    if Users_lst[i] == 'CMP2946':
        print Users_lst[i], ':', JS_users_lst[i], '\n'
        print Users_lst[i], ' nor: ', JS_users_nor_lst[i], '\n'
        print Users_lst[i], ' std: ', JS_users_std_lst[i], '\n'
        i += 1
        continue
    if Users_lst[i] == 'PLJ1771':
        print Users_lst[i], ':', JS_users_lst[i], '\n'
        print Users_lst[i], ' nor: ', JS_users_nor_lst[i], '\n'
        print Users_lst[i], ' std: ', JS_users_std_lst[i], '\n'
        i += 1
        continue
    if Users_lst[i] == 'CDE1846':
        print Users_lst[i], ':', JS_users_lst[i], '\n'
        print Users_lst[i], ' nor: ', JS_users_nor_lst[i], '\n'
        print Users_lst[i], ' std: ', JS_users_std_lst[i], '\n'
        i += 1
        continue
    if Users_lst[i] == 'MBG3183':
        print Users_lst[i], ':', JS_users_lst[i], '\n'
        print Users_lst[i], ' nor: ', JS_users_nor_lst[i], '\n'
        print Users_lst[i], ' std: ', JS_users_std_lst[i], '\n'
        i += 1
        continue
    i += 1
sys.exit()





