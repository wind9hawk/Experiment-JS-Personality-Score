# coding:utf-8
# 本脚本主要对于CERT中的用户初始psychometric文件中的OCEAN分数进行初步统计，以发现规律

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

def Draw(f_array, index_x, index_y): # index_x与index_y为记录中对应特征的下标，比index_lst的下标多1
    traits_lst = ['O', 'C', 'E', 'A', 'N']
    insiders_lst = ['ACM2278', 'CMP2946', 'PLJ1771', 'CDE1846', 'MBG3183']
    # Psychometric.csv文件中位置： ACM2278:2842，CMP2946：2332，PLJ1771：1284，CDE1846：656，MBG3183：1496
    # 因为计算psy_lst时跳过了第一行字段说明，故总共4000行，在原有文件基础上应再减去一行，即再-1
    plt.xlabel(traits_lst[index_x - 1])
    plt.ylabel(traits_lst[index_y - 1])
    plt.plot(f_array[:, index_x - 1], f_array[:, index_y - 1], 'go')
    plt.plot(f_array[2840, index_x - 1], f_array[2840, index_y - 1], 'bo', label='ACM2278')
    plt.plot(f_array[2330, index_x - 1], f_array[2330, index_y - 1], 'r^', label='CMP2946')
    plt.plot(f_array[1282, index_x - 1], f_array[1282, index_y - 1], 'ro', label='PLJ1771')
    plt.plot(f_array[654, index_x - 1], f_array[654, index_y - 1], 'b^', label='CDE1846')
    plt.plot(f_array[1494, index_x - 1], f_array[1494, index_y - 1], 'rs', label='MBG3183')
    plt.legend(loc = 'upper left')
    # plt.legend(loc = 'left')
    plt.show()

print '统计psychometric文件中大五人格分数...\n'
# 文件基本格式：
# employee_name,user_id,O,C,E,A,N
# Nicholas Fletcher Pruitt,NFP2441,34,39,38,36,21
f_psy = open(r'S:\内部威胁\数据集\Cert-Data\CERT_Result\Experiment\Experiment-JS-Personality-Score\JS-Profile\psychometric.csv'.decode('utf-8'), 'r')
f_psy_lst = f_psy.readlines()
f_psy.close()
print 'psychometric文件读入完毕...\n'

print '开始转化记录为分段列表...\n'
psy_lst = []
for line in f_psy_lst:
    psy_lst_tmp = []
    line_lst = line.strip('\n').strip(',').split(',')
    if 'user_id' in line_lst[1]:
        continue
    i = 2
    while i < len(line_lst):
        psy_lst_tmp.append(float(line_lst[i]))
        i += 1
    psy_lst.append(psy_lst_tmp)
print 'psychmetric list has been built...\n'
# print len(psy_lst), '\n'

print '开始依次绘图...\n'
print '首先是原始数据分布...\n'
# OCEAN
psy_array = np.array(psy_lst)
# 对psy_array 标准化
psy_array_std = preprocessing.scale(psy_array)
Draw(psy_array_std, 4, 5)
print '绘图完毕...\n'
sys.exit()
