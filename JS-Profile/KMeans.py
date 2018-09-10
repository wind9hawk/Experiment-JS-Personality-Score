# coding:utf-8
# 本脚本开始对之前生成的用户Job Satisfaction特征数据集进行初步的K均值聚类
# 聚类前需要先对数据进行归一化

import sys
import numpy as np
from sklearn import  preprocessing
from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

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
def Draw(f_array, index_x, index_y, Labels_lst): # index_x与index_y为记录中对应特征的下标，比index_lst的下标多1
    index_lst = ['O', 'C', 'N', 'R-CPB-I', 'R-CPB-O', 'Low_C', 'Low_A', 'High_N']
    insiders_lst = ['ACM2278', 'CMP2946', 'PLJ1771', 'CDE1846', 'MBG3183']
    color_lst = ['bo', 'g^', 'yo', 'cs',  'gs',  'x', 'go', 'bx',  'y^', 'gx', 'ys']
    # CAN文件中位置： ACM2278:2644，CMP2946：2175，PLJ1771：1188，CDE1846：604，MBG3183：1390
    plt.xlabel(index_lst[index_x - 1])
    plt.ylabel(index_lst[index_y - 1])
    # plt.plot(f_array[:, index_x - 1], f_array[:, index_y - 1], 'bo')
    i = 0
    while i < len(f_array):
        plt.plot(f_array[i, index_x - 1], f_array[i, index_y - 1], color_lst[Labels_lst[i]])
        i += 1
    plt.plot(f_array[2643, index_x - 1], f_array[2643, index_y - 1], 'm^', label='ACM2278')
    plt.plot(f_array[2174, index_x - 1], f_array[2174, index_y - 1], 'r^', label='CMP2946')
    plt.plot(f_array[1187, index_x - 1], f_array[1187, index_y - 1], 'ro', label='PLJ1771')
    plt.plot(f_array[603, index_x - 1], f_array[603, index_y - 1], 'mo', label='CDE1846')
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


print 'KMeans Test...\n'

# f = open(r'2010-07-User-8JS-Model-median.csv', 'r')
f = open(r'CERT6.2-2010-07-New-25JS.csv', 'r')
f_lst = f.readlines()
f.close()

f_KM = open(r'KMeans_Result.csv', 'w')

print 'File Creat done...\n'

f_feat_lst = []
for line in f_lst:
    f_feat_tmp = []
    line_lst = line.strip('\n').strip(',').split(',')
    if line_lst[0] == 'user_id':
        continue
    i = 1
    while i < len(line_lst):
        f_feat_tmp.append(float(line_lst[i]))
        i += 1
    f_feat_lst.append(f_feat_tmp)
f_feat_array = np.array(f_feat_lst)
print 'f_feat_array[0] is ', f_feat_array[0], '\n'

print 'Normalization...\n'
# 区间化
min_max_scaler = preprocessing.MinMaxScaler()
f_nor_array = min_max_scaler.fit_transform(f_feat_array)
print 'f_feat after Normalization..\n', f_nor_array[0], '\n'


print '在进行K均值聚类前先做PCA降维..\n'
pca = PCA(n_components=10)
newData = pca.fit_transform(f_nor_array)
print 'KMeans start...\n'
# kmeans = cluster.KMeans(n_clusters=6, random_state=10).fit(newData)
newData = f_feat_array
kmeans = cluster.KMeans(n_clusters=6, random_state=10).fit(newData)
# insiders_lst = ['ACM2278', 'CMP2946', 'PLJ1771', 'CDE1846', 'MBG3183']
# 在*-median.csv文件中，五个攻击用户的位置为：
# ACM2278：2644-【2643】， CMP2946：2175-【2174】， PLJ1771：1188-【1187】；
# CDE1846：604-【603】， MBG3183：1390-【1389】

# JS_Feat_array = np.array(JS_Feat)
# JS_Feat_Scale = np.array(JS_Feat)
# JS_Feat_Scale = preprocessing.scale(JS_Feat_array)

print '开始写入KM聚类结果到对应文件...\n'
print '对于PCA（2）与KM（5）而言...\n'
f_km_0 = open(r'KM-5_0.csv', 'w')
f_km_1 = open(r'KM-5_1.csv', 'w')
f_km_2 = open(r'KM-5_2.csv', 'w')
f_km_3 = open(r'KM-5_3.csv', 'w')
f_km_4 = open(r'KM-5_4.csv', 'w')

