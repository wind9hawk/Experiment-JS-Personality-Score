# coding:utf-8
# 本脚本用于绘制用户分布图：
# 基于CERT-2009-12的全部用户图，以及风险用户图分别绘制分布
# 横坐标为用户user_id
# 纵坐标为满意度分数（0-5）

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from sklearn import preprocessing
import sys

f_Cert = open(r'CERT6.2-2009-12-5JS-Label-0.2 -accepted.csv', 'r')
f_cert_lst = f_Cert.readlines()
f_Cert.close()
f_risk = open(r'CERT6.2-2009-12-High Risk-0.1.csv', 'r')
f_risk_lst = f_risk.readlines()
f_risk.close()

# 开始建立初始全部用户的5JS标签值（其中1的个数）
# NFP2441,0,1,1,0,1,3,7
Users_JS = []
for line in f_cert_lst:
    line_lst = line.strip('\n').strip(',').split(',')
    user_js = []
    user_js.append(line_lst[0])
    user_js.append(float(line_lst[6]))
    Users_JS.append(user_js)

JS_lst = []  # 存储全部用户的1的个数
for line in Users_JS:
    JS_lst.append(line[1])

Users_Risk = []
for line in f_risk_lst:
    line_lst = line.strip('\n').strip(',').split(',')
    # BTR2026,-3.9465461889
    Users_Risk.append(line_lst[0])

# 1. 高危用户user_id列表（红色实心圆）
# 2. 剩余用户user_id列表（蓝色x）
# 3. OCSVM时选取的较高的3200个用户颜色（绿色实心圆）

Users_JS_sort = sorted(Users_JS, key=lambda js:js[1])
print Users_JS_sort[:5], '\n'

# 开始对每个点绘图
plt.xlabel('User_No')
plt.ylabel('5JS')
flag_HR = 0
flag_OCSVM = 0
flag_Nomaal = 0
i = 0
while i < len(Users_JS_sort):
    if Users_JS_sort[i][0] in Users_Risk:
        if flag_HR == 0:
            plt.plot(i + 1, Users_JS_sort[i][1], 'ro', label='High Risk')
            i += 1
            flag_HR += 1
            continue
        else:
            plt.plot(i + 1, Users_JS_sort[i][1], 'ro')
            i += 1
            continue
    else:
        if i >= 1800:
            if flag_OCSVM == 0:
                plt.plot(i + 1, Users_JS_sort[i][1], 'go', label='OCSVM_Train')
                i += 1
                flag_OCSVM += 1
                continue
            else:
                plt.plot(i + 1, Users_JS_sort[i][1], 'go')
                i += 1
                continue
        else:
            if flag_Nomaal == 0:
                plt.plot(i + 1, Users_JS_sort[i][1], 'bx', Label='Low but Normal')
                i += 1
                flag_Nomaal += 1
                continue
            else:
                plt.plot(i + 1, Users_JS_sort[i][1], 'bx')
                i += 1
                continue
plt.legend()
plt.show()
print 'Drow done...\n'
sys.exit()
# plt.xlabel(index_lst[index_x - 1])
# plt.ylabel(index_lst[index_y - 1])
plt.xlabel('5JS-Label')
plt.ylabel('User_No')
plt.plot(f_array[:, index_x - 1], f_array[:, index_y - 1], 'bo')
plt.plot(f_array[2643, index_x - 1], f_array[2643, index_y - 1], 'g^', label='ACM2278')
plt.plot(f_array[2174, index_x - 1], f_array[2174, index_y - 1], 'r^', label='CMP2946')
plt.plot(f_array[1187, index_x - 1], f_array[1187, index_y - 1], 'ro', label='PLJ1771')
plt.plot(f_array[603, index_x - 1], f_array[603, index_y - 1], 'rx', label='CDE1846')
plt.plot(f_array[1389, index_x - 1], f_array[1389, index_y - 1], 'rs', label='MBG3183')
plt.legend(loc = 'upper left')
plt.show()
