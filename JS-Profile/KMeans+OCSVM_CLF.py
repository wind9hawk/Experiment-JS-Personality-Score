# coding:utf-8
# 本脚本验证基于多KMeans投票的猜想
# 基本算法：
# 事先通过轮廓系数得到人格、团队因子、部门因子、领导人因子以及工作时长五项因素KMeans的最佳K值（从2-10中依据轮廓系数选取）
# 1. 处理原始26JS特征，得到五部分因素数据，顺序和原始JS文件数据一致；
# 2. 分别对五项数据进行KMeans聚类，得到五组聚类中心与每个用户的五组标签；
# 3. 在每个聚类群里，按照公式计算满意度影响程度，筛选出满意度程度高于均值的群簇，得到其标签；
# 4. 检查每个用户的五项标签，如果该标签位于满意度高于均值的标签中，则为1，否则为0；
# 5. 存储每个用户的五项JS标签以及其中1的个数到文件，然后根据K=3判断，凡是小于3的均划定为高危用户，查看5个Insiders的结果；
# 6. 需要分析[-1]用户个数，5个Insiders的分类情况；
import sys
import numpy as np
import math
from sklearn.cluster import KMeans
from sklearn.preprocessing import  MinMaxScaler
from sklearn.preprocessing import  scale
from sklearn.preprocessing import Normalizer
# from sklearn.preprocessing import MaxAbsScaler

def JS_1(center):
    # 2002:N:-0.29, E:0.25, O:0.02, A:0.17, C:0.26;
    score = center[0] * 0.08 + center[1] * 0.22 + center[2] * 0.08 + center[3] * 0.31 + center[4] * 0.23
    # score = center[2] + center[3] + center[4] + center[0] + center[1]
    # score = center[0] * 0.02 + center[1] * 0.26 + center[2] * 0.25 + center[3] * 0.17 + center[4] * 0.29
    return score
def JS_2(center):
    print 'JS_2 sum is ', center[2] + center[3] + center[4] + center[5], '\n'
    score = (center[0] + center[1]) * (1 - math.exp(center[2] + center[3] + center[4] + center[5]))
    return score
def JS_3(center):
    score = (center[0] + center[1]) * (1 - math.exp(center[2] + center[3] + center[4] + center[5]))
    return score
def JS_4(center):
    score = center[0] + center[1]
    return score
def JS_5(center):
    score = center[2]  * (1 - math.exp(center[0] + center[1]))
    return score
print '基于KMeans的多分类器投票...\n'
f_cert = open(r'CERT6.2-2009-12-New-26JS.csv', 'r')
f_cert_lst = f_cert.readlines()
f_cert.close()
print '原始JS特征数据读取完毕，接下来开始分割成五部分...\n'
Users_nm = []
Users_OCEAN = []
Users_TeamCPB = []
Users_DptCPB = []
Users_LeaderCPB = []
Users_JobTime = []
Users_26JS = []
for line in f_cert_lst:
    User_26JS_tmp = []
    # user_id,O_Score,C_Score,E_Score,A_Score,N_Score,Team_CPB-I-mean,Team_CPB-O-mean,Users-less-mean-A,Users-less-mean-A and C,Users-less-mean-C,Users-High-mean-N,Team_CPB-I-median,Team_CPB-O-median,No-JobState-in-Team,Dpt-CPB-I-mean,Dpt_CPB-O-mean,Dpt-Less-A-mean,Dpt-Less-AC-mean,Dpt-less-C-mean,Dpt-High-N-mean,Dpt_CPB-I-median,Dpt_CPB-O-median,No-JobState-in-Dpt,Job State,Leader_CPB-I,Leader_CPB-O
    # 开始挑选OCEAN分数
    line_lst = line.strip('\n').strip(',').split(',')
    if line_lst[0] == 'user_id':
        continue
    Users_nm.append(line_lst[0])
    i = 1
    while i < len(line_lst):
        User_26JS_tmp.append(float(line_lst[i]))
        i += 1
    Users_26JS.append(User_26JS_tmp)
