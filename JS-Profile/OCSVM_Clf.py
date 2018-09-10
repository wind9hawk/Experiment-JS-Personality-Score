# coding:utf-8
# 本脚本尝试使用OCSVM分析提取的19维度的JS特征，看是否依靠大量正常用户训练以发现潜在的攻击用户
# 假设企业中绝大部分用户的满意度均处于正常范围，极少数（低于5%）的满意度较低，为高危用户
# 首先使用分割训练集的方法，从正常用户中选择90%/80%作为训练集，然后剩下的作为测试集；
# 在进行OCSVM前可能需要进行标准化与PCA

import sys
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import MinMaxScaler
# 在2010-07-25JS.csv中：
# Line 2753: ACM2278
# Line 2262: CMP2946
# Line 1244: PLJ1771
# Line 633: CDE1846
# Line 1453: MBG3183
# user_id,O_Score,C_Score,E_Score,A_Score,N_Score,
# Team_CPB-I-mean,Team_CPB-O-mean,Users-less-mean-A,Users-less-mean-A and C,Users-less-mean-C,Users-High-mean-N,
# Team_CPB-I-median,Team_CPB-O-median,
# Dpt-CPB-I-mean,Dpt_CPB-O-mean,Dpt_CPB-I-median,Dpt_CPB-O-median,
# Leader_CPB-I,Leader_CPB-O
# 由于原始记录中包含第一行标题行，故insiders的实际位置要-1，如果考虑坐标的话需要再-1

# 数组寻元素返回索引值
def IndexInArray(x, y_array):
    i = 0
    while i < len(y_array):
        if x in  y_array[i]:
            print 'x is ', x, '\n'
            print 'y is ', y_array[i], '\n'
            i += 1
            return i
        else:
            i += 1
            continue
    return 'No Match'


print '开始读入原始数据...\n'
f_cert = open(r'CERT6.2-2009-10-New-26JS.csv', 'r')
# f_cert = open(r'2010-07-19JS.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()
print '数据读入完毕...\n'

print '构造训练集与训练标签...\n'
JS_Users = []
Users_nm = []
for line in f_cert_lst:
    JS_tmp = []
    line_lst = line.strip('\n').strip(',').split(',')
    if line_lst[0] == 'user_id':
        continue
    # JS_tmp.append(line_lst[0])
    i = 1
    while i < len(line_lst):
        # if i == 14:
        #     i += 1
        #     continue
        #if i == 22:
         #   i += 1
        #    continue
        JS_tmp.append(float(line_lst[i]))
        i += 1
    if len(line_lst) < 26:
        print JS_tmp, '\n'
    JS_Users.append(JS_tmp)
    Users_nm.append(line_lst[0])
    if line_lst[0] == 'PLJ1771':
        print 'PLJ1771', line_lst, '\n'
print '数据分割完成..\n'
JS_Users_array = np.array(JS_Users)
pca = PCA(n_components=4)
JS_PCA_0 = pca.fit_transform(JS_Users)
# JS_Users_scale = scale(JS_Users_array)
JS_Users_scale = Normalizer().fit_transform(JS_PCA_0)
# JS_Users_scale = scale(JS_PCA_0)
# min_max = MinMaxScaler()
# JS_Users_scale = min_max.fit_transform(JS_PCA_0)
JS_PCA = JS_Users_scale

print JS_Users_scale[2751], '\n'
print JS_Users_scale[2260], '\n'
print JS_Users_scale[1242], '\n'
print JS_Users_scale[631], '\n'
print JS_Users_scale[1451], '\n'
# 训练分类器前降维
# pca = PCA(n_components=5)
# JS_PCA = pca.fit_transform(JS_Users_scale)

Insiders_lst = []
Insiders_lst.append(JS_PCA[2751])
Insiders_lst.append(JS_PCA[2260])
Insiders_lst.append(JS_PCA[1242])
Insiders_lst.append(JS_PCA[631])
Insiders_lst.append(JS_PCA[1451])

