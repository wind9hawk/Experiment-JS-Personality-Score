# coding:utf-8
# 本脚本尝试用随机森林算法构建分类器，初步对15JS的特征重要性进行判断
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import sys

print '随机森林分类器实验。。。\n'
print '首先读入原始数据...\n'
f_cert = open(r'CERT6.2-2009-12-New-26JS.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()
print '原始数据JS特征读入完毕...\n'

print '构建标签列表...\n'
# 在2010-07-17JS.csv中，五个insiders的位置为：
# ACM2278:2753， CMP2946：2262，PLJ1771：1244， CDE1846：633， MBG3183：1453
# 因此，在去除标题行的15JS列表中，五个攻击者的下标为位置-2
Y_lables = [1] * (len(f_cert_lst) - 1)
Y_lables[2751] = -1
Y_lables[2260] = -1
Y_lables[1242] = -1
Y_lables[631] = -1
Y_lables[1451] = -1
print '标签列表构建完毕，其中有5个恶意-1类别...\n'

print '开始构建随机森林分类器...\n'
clf = RandomForestClassifier(n_estimators=1000, max_depth=100, max_features='auto', random_state=100)
X_lst = []
Name_lst = []
for line in f_cert_lst:
    X_tmp = []
    line_lst = line.strip('\n').strip(',').split(',')
    if line_lst[0] == 'user_id':
        continue
    Name_lst.append(line_lst[0])
    i = 1
    while i < len(line_lst):
        X_tmp.append(float(line_lst[i]))
        i += 1
    X_lst.append(X_tmp)
X_array = np.array(X_lst)
print X_array[0:2], '\n'
print type(X_array), '\n'
for line in X_array:
    if len(line) != 18:
        print line, '\n'
# sys.exit()
clf.fit(X_array, Y_lables)
print '特征重要性为: ', clf.feature_importances_, '\n'
sys.exit()

Y_estimats = []
print clf.predict(X_lst[0]), '\n'
cnt = 0
for user in X_lst:
    # print user, '\n'
    Y_estimats.extend(clf.predict(user))
    # print '用户分类添加完成..\n'
    # print Y_estimats, '\n'
    cnt += 1
    print cnt, '\n'
Anormaly_lst = []
print '开始统计Anormaly_lst...\n'
i = 0
while i < len(Y_estimats):
    if Y_estimats[i] == -1:
        Anormaly_lst.append(X_lst[i])
        print Name_lst[i], i, '个用户异常...\n'
        i += 1
    else:
        print Name_lst[i], i, ' 个用户正常...\n'
        i += 1
# print 'Anormaly_lst is ', Anormaly_lst, '\t', len(Anormaly_lst), '\n'
for user in Anormaly_lst:
    print user, '\n'
print len(Anormaly_lst), '\n'

sys.exit()