# 在进一步处理前可以考虑标准化、最大值化、归一化
Users_26JS_scale = scale(Users_26JS)
Users_26JS_nor = Normalizer().fit_transform(Users_26JS)
Users_26JS_minmax = MinMaxScaler().fit_transform(Users_26JS)
for line in Users_26JS_nor:
    # user_id,O_Score,C_Score,E_Score,A_Score,N_Score,Team_CPB-I-mean,Team_CPB-O-mean,Users-less-mean-A,Users-less-mean-A and C,Users-less-mean-C,Users-High-mean-N,Team_CPB-I-median,Team_CPB-O-median,No-JobState-in-Team,Dpt-CPB-I-mean,Dpt_CPB-O-mean,Dpt-Less-A-mean,Dpt-Less-AC-mean,Dpt-less-C-mean,Dpt-High-N-mean,Dpt_CPB-I-median,Dpt_CPB-O-median,No-JobState-in-Dpt,Job State,Leader_CPB-I,Leader_CPB-O
    # 开始挑选OCEAN分数
    User_OCEAN = []
    User_TeamCPB = []
    User_DptCPB = []
    User_LeaderCPB = []
    User_JobTime = []
    Cnt_turn = 0
    # Users_nm.append(line_lst[0])
    line_lst = line
    i = 0
    while i < len(line_lst):
        # 结果分为不考虑中位数与考虑中位数两种情况
        # print '进入提取子循环...\t', Cnt_turn, '\n'
        Cnt_turn += 1
        # 提取OCEAN特征，下标1-5
        if i < 5:
            if i == 4:
                User_OCEAN.append(-1 * float(line_lst[i]))
                i += 1
                continue
            User_OCEAN.append(float(line_lst[i]))
            i += 1
            continue
        if i > 4 and i < 11: # 4 + 4 = 8，未考虑下标14的团队工作时间情况
        # if i > 6 and i < 13:
            if i == 11 or i == 12: # 先仅考虑均值的CPB
                User_TeamCPB.append(-1 * float(line_lst[i]))
                i += 1
                continue
            else:
                User_TeamCPB.append(float(line_lst[i]))
                i += 1
                continue
        if i > 13 and i < 20:  # 计算部门影响时暂时不考虑中位数的作用
        # if i > 15 and i < 22:
            if i == 20 or i == 21:
                User_DptCPB.append(-1 * float(line_lst[i]))
                i += 1
                continue
            else:
                User_DptCPB.append(float(line_lst[i]))
                i += 1
                continue
        if i == 24 or i == 25: # 如果是领导的CPB
            User_LeaderCPB.append(-1 * float(line_lst[i]))
            i += 1
            continue
        if i == 13 or i == 22 or i == 23: # 记录工作时间
            User_JobTime.append(line_lst[i])
            i += 1
            continue
        # 这里的i+=1不能忘记，因为没有统计中位数，所以有情况不落在任何一个if中
        i += 1
        continue
    Users_OCEAN.append(User_OCEAN)
    Users_TeamCPB.append(User_TeamCPB)
    Users_DptCPB.append(User_DptCPB)
    Users_LeaderCPB.append(User_LeaderCPB)
    Users_JobTime.append(User_JobTime)
    print line_lst[0], '五项特征组构建完毕...\n'
print '为了进一步比较，计算五组数据反映的JS的均值与中位数...\n'
OCEAN_score = []
for user in Users_OCEAN:
    OCEAN_score.append(JS_1(user))
OCEAN_score_array = np.array(OCEAN_score)
OCEAN_mean = OCEAN_score_array.mean()
OCEAN_median = np.median(OCEAN_score_array)
print 'OCEAN整体均值与中位数计算完成...\n'

TeamCPB_score = []
for user in Users_TeamCPB:
    TeamCPB_score.append(JS_2(user))
TeamCPB_score_array = np.array(TeamCPB_score)
Team_mean = TeamCPB_score_array.mean()
Team_median = np.median(TeamCPB_score_array)
print 'Team整体均值与中位数计算完成...\n'

DptCPB_score = []
for user in Users_DptCPB:
    DptCPB_score.append(JS_3(user))
DptCPB_score_array = np.array(DptCPB_score)
Dpt_mean = DptCPB_score_array.mean()
Dpt_median = np.median(DptCPB_score_array)
print 'Dpt整体均值与中位数计算完成...\n'

LeanderCPB_score = []
for user in Users_LeaderCPB:
    LeanderCPB_score.append(JS_4(user))
LeanderCPB_score_array = np.array(LeanderCPB_score)
Leader_mean = LeanderCPB_score_array.mean()
Leader_median = np.median(LeanderCPB_score_array)
print 'Leader整体均值与中位数计算完成...\n'

JobTime_score = []
for user in Users_JobTime:
    JobTime_score.append(JS_5(user))
JobTime_score_array = np.array(JobTime_score)
JobTime_mean = JobTime_score_array.mean()
JobTime_median = np.median(JobTime_score_array)
print 'JobTime整体均值与中位数计算完成...\n'

print 'CERT6.2中4000个用户的五项特征数组构建完毕...\n'