j = 0
while j < 0:  # len(newData):
    if kmeans.labels_[j] == 0:
        print newData[j], type(newData[j]), '\n'
        f_km_0.write(str(j))
        f_km_0.write(',')
        f_km_0.write(str(newData[j][0]))
        f_km_0.write(',')
        f_km_0.write(str(newData[j][1]))
        f_km_0.write('\n')
        j += 1
        continue
    if kmeans.labels_[j] == 1:
        print newData[j], type(newData[j]), '\n'
        f_km_1.write(str(j))
        f_km_1.write(',')
        f_km_1.write(str(newData[j][0]))
        f_km_1.write(',')
        f_km_1.write(str(newData[j][1]))
        f_km_1.write('\n')
        j += 1
        continue
    if kmeans.labels_[j] == 2:
        print newData[j], type(newData[j]), '\n'
        f_km_2.write(str(j))
        f_km_2.write(',')
        f_km_2.write(str(newData[j][0]))
        f_km_2.write(',')
        f_km_2.write(str(newData[j][1]))
        f_km_2.write('\n')
        j += 1
        continue
    if kmeans.labels_[j] == 3:
        print newData[j], type(newData[j]), '\n'
        f_km_3.write(str(j))
        f_km_3.write(',')
        f_km_3.write(str(newData[j][0]))
        f_km_3.write(',')
        f_km_3.write(str(newData[j][1]))
        f_km_3.write('\n')
        j += 1
        continue
    if kmeans.labels_[j] == 4:
        print newData[j], type(newData[j]), '\n'
        f_km_4.write(str(j))
        f_km_4.write(',')
        f_km_4.write(str(newData[j][0]))
        f_km_4.write(',')
        f_km_4.write(str(newData[j][1]))
        f_km_4.write('\n')
        j += 1
        continue
print 'KM聚类分类结果文件已经写入...PCA(2)..\n'
f_km_0.close()
f_km_1.close()
f_km_2.close()
f_km_3.close()
f_km_4.close()
print '开始绘制二维图，需要指定x-y轴...\n'
# Draw(newData, 1, 2, kmeans.labels_)

print '统计每个类别的个数...\n'
L_0 = 0
L_1 = 0
L_2 = 0
L_3 = 0
L_4 = 0.0
L_5 = 0.0
L_6 = 0.0
L_7 = 0.0
L_8 = 0.0
L_9 = 0.0
L_10 = 0.0
print kmeans.labels_[:10], '\n'
for l in kmeans.labels_:
    if l == 0:
        L_0 += 1.0
    if l == 1:
        L_1 += 1.0
    if l == 2:
        L_2 += 1.0
    if l == 3:
        L_3 += 1.0
    if l == 4:
        L_4 += 1.0
    if l == 5:
        L_5 += 1.0
    if l == 6:
        L_6 += 1.0
    if l == 6:
        L_7 += 1.0
    if l == 6:
        L_8 += 1.0
    if l == 6:
        L_9 += 1.0
    if l == 6:
        L_10 += 1.0


# 在2010-07-25JS.csv中：
# Line 2753: ACM2278
# Line 2262: CMP2946
# Line 1244: PLJ1771
# Line 633: CDE1846
# Line 1453: MBG3183
print 'Center is ', kmeans.cluster_centers_, '\n'
print 'ACM2278\'s label is  ', kmeans.labels_[2751], '\n'
print 'CMP2946\'s label is  ', kmeans.labels_[2260], '\n'
print 'PLJ1771\'s label is  ', kmeans.labels_[1242], '\n'
print 'CDE1846\'s label is  ', kmeans.labels_[631], '\n'
print 'MBG3183\'s label is  ', kmeans.labels_[1451], '\n'
print '每个类别的用户数量...\n'
print L_0, '\n'
print L_1, '\n'
print L_2, '\n'
print L_3, '\n'
print L_4, '\n'
print L_5, '\n'
print L_6, '\n'
print L_7, '\n'
print L_8, '\n'
print L_9, '\n'
print L_10, '\n'
print 'Center is ', kmeans.cluster_centers_,'\n'

sys.exit()
