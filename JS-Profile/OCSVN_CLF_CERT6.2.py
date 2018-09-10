# coding:utf-8
# 基于新的26JS用户满意度特征，训练OCSVM分类用户满意度；
# 与上个OCSVM的不同
# -1. 考虑了用户18个月是否全部在职，训练集用户必须18个月均在职；
# -2. 在18个月均在职的用户中，选择3200个用户用于训练OCSVM；
# -3. 剩余的18个月均在职的用户+18个月不全在职的用户+CDE+MBG；
# 首先从CERT中读取用户特征
# PCA降维；
# 归一化Normalizer
# 分割训练集与测试集，使用数据的索引进行分割

import sys
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import MinMaxScaler
import random

print '读入新的用户JS特征数据...\n'
f_cert = open(r'CERT6.2-2009-12-New-26JS.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()
print '读取用户工作状态数据...\n'
f_jobs = open(r'CERT6.2-2009-12-JobState.csv', 'r')
f_jobs_lst = f_jobs.readlines()
f_jobs.close()
print 'JS特征文件与工作状态文件均读入完毕...\n'

print '开始从4000个用户中选择训练集...\n'
# 本脚本实验从行索引的角度计算
Users_All_Jobs_index = []
Users_not_All_Jobs_index = []
Users_26JS = []
cert_index = 0
while cert_index < len(f_cert_lst):
    line_lst = f_cert_lst[cert_index].strip('\n').strip(',').split(',')
    if line_lst[0] == 'user_id':
        cert_index += 1
        continue
    Users_26JS_tmp = []
    # Users_26JS_tmp.append(line_lst[0])
    i = 1
    while i < len(line_lst):
        Users_26JS_tmp.append(float(line_lst[i]))
        i += 1
    # 从[-3]字段判定是否All Jobs
    if float(line_lst[-3]) == 18:
        # print line_lst[0], '干满18个月...\n'
        # print line_lst, '\n'
        # print line_lst[-3], '\n'
        # 索引计算
        # 因为Users_26JS文件中不包含标题行，因此原先的索引在该文件中+1
        Users_All_Jobs_index.append(cert_index - 1)
        Users_26JS.append(Users_26JS_tmp)
        cert_index += 1
        continue
    else:
        # print line_lst[0], '没有干满18个月...\n'
        # print cert_index - 1, '\n'
        # 索引计算
        #if line_lst[0] == 'CMP2946':
        #    print cert_index, '\n'
        #    sys.exit()
        # Users_not_All_Jobs_index.append(cert_index - 1)
        # 不再因为非全职单独考虑
        Users_All_Jobs_index.append(cert_index - 1)
        Users_26JS.append(Users_26JS_tmp)
        cert_index += 1
        continue
# sys.exit()
print len(Users_All_Jobs_index), ' 个用户干满18个月...\n'
print len(Users_not_All_Jobs_index), ' 个用户未干满18个月...\n'
print len(f_cert_lst), ' 个用户...\n'
# 3638个用户干满18个月
# 361个用户未干满18个月
# 总计3999个用户，少了一个主席用户（原始LDAP长度小于9）
# 考虑标题行在内
# ACM2278:line 2841;
# CMP2946:line 2331;
# PLJ1771:line 1283;
# CDE1846:line 656;
# MBG3183:line 1495;
# 如果考虑上述去掉标题行的索引，应当-2T5TGUI12QWER
# 使用索引作为元素指标时，一定要注意先后两个列表中元素的索引未必一致，因此不可直接拿原先的索引套用新列表
print '从全职用户集合中去掉Insiders到测试集...\n'
Insiders_nm = ['ACM2278', 'CMP2946', 'PLJ1771', 'CDE1846', 'MBG3183']
for user_index in Users_All_Jobs_index:
    if Users_26JS[user_index][0] in Insiders_nm:
        # print user_index, 'Insiders in Users_All_Jobs_index...\n' # 验证5个Insiders的原数据索引-2正确
        # print Users_26JS[user_index], '\n'
        Users_not_All_Jobs_index.append(user_index)
        # print user_index in Users_not_All_Jobs_index, '\n'
        del Users_All_Jobs_index[Users_All_Jobs_index.index(user_index)]
        # print user_index in Users_All_Jobs_index, '\n'
        continue
    else:
        continue
print '开始分割数据集为训练集与测试集...\n'
# 训练数据集中不再包含五个insiders，且也不包括未干满18个月的用户
# 从3638-2=3636个用户中随机选择3200个用户
# 先构建标签数据
Y_train = [1] * len(Users_All_Jobs_index)
Y_test = []
for index_0 in Users_not_All_Jobs_index:
    if Users_26JS[index_0][0] in Insiders_nm:
        Y_test.append(-1)
        print '[1]类个数为： ', Y_test.count(-1), '\n'
    else:
        Y_test.append(1)
# 从干满18个月的用户中分出3200个训练集，剩余纳入测试集，需要与已有测试集归并
X_train, X_test_0, Y_train_0, Y_test_0 = train_test_split(Users_All_Jobs_index, Y_train, test_size=0.2, random_state=15)
# 原来全工的用户的一部分补充到测试集
for index_1 in X_test_0:
    Users_not_All_Jobs_index.append(index_1)
for lable_1 in Y_test_0:
    Y_test.append(lable_1)
print '开始进行Users_26JS的降维与归一化...\n'
# 由于分析的是索引，在训练OCSVM时需要转化成特征向量
# 先从索引映射到特征向量

pca = PCA(n_components=4)
Users_26JS_pca = pca.fit_transform(Users_26JS)
Users_26JS_pca_nor = Normalizer().fit_transform(Users_26JS_pca)
print 'PCA与归一化完成...\n'
X_train_lst = []
X_test_lst = []
for index_2 in X_train:
    X_train_lst.append(Users_26JS_pca_nor[index_2])
for index_3 in Users_not_All_Jobs_index:
    X_test_lst.append(Users_26JS_pca_nor[index_3])
X_train_array= np.array(X_train_lst)
X_test_array = np.array(X_test_lst)

print 'OCSVM开始训练...\n'
clf = OneClassSVM(kernel='rbf', tol=0.01, nu=0.25, gamma='auto')
clf.fit(X_train_array)
pred = clf.predict(X_test_array)

print '开始输出分类结果...\n'
# 考虑标题行在内
# ACM2278:line 2841;
# CMP2946:line 2331;
# PLJ1771:line 1283;
# CDE1846:line 656;
# MBG3183:line 1495;
print 'ACM2278 is ', clf.predict(Users_26JS_pca_nor[2839]), '\t', clf.decision_function(Users_26JS_pca_nor[2839]), '\n'
print 'CMP2946 is ', clf.predict(Users_26JS_pca_nor[2329]), '\n', clf.decision_function(Users_26JS_pca_nor[2329]), '\n'
print 'PLJ1771 is ', clf.predict(Users_26JS_pca_nor[1281]), '\t', clf.decision_function(Users_26JS_pca_nor[1281]), '\n'
print 'CDE1846 is ', clf.predict(Users_26JS_pca_nor[654]), '\n',  clf.decision_function(Users_26JS_pca_nor[654]), '\n'
print 'MBG3183 is ', clf.predict(Users_26JS_pca_nor[1493]), '\n', clf.decision_function(Users_26JS_pca_nor[1493]), '\n'

print '分类出[-1]类用户数目为： ', len(X_test_array[pred == -1]), '\n'
print '总共测试集用户为： ', len(X_test_array), '\n'
print '训练集总共有： ', len(X_train_lst), '\n'



print '支持向量的索引为：', clf.support_, '\n'
# print '识别为[-1]的用户为： ', X_test_array[pred == -1], '\n'



sys.exit()