# del JS_PCA[2751]
print JS_PCA[2751], '\n'
# JS_PCA = np.delete(JS_PCA, 2751, axis=0)
print JS_PCA[2751], '\n'
# sys.exit()
# JS_PCA = np.delete(JS_PCA, 2260, axis=0)
# JS_PCA = np.delete(JS_PCA, 1451, axis=0)
# JS_PCA = np.delete(JS_PCA, 1241, axis=0)
# JS_PCA = np.delete(JS_PCA,631, axis=0)
# del JS_PCA[2260]
# del JS_PCA[1242]
# del JS_PCA[631]
# del JS_PCA[1451]

Y_lst = [1] * len(JS_PCA)




# 先做一次OCSVM
X_train, X_test, Y_train, Y_test = train_test_split(JS_PCA, Y_lst, test_size=0.2, random_state=10)

print '开始OCSVM训练..\n'
print type(X_test), '\n'

X_train_array = np.array(X_train)
X_test_array = np.array(X_test)
clf = OneClassSVM(kernel='rbf', tol=0.01, nu=0.25, gamma='auto')
clf.fit(X_train_array)
pred = clf.predict(X_test_array)

# for user in X_test_array[pred == -1]:
    # print user, '\n'
# 在2010-07-19JS.csv中：
# Line 2753: ACM2278
# Line 2262: CMP2946
# Line 1244: PLJ1771
# Line 633: CDE1846

print ' ACM2278: ', clf.predict(Insiders_lst[0]), '\t', clf.decision_function(Insiders_lst[0]), '\n'
print '  CMP2946: ', clf.predict(Insiders_lst[1]), '\t', clf.decision_function(Insiders_lst[1]), '\n'
print ' PLJ1771: ', clf.predict(Insiders_lst[2]), '\t', clf.decision_function(Insiders_lst[2]), '\n'
print ' CDE1846: ', clf.predict(Insiders_lst[3]), '\t', clf.decision_function(Insiders_lst[3]), '\n'
print ' MBG3183: ', clf.predict(Insiders_lst[4]), '\t', clf.decision_function(Insiders_lst[4]), '\n'
print len(X_test_array[pred == -1]), '\n'
print len(X_test_array), '\n'
sys.exit()

print '所有[-1]标签的用户的距离...\n'
for user in X_test_array[pred == -1]:
    if clf.decision_function(user)> 0:
        print user, '\t', clf.decision_function(user), '\n'
    # print
print len(JS_PCA), len(JS_Users), '\n'

sys.exit()
# 把分类得到的178个用户写入高危用户文件
print '创建分类得到的高危用户文件Insiders_Risk_ByOCSVM...\n'
f_risk = open('CERT-6.2-2010-07-Insiders-Risk-OCSVM.csv', 'w')
Insider_lst = []
Insider_index = []
Cnt_Insiders = 0
for user in X_test_array[pred == -1]:
    for user_scale in JS_Users_scale:
        if user in user_scale:
            # print 'user is ', user, '\n'
            index_tmp = IndexInArray(user_scale, JS_Users_scale)
            if index_tmp == 'No Match':
                print 'No Match...', user_scale, '\n'
                continue
            if index_tmp not in Insider_index:
                Cnt_Insiders += 1
                Insider_index.append(index_tmp)
                Insiders_lst.append(Users_nm[index_tmp])
print len(Insiders_lst), '\n'
Delete_users = []
j = 0
while j < len(Insiders_lst):
    # print clf.predict(JS_Users_scale[j]), '\n'
    print j, '\n'
    # sys.exit()
    if clf.predict(JS_Users_scale[j])[0] == 1:
        print '>0:', Insiders_lst[j], '\n'
        Delete_users.append(Insiders_lst[j])
        np.delete(Insiders_lst, j, axis=0)

        j += 1
    else:
        j += 1
print 'After delete ', len(Insiders_lst), '\n'
Insiders_lst.append('CMP2946')
Insiders_lst.append('PLJ1771')
Insiders_lst.append('MBG3183')
# print len(Insiders_lst), '\t', Insiders_lst, '\n'
print len(Insiders_lst), '\n'
print Cnt_Insiders, '\n'

for user in Insiders_lst:
    # print '写入...', user, '\n'
    f_risk.write(user)
    f_risk.write('\n')
f_risk.close()
print 'Delete_users is ', Delete_users, '\n'

sys.exit()