print '开始对五项特征分别KMeans...\n'
K1 = 10
K2 = 2
K3 = 10
K4 = 4
K5 = 7
# Users_OCEAN = scale(Users_OCEAN)
Clf_1 = KMeans(n_clusters=K1).fit(Users_OCEAN)#(scale(Users_OCEAN))
# Clf_1 = KMeans(n_clusters=K1).fit(MinMaxScaler().fit_transform(Users_OCEAN))
pred_1 = Clf_1.labels_
center_1 = Clf_1.cluster_centers_
# Users_TeamCPB = scale(Users_TeamCPB)
Clf_2 = KMeans(n_clusters=K2).fit(Users_TeamCPB)#(scale(Users_TeamCPB))
# Clf_2 = KMeans(n_clusters=K2).fit(MinMaxScaler().fit_transform(Users_TeamCPB))
pred_2 = Clf_2.labels_
center_2 = Clf_2.cluster_centers_
# Users_DptCPB = scale(Users_DptCPB)
Clf_3 = KMeans(n_clusters=K3).fit(Users_DptCPB)#(scale(Users_DptCPB))
# Clf_3 = KMeans(n_clusters=K3).fit(MinMaxScaler().fit_transform(Users_DptCPB))
pred_3 = Clf_3.labels_
center_3 = Clf_3.cluster_centers_
# Users_LeaderCPB = scale(Users_LeaderCPB)
Clf_4 = KMeans(n_clusters=K4).fit(Users_LeaderCPB)#(scale(Users_LeaderCPB))
# Clf_4 = KMeans(n_clusters=K4).fit(MinMaxScaler().fit_transform(Users_LeaderCPB))
pred_4 = Clf_4.labels_
center_4 = Clf_4.cluster_centers_
# Users_JobTime = scale(Users_JobTime)
Clf_5 = KMeans(n_clusters=K5).fit(Users_JobTime)#(scale(Users_JobTime))
# Clf_5 = KMeans(n_clusters=K5).fit(MinMaxScaler().fit_transform(Users_JobTime))
pred_5 = Clf_5.labels_
center_5 = Clf_5.cluster_centers_
print '五个特征组的KMeans训练完毕...\n'

print '依次计算每个分组里中心值反映的用户满意度程度高低...\n'
# 首先对于OCEAN反映的JS高低计算方法为：
# 或者根据CERT参考的文章的数据：
# A：0.31, C:0.22, -N:0.23, E:0.08, O:0.08
print '计算OCEAN分组中中心的JS值...\n'
JS_Score_Clf_1 = []
for center in center_1:
    # 多次实验证明，OCEAN直接求和结果不如加权和
    print center[4],'\n'
    # sys.exit()
    # score = center[0] * 0.08 + center[1] * 0.22 + center[2] * 0.08 + center[3] * 0.31 + center[4] * 0.23
    score = JS_1(center)
    # score = center[0] + center[1] + center[2] + center[3] + center[4]
    JS_Score_Clf_1.append(score)
score_mean_1 = np.array(JS_Score_Clf_1).mean()
score_median_1 = np.median(JS_Score_Clf_1)
High_JS_1 = []
j = 0
while j < K1:
    # if JS_Score_Clf_1[j] > score_mean_1:
    if JS_Score_Clf_1[j] > score_median_1:
    # if JS_Score_Clf_1[j] > OCEAN_mean:
    # if JS_Score_Clf_1[j] > OCEAN_median:
        High_JS_1.append(j)
        j += 1
    else:
        j += 1
print 'OCEAN群簇中高满意度标签为: ', High_JS_1, '\n'

print '计算团队CPB的中心的JS值...\n'
JS_Score_Clf_2 = []
for center in center_2:
    print center[2] + center[3] + center[4] + center[5], '\n'
    # score = (center[0] + center[1])  * (1 - math.log10(center[2] + center[3] + center[4] + center[5]))
    # score = (center[-1] + center[-2]) * (1 - math.log10(center[0] + center[1] + center[2] + center[3])) # 中位数CPB
    # score = (center[-1] + center[-2]) / (center[0] + center[1] + center[2] + center[3])
    # score = (center[0] + center[1]) * (1 - math.log10(center[2] + center[3] + center[4] + center[5] + 10))
    score = JS_2(center)
    JS_Score_Clf_2.append(score)
