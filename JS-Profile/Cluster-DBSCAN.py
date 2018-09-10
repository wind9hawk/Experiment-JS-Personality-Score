# coding:utf-8
# 本脚本针对得到的15-JS特征数据进行DBSCAN聚类分析，以验证是否可以聚类成高危用户簇类

import sys
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.decomposition import  PCA


print '开始针对15JS特征使用DBSCAN聚类实验...\n'
print '应分别使用以下几种距离度量：欧式距离 “euclidean”, \n曼哈顿距离 “manhattan”, \n切比雪夫距离“chebyshev”, \n闵可夫斯基距离 “minkowski”, \n带权重闵可夫斯基距离 “wminkowski”, \n标准化欧式距离 “seuclidean”, \n马氏距离“mahalanobis” \n'

print '读入用户的15维JS特征文件...\n'
f_JS = open(r'2010-07-15JS.csv', 'r')
f_JS_lst = f_JS.readlines()
f_JS.close()
print 'JS文件读入完毕...\n'

print '开始使用DBSCAN聚类...\n'
print '处理原始数据为数组...\n'
Users_JS_lst = []
for line in f_JS_lst:
    User_JS_tmp = []
# user_id,O_Score,C_Score,E_Score,A_Score,N_Score,Team_CPB-I-mean,Team_CPB-O-mean,Team_CPB-I-median,Team_CPB-O-median,Dpt-CPB-I-mean,Dpt_CPB-O-mean,Dpt_CPB-I-median,Dpt_CPB-O-median,Leader_CPB-I,Leader_CPB-O
    line_lst = line.strip('\n').strip(',').split(',')
    if line_lst[0] == 'user_id':
        continue
    # 错误格式下第一个字段多写了
    i = 2
    while i < len(line_lst):
        User_JS_tmp.append(float(line_lst[i]))
        i += 1
    # 去掉其中的均值
    print User_JS_tmp, '\n'
    del User_JS_tmp[12]
    del User_JS_tmp[11]
    del User_JS_tmp[8]
    del User_JS_tmp[7]



    Users_JS_lst.append(User_JS_tmp)
Users_JS_array = np.array(Users_JS_lst)
print '原始数据已经处理为数组...\n'
print 'DBSCAN Start...\n'
# Users_JS_array_std = preprocessing.scale(Users_JS_array, axis=0)
# pca = PCA(n_components=2)
# Users_JS_PCA = pca.fit_transform(Users_JS_array)
# y_pred = DBSCAN(eps=0.01, min_samples=100).fit_predict(Users_JS_PCA)
y_pred = KMeans(n_clusters=8).fit(Users_JS_array).labels_
# y_pred = KMeans(n_clusters=9).fit(Users_JS_PCA).labels_
x = 0
y = 1
plt.scatter(Users_JS_array[:, 0], Users_JS_array[:, 1], c=y_pred)
# plt.plot(Users_JS_array[:, x], Users_JS_array[:, y], 'bo')

# plt.plot(Users_JS_PCA[2751, x], Users_JS_PCA[2751, y], 'ms', label='ACM2278')
# plt.plot(Users_JS_PCA[2260, x], Users_JS_PCA[2260, y], 'r^', label='CMP2946')
# plt.plot(Users_JS_PCA[1241, x], Users_JS_PCA[1242, y], 'ro', label='PLJ1771')
# plt.plot(Users_JS_PCA[631, x], Users_JS_PCA[631, y], 'rx', label='CDE1846')
# plt.plot(Users_JS_PCA[1451, x], Users_JS_PCA[1451, y], 'rs', label='MBG3183')
plt.plot(Users_JS_array[2751, x], Users_JS_array[2751, y], 'ms', label='ACM2278')
plt.plot(Users_JS_array[2260, x], Users_JS_array[2260, y], 'r^', label='CMP2946')
plt.plot(Users_JS_array[1241, x], Users_JS_array[1242, y], 'ro', label='PLJ1771')
plt.plot(Users_JS_array[631, x], Users_JS_array[631, y], 'rx', label='CDE1846')
plt.plot(Users_JS_array[1451, x], Users_JS_array[1451, y], 'rs', label='MBG3183')
plt.legend(loc = 'upper left')
plt.show()
print 'y_pred[:10] is ', y_pred[:10], '\n'
print 'y_pred中类别为： ', len(set(y_pred)), '\n'
print 'DBSCAN已经完成...\n'

# 错误格式：
# JLF3219,ADR1517,36.0,39.0,13.0,19.0,27.0,-15.9016,-20.1751490909,-17.424,-19.8736,-15.0351142857,-20.0305742857,-16.456,-20.6184,-19.844,-15.9316,
# 上述格式多了第一个字段，从第二个字段正式开始
# 在2010-07-15JS.csv中，五个insiders的位置为：
# ACM2278:2753， CMP2946：2262，PLJ1771：1244， CDE1846：633， MBG3183：1453
# y_pred中五个insiders的位置下标应该为位置-2
print 'ACM2278 is ', y_pred[2751], '\n'
print 'CMP2946 is ', y_pred[2260], '\n'
print 'PLJ1771 is ', y_pred[1242], '\n'
print 'CDE1846 is ', y_pred[631], '\n'
print 'MBG3183 is ', y_pred[1451], '\n'
print '统计用户群组中每个群簇的用户个数..\n'
KM_0 = 0
KM_1 = 0
KM_2 = 0
KM_3 = 0
KM_4 = 0
KM_5 = 0
KM_6 = 0
KM_7 = 0
KM_8 = 0
KM_9 = 0
for label in y_pred:
    if label == 0:
        KM_0 += 1
    if label == 1:
        KM_1 += 1
    if label == 2:
        KM_2 += 1
    if label == 3:
        KM_3 += 1
    if label == 4:
        KM_4 += 1
    if label == 5:
        KM_5 += 1
    if label == 6:
        KM_6 += 1
    if label == 7:
        KM_7 += 1
    if label == 8:
        KM_8 += 1
    if label == 9:
        KM_9 += 1
print 'KM聚类中用户个数分别为：\n'
print 'KM_0 is ', KM_0, '\n'
print 'KM_1 is ', KM_1, '\n'
print 'KM_2 is ', KM_2, '\n'
print 'KM_3 is ', KM_3, '\n'
print 'KM_4 is ', KM_4, '\n'
print 'KM_5 is ', KM_5, '\n'
print 'KM_6 is ', KM_6, '\n'
print 'KM_7 is ', KM_7, '\n'
print 'KM_8 is ', KM_8, '\n'
print 'KM_9 is ', KM_9, '\n'
print '程序完毕..\n'
sys.exit()


