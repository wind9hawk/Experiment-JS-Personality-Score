# coding:utf-8
# 本脚本单独依靠现有的人格特征与满意度研究，进行满意度分数研究排名，查看三个满意度相关用户的排名
# 即如果要包含3个内部不满用户，需要最少考虑识别多少用户
# 读入初始的psychometric文件，并计算其基于Big-5的满意度分数

import sys
import os

import numpy as np
# employee_name,user_id,O,C,E,A,N
# Nicholas Fletcher Pruitt,NFP2441,34,39,38,36,21
# JS: A-0.31, C-0.22, N:-0.23, E-0.08, O-0.08
def JS_Cal(line, Users):
    line_lst = line.strip('\n').strip(',').split(',')
    if line_lst[1] == 'user_id':
        return 0
    Users.append(line_lst[1])
    JS_tmp = []
    JS_tmp.append(line_lst[1])
    JS_Score = float(line_lst[2]) * 0.08 + float(line_lst[3]) * 0.22 + float(line_lst[4]) * 0.08 + float(line_lst[5]) * 0.31 + float(line_lst[6]) * (-0.23)
    JS_tmp.append(JS_Score)
    # print JS_tmp, '\n'
    return JS_tmp

f_psy = open(r'psychometric.csv')
f_psy_lst = f_psy.readlines()
f_psy.close()

JS_lst = []
Users = []
print f_psy_lst[1], '\n'
for line in f_psy_lst:
    if JS_Cal(line, Users) == 0:
        continue
    JS_lst.append(JS_Cal(line, Users))
# print JS_lst[:10], '\n'

JS_sort_lst  = sorted(JS_lst, key=lambda js: js[1])
print JS_sort_lst[:5], '\n'
f_JS_Big5 = open(r'CERT6.2-2009-12-JS-Big5.csv', 'w')
for line in JS_sort_lst:
    f_JS_Big5.write(line[0])
    f_JS_Big5.write(',')
    f_JS_Big5.write(str(line[1]))
    f_JS_Big5.write('\n')

sys.exit()