score_mean_2 = np.array(JS_Score_Clf_2).mean()
score_median_2 = np.median(JS_Score_Clf_2)
High_JS_2 = []
j = 0
while j < K2:
    # if JS_Score_Clf_2[j] > score_mean_2:
    if JS_Score_Clf_2[j] > score_median_2:
    # if JS_Score_Clf_2[j] > Team_mean: # 全局Team分数均值
    # if JS_Score_Clf_2[j] > Team_median:
        High_JS_2.append(j)
        j += 1
    else:
        j += 1
print '团队CPB群簇中高满意度标签为： ', High_JS_2, '\n'

print '计算部门CPB的中心的JS值...\n'
JS_Score_Clf_3 = []
print center_3, '\n'
for center in center_3:
    # score = (center[-1] + center[-2])  * (1 - math.log1p(center[0] + center[1] + center[2] + center[3])) # 中位数CPB
    #score = (center[0] + center[1]) * (1 - math.log10(center[2] + center[3] + center[4] + center[5]))
    score = JS_3(center)
    JS_Score_Clf_3.append(score)
score_mean_3 = np.array(JS_Score_Clf_3).mean()
score_median_3 = np.median(JS_Score_Clf_3)
High_JS_3 = []
j = 0
while j < K3:
    # if JS_Score_Clf_3[j] > score_mean_3:
    if JS_Score_Clf_3[j] > score_median_3:
    # if JS_Score_Clf_3[j] > Dpt_mean:
    # if JS_Score_Clf_3[j] > Dpt_median:
        High_JS_3.append(j)
        j += 1
    else:
        j += 1
print '部门中CPB群簇中高满意度标签为： ', High_JS_3, '\n'

print '计算领导CPB的中心的JS值...\n'
JS_Score_Clf_4 = []
print center_4, '\n'
for center in center_4:
    # score = center[0] + center[1]
    score = JS_4(center)
    JS_Score_Clf_4.append(score)
score_mean_4 = np.array(JS_Score_Clf_4).mean()
score_median_4 = np.median(JS_Score_Clf_4)
High_JS_4 = []
j = 0
while j < K4:
    # if JS_Score_Clf_4[j] > score_mean_4:
    if JS_Score_Clf_4[j] > score_median_4:
    # if JS_Score_Clf_4[j] > Leader_mean:
    # if JS_Score_Clf_4[j] > Leader_median:
        High_JS_4.append(j)
        j += 1
    else:
        j += 1
print '领导CPB群簇中高满意度标签为： ', High_JS_4, '\n'

print '计算工作连续时间的的JS值...\n'
JS_Score_Clf_5 = []
print center_5, '\n'
for center in center_5:
    score = JS_5(center)
    # score = center[2] * (1 - math.log10(center[0] + center[1]))
    JS_Score_Clf_5.append(score)
score_mean_5 = np.array(JS_Score_Clf_5).mean()
score_median_5 = np.median(JS_Score_Clf_5)
High_JS_5 = []
j = 0
while j < K5:
    if JS_Score_Clf_5[j] > score_mean_5:
    # if JS_Score_Clf_5[j] > score_median_5:
    # if JS_Score_Clf_5[j] > score_median_5:
    # if JS_Score_Clf_5[j] > JobTime_mean:
    # if JS_Score_Clf_5[j] > JobTime_median:
        High_JS_5.append(j)
        j += 1
    else:
        j += 1
print '工作连续时间中高满意度标签为： ', High_JS_5, '\n'

print '开始计算每个用户的整体满意度...\n'
Users_5JS = []
Insiders_nm = ['ACM2278', 'CMP2946', 'PLJ1771', 'CDE1846', 'MBG3183']
Insiders_index = []
r = 0
while r < len(Users_nm):
    User_5JS = []
    if pred_1[r] in High_JS_1:
        User_5JS.append(1)
    else:
        User_5JS.append(0)
    if pred_2[r] in High_JS_2:
        User_5JS.append(1)
    else:
        User_5JS.append(0)
    if pred_3[r] in High_JS_3:
        User_5JS.append(1)
    else:
        User_5JS.append(0)
    if pred_4[r] in High_JS_4:
        User_5JS.append(1)
    else:
        User_5JS.append(0)
    # if pred_5[r] in High_JS_5:
    #       User_5JS.append(1)
    # else:
    #       User_5JS.append(0)
    #print Users_5JS[r], '\n'
    #print Users_26JS[r][-3], '\n'
    if Users_26JS[r][-3] == 18:
        User_5JS.append(1)
    else:
        User_5JS.append(0)
    # Users_5JS.append(User_5JS)
    # if Users_nm[r] in Insiders_nm:
    #     Insiders_index.append(Users_nm[r])
    #     Insiders_index.append(r)
    Users_5JS.append(User_5JS)
    r += 1
