# coding:utf-8
# 本脚本主要针对得到的PCA（2）-KM（5）的聚类结果进一步分析其稀疏度，从而发现那个群簇包含恶意用户， 以与异常检测结合；

import numpy as np
import sys

def GoLine(file):
    f_lst = []
    for line in file:
        f_lst_tmp = []
        line_lst = line.strip('\n').strip(',').split(',')
        f_lst_tmp.append(float(line_lst[1]))
        f_lst_tmp.append(float(line_lst[2]))
        f_lst.append(f_lst_tmp)
    return f_lst


print '读入5个群簇结果文件...\n'

f_km_0 = open(r'KM-5_0.csv', 'r')
f_km_1 = open(r'KM-5_1.csv', 'r')
f_km_2 = open(r'KM-5_2.csv', 'r')
f_km_3 = open(r'KM-5_3.csv', 'r')
f_km_4 = open(r'KM-5_4.csv', 'r')

f_km_0_lst = GoLine(f_km_0.readlines())
f_km_1_lst = GoLine(f_km_1.readlines())
f_km_2_lst = GoLine(f_km_2.readlines())
f_km_3_lst = GoLine(f_km_3.readlines())
f_km_4_lst = GoLine(f_km_4.readlines())

f_km_1.close()
f_km_2.close()
f_km_3.close()
f_km_4.close()
f_km_0.close()

print 'KM结果文件读入完毕...\n'

print '计算每个群簇的均值、标准差...\n'


f_km_0_array = np.array(f_km_0_lst)
f_km_1_array = np.array(f_km_1_lst)
f_km_2_array = np.array(f_km_2_lst)
f_km_3_array = np.array(f_km_3_lst)
f_km_4_array = np.array(f_km_4_lst)

f_0_mean = f_km_0_array.mean(axis=0)
f_1_mean = f_km_1_array.mean(axis=0)
f_2_mean = f_km_2_array.mean(axis=0)
f_3_mean = f_km_3_array.mean(axis=0)
f_4_mean = f_km_4_array.mean(axis=0)

f_0_std = f_km_0_array.std(axis=0)
f_1_std = f_km_1_array.std(axis=0)
f_2_std = f_km_2_array.std(axis=0)
f_3_std = f_km_3_array.std(axis=0)
f_4_std = f_km_4_array.std(axis=0)

print '每个群簇的均值与标准差为...\n'
print 'f_0 is ', f_0_mean, '\t', f_0_std, '\t', np.square(f_0_std[0]) + np.square(f_0_std[1]), '\t', np.square(f_0_std.sum()), '\t', f_0_std[0] * f_0_std[1], '\n'
print 'f_1 is ', f_1_mean, '\t', f_1_std, '\t', np.square(f_1_std[0]) + np.square(f_1_std[1]), '\t', np.square(f_1_std.sum()), '\t', f_1_std[0] * f_1_std[1], '\n'
print 'f_2 is ', f_2_mean, '\t', f_2_std, '\t', np.square(f_2_std[0]) + np.square(f_2_std[1]), '\t', np.square(f_2_std.sum()), '\t', f_2_std[0] * f_2_std[1], '\n'
print 'f_3 is ', f_3_mean, '\t', f_3_std, '\t', np.square(f_3_std[0]) + np.square(f_3_std[1]), '\t', np.square(f_3_std.sum()), '\t', f_3_std[0] * f_3_std[1], '\n'
print 'f_4 is ', f_4_mean, '\t', f_4_std, '\t', np.square(f_4_std[0]) + np.square(f_4_std[1]), '\t', np.square(f_4_std.sum()), '\t', f_4_std[0] * f_4_std[1], '\n'

print '继续分析每个群簇的平均间距...\n'

Distance_sum = []

sum_0 = 0.0
for line in f_km_0_array[0:2]:
    # sum_tmp = []
    for oppo in f_km_0_array:
        print line[0], '-', oppo[0], '\n'
        print line[1], '-', oppo[1], '\n'
        sum_0 += np.sqrt(np.square(line[0] - oppo[0]) + np.square(line[1] - oppo[1]))
sum_mean = []
sum_mean.append(sum_0/2.0)
sum_mean.append(sum_0/2.0/len(f_km_0_array))
Distance_sum.append(sum_mean)

sum_0 = 0.0
for line in f_km_1_array[0:2]:
    # sum_tmp = []
    for oppo in f_km_1_array:
        sum_0 += np.sqrt(np.square(line[0] - oppo[0]) + np.square(line[1] - oppo[1]))
sum_mean = []
sum_mean.append(sum_0/2.0)
sum_mean.append(sum_0/2.0/len(f_km_1_array))
Distance_sum.append(sum_mean)

sum_0 = 0.0
for line in f_km_2_array[0:2]:
    # sum_tmp = []
    for oppo in f_km_2_array:
        sum_0 += np.sqrt(np.square(line[0] - oppo[0]) + np.square(line[1] - oppo[1]))
sum_mean = []
sum_mean.append(sum_0/2.0)
sum_mean.append(sum_0/2.0/len(f_km_2_array))
Distance_sum.append(sum_mean)

sum_0 = 0.0
for line in f_km_3_array[0:2]:
    # sum_tmp = []
    for oppo in f_km_3_array:
        sum_0 += np.sqrt(np.square(line[0] - oppo[0]) + np.square(line[1] - oppo[1]))
sum_mean = []
sum_mean.append(sum_0/2.0)
sum_mean.append(sum_0/2.0/len(f_km_3_array))
Distance_sum.append(sum_mean)

sum_0 = 0.0
for line in f_km_4_array[0:2]:
    # sum_tmp = []
    for oppo in f_km_4_array:
        sum_0 += np.sqrt(np.square(line[0] - oppo[0]) + np.square(line[1] - oppo[1]))
sum_mean = []
sum_mean.append(sum_0/2.0)
sum_mean.append(sum_0/2.0/len(f_km_4_array))
Distance_sum.append(sum_mean)

for one in Distance_sum:
    print 'f_n distance is ', one[0], '\t', one[1], '\n'
print len(f_km_0_array), '\n'
print len(f_km_1_array), '\n'
print len(f_km_2_array), '\n'
print len(f_km_3_array), '\n'
print len(f_km_4_array), '\n'
sys.exit()
