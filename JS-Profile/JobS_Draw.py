# coding:utf-8
# 本脚本开始处理得到的用户5维Job Satisfaction特征
# 作图绘制2个维度的二维图
# 运用K均值聚类分析

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from sklearn import preprocessing
import sys

# 定位函数，给定一个任意User_id和指定的记录，返回其所在的记录行
def Locate_User(f_0_lst, user):
    for line in f_0_lst:
        # line_0_lst = line.strip('\n').strip(',').split(',')
        if line_0_lst[0] == user:
            return line_0_lst
        else:
            continue
    return None

# 定义一个绘图函数，输入任意两个维度以及指定的数据集，以此绘图
def Draw(f_array, index_x, index_y): # index_x与index_y为记录中对应特征的下标，比index_lst的下标多1
    index_lst = ['C', 'A', 'N', 'T-CPB-I', 'T-CPB-O', 'T-CPB-I-median', 'T-CPT-O-median', 'Low_C', 'Low_A', 'High_N']
    insiders_lst = ['ACM2278', 'CMP2946', 'PLJ1771', 'CDE1846', 'MBG3183']
    # 2010-07-17JS.csv中：ACM2278:2753， CMP2946：2262，PLJ1771：1244， CDE1846：633， MBG3183：1453
    # CAN文件中位置： ACM2278:2644，CMP2946：2175，PLJ1771：1188，CDE1846：604，MBG3183：1390
    plt.xlabel(index_lst[index_x - 1])
    plt.ylabel(index_lst[index_y - 1])
    plt.plot(f_array[:, index_x - 1], f_array[:, index_y - 1], 'bo')
    plt.plot(f_array[2643, index_x - 1], f_array[2643, index_y - 1], 'g^', label='ACM2278')
    plt.plot(f_array[2174, index_x - 1], f_array[2174, index_y - 1], 'r^', label='CMP2946')
    plt.plot(f_array[1187, index_x - 1], f_array[1187, index_y - 1], 'ro', label='PLJ1771')
    plt.plot(f_array[603, index_x - 1], f_array[603, index_y - 1], 'rx', label='CDE1846')
    plt.plot(f_array[1389, index_x - 1], f_array[1389, index_y - 1], 'rs', label='MBG3183')
    # f_array_mean = f_array.mean(axis=0) # 依次是CAN的均值
    # print f_array_mean,'\n'
    # 　f_array_new = []
    #for one in f_array:
        #　f_array_new.append(np.concatenate((one, f_array_mean), axis=0))
    # f_array = np.array(f_array_new)
    # print 'New array with mean value is ', f_array[0], '\n'
    # plt.plot(f_array[:, index_x - 1 + 5], 'g--', label = 'x-mean-value')
    # plt.plot(f_array[:, index_y - 1 + 5], 'g-', label = 'y-mean-value')
    # plt.plot(n_len, f_array_mean[index_x - 1], 'g-', label = 'mean_x')
    # plt.plot(n_len, f_array_mean[index_y - 1], 'b-', label = 'mean_y')
    # plt.plot(File_array_mean, 'b-', label='Mean of features')
    # plt.plot(File_array[1], 'g-', File_array[2], 'g--', label='Normal users')
    plt.legend(loc = 'upper left')
    # plt.legend(loc = 'left')
    plt.show()


print '5-JS-Feature Analysis...\n'

# f = open(r'S:\内部威胁\数据集\Cert-Data\CERT_Result\Experiment\Experiment-FMM-JobSatisfaction\2010-07-User-5JS.csv'.decode('utf-8'), 'r')
# f = open(r'S:\内部威胁\数据集\Cert-Data\CERT_Result\Experiment\Experiment-FMM-JobSatisfaction\2010-07-User-5JS-Model-CAN-median.csv'.decode('utf-8'), 'r')
# f = open(r'S:\内部威胁\数据集\Cert-Data\CERT_Result\Experiment\Experiment-FMM-JobSatisfaction\2010-07-User-5JS-Model-CAN-sum.csv'.decode('utf-8'), 'r')
# f = open(r'S:\内部威胁\数据集\Cert-Data\CERT_Result\Experiment\Experiment-FMM-JobSatisfaction\2010-07-User-5JS-Model-CAN-Low-mean.csv'.decode('utf-8'), 'r')
#f = open(r'S:\内部威胁\数据集\Cert-Data\CERT_Result\Experiment\Experiment-FMM-JobSatisfaction\2010-07-User-5JS-Model-median.csv'.decode('utf-8'), 'r')
f = open(r'2010-07-17JS.csv', 'r')
f_lst = f.readlines()
f.close()
print 'f_lst is ', len(f_lst), '\t', f_lst,'\n'
print '2010-07-User-5JS.csv读取完毕...\n'

# 从原始数据中剔除user_id，得到可以直接计算绘图的数值数组

JS_Feat = []
for user_line in f_lst:
    JS_Feat_tmp = []
    user_line_lst = user_line.strip('\n').strip(',').split(',')
    if user_line_lst[0] == 'user_id':
        continue
    print 'user_line_lst is ', user_line_lst, '\n'
    i = 1
    while i < len(user_line_lst):
        print 'user_line_lst is ', user_line_lst, '\n'
        JS_Feat_tmp.append(float(user_line_lst[i]))
        i += 1
    JS_Feat.append(JS_Feat_tmp)
print 'JS_Feat[] has been built...\n'
print 'JS_Feat[] is ', JS_Feat, '\n'
JS_Feat_array = np.array(JS_Feat)
# JS_Feat_Scale = np.array(JS_Feat)
JS_Feat_Scale = preprocessing.scale(JS_Feat_array)

print '开始绘制二维图，需要指定x-y轴...\n'
Draw(JS_Feat_Scale, 1, 6)
sys.exc_clear()