print 'CERT6.2所有用户的5JS标签构建完毕...\n'
print Users_5JS[0], '\n'
# sys.exit()

print '开始写入一个5JS文件...\n'
f_5JS = open(r'CERT6.2-2009-12-5JS-Label.csv', 'w')
Risk_score = []
Risk_Index = []
print len(Users_5JS), '\t', len(Users_nm), '\n'
# sys.exit()
s = 0
while s < len(Users_nm):
    f_5JS.write(Users_nm[s])
    f_5JS.write(',')
    for ele in Users_5JS[s]:
        f_5JS.write(str(ele))
        f_5JS.write(',')
    f_5JS.write(str(Users_5JS[s].count(1)))
    f_5JS.write(',')
    #score_tmp = (Users_5JS[s][0] + Users_5JS[s][4]) * 4 + (Users_5JS[s][1] + Users_5JS[s][3]) * 2 + Users_5JS[s][2]
    score_tmp = 0.0
    score_tmp = (Users_5JS[s][0] + Users_5JS[s][4]) * 4 + (Users_5JS[s][1] + Users_5JS[s][3]) * 2 + Users_5JS[s][2]
    # k = 0
    # while k < 5:
    #     score_tmp += Users_5JS[s][k] * math.pow(2, 4-k)
    #     k += 1
    #if Users_5JS[s].count(1) < 3:
    #   Risk_Index.append(s)
    f_5JS.write(str(score_tmp))
    f_5JS.write('\n')
    Risk_score.append(score_tmp)
    s += 1
Risk_score_array = np.array(Risk_score)
Risk_mean = Risk_score_array.mean()
Risk_median = np.median(Risk_score_array)
Cnt_1_0 = 0
Cnt_1_1 = 0
Cnt_1_2 = 0
Cnt_10010 = 0
Cnt_Risk = 0.0
Train_index = []
Test_index = []
t = 0
while t < len(Users_5JS):
    # score_tmp = (user[0] + user[4]) * 4 + (user[1] + user[3]) * 2 + user[2]
    # score_tmp = 0.0
    # k = 0
    # while k < len(user):
        # score_tmp += user[k] * math.pow(2, 4-k)
        # k += 1
    score_tmp = 0.0
    #k = 0
    #while k < 5:
    #    score_tmp += Users_5JS[t][k] * math.pow(2, 4-k)
    #   k += 1
    score_tmp = (Users_5JS[t][0] + Users_5JS[t][4]) * 4 + (Users_5JS[t][1] + Users_5JS[t][3]) * 2 + Users_5JS[t][2]
    if Users_5JS[t].count(1) < 3: # or score_tmp < Risk_mean:
        #if score_tmp < Risk_mean :
        Cnt_Risk += 1
        Test_index.append(t)
        t += 1
    else:
        Train_index.append(t)
        t += 1
    # if user.count(1) == 0:
    #     Cnt_1_0 += 1
    # if user.count(1) == 1:
    #     Cnt_1_1 += 1
    # if user.count(1) == 2:
    #     Cnt_1_2 += 1
    #     if user[0] == 1 and user[3] == 1:
    #         Cnt_10010 += 1

print 'CERT6.2 5JS标签文件写入完毕...\n'
print '高危用户数目为： ', Cnt_Risk, '\n'
print '风险均值为： ', Risk_mean, '\n'
print '风险中位数为：', Risk_median, '\n'
print 'count(1)为0，1，2的用户数目分别为：', Cnt_1_0, Cnt_1_1, Cnt_1_2, '\n'
print '10010型用户为；', Cnt_10010, '\n'
# Line 2840: ACM2278,0,0,0,0,1,1
print 'ACM2278 is ', Users_5JS[2839], '\t', Risk_score_array[2839], '\n'
# Line 2330: CMP2946,1,0,0,1,1,3
print 'CMP  is ', Users_5JS[2329], '\t', Risk_score_array[2329], '\n'
# Line 1282: PLJ1771,0,0,0,0,1,1
print 'PLJ is ', Users_5JS[1281], '\t', Risk_score_array[1281], '\n'
# Line 655: CDE1846,1,0,0,1,0,2
print 'CDE is ', Users_5JS[654], '\t', Risk_score_array[654], '\n'
# Line 1494: MBG3183,1,0,0,1,0,2
print 'MBG is ', Users_5JS[1493], '\t', Risk_score_array[1493], '\n'
print Insiders_index, '\n'
print '训练集有： ', len(Train_index), '\n'
print '测试集有： ', len(Test_index), '\n'

sys.exit()






