# coding:utf-8
# 本脚步作为实验二，利用论文中揭示的模型关系建模CPB-I与CPB-O，具体为：
# CPB-I = A均值-->CPB-I + A均值-->JS-->CPB-I
# CPB-O = C均值-->CPB-O + A均值-->JS-->CPB-O
# 其中关键的相关性有：
# A-CPB-I:-0.43, A-JS:0.31, JS-CPB-I:-0.41, JS-CPB-O:-0.43, C-CPB-O:-0.44
# 本脚本主要结合已经处理得到的2010-07-TeamUser文件以及psychometric.csv数据，计算出侧写用户工作满意度的特征；
# 其满意度特征来自于两部分，一个是psychometric.csv中提供的用户的原始OCEAN分数，重点关注NAC三个维度，
# 人格特征与工作满意度的显著相关性为：A-JS：0.31，C-JS：0.22，N-JS：-0.23
# 第二部分考虑到用户所处的人际关系的成员人格特征的影响，其直接影响是工作中的CPB-I与CPB-O两类行为，依据相关性有：
# A-CPB-I：-0.43， C-CPB-I：-0.16， N-CPB-I：0.24
# A-CPB-O：-0.41， C-CPB-O：-0.44， N-CPB-O：0.47
# 接下来对于每个用户而言，其侧写工作满意度的特征由5个维度组成，分别是
# 【原始C分数，原始A分数，原始N分数】分别关联到Job Satisfaction；
# 团队成员中除去自身外其他所有成员的【C均值，A均值，N均值】分别关联到CPB-I/CPB-O，然后除以对应的C标准差，A标准差，N标准差；

import sys
import numpy as np

# Locate_User函数用于从给定的文件行列表中定位含有指定用户信息的行记录
def Locate_User(user, file):
    for line in file:
        line_lst = line.strip('\n').strip(',').split(',')
        if user in line_lst:
            return line_lst
        else:
            continue
    return 'No'


print '开始读入文件...\n'
# 读入用户团队信息
f_0 = open(r'S:\内部威胁\数据集\Cert-Data\CERT_Result\Experiment\Experiment-FMM-JobSatisfaction\2010-07-TeamUser-UserId.csv'.decode('utf-8'), 'r')
f_0_lst = f_0.readlines()
f_0.close()
print 'TeamUser-further 文件读取完毕...\n'

# 读入用户的人格特征数据
f_1 = open(r'S:\内部威胁\数据集\Cert-Data\CERT_Result\Experiment\Experiment-FMM-JobSatisfaction\psychometric.csv'.decode('utf-8'), 'r')
f_1_lst = f_1.readlines()
f_1.close()
print 'psychometric文件读取完毕...\n'

print '创建要写入的文件2010-07-User-JS.csv\n'
f_2 = open(r'S:\内部威胁\数据集\Cert-Data\CERT_Result\Experiment\Experiment-FMM-JobSatisfaction\2010-07-User-5JS-Model-median.csv'.decode('utf-8'), 'w')
print '开始循环读取psychometric中的用户数据...\n'
User_JS_Feat = []
Error_lst =[]
Mean_value = []
Personality_lst = []

for user in f_1_lst[0:-1]:
    User_JS_tmp = []
    Personality_lst_tmp = []
    # psychometric file format: employee_name,user_id,O,C,E,A,N
    # Nicholas Fletcher Pruitt,NFP2441,34,39,38,36,21
    # 格式化人格特征数据中的行记录为字符串列表
    user_lst = user.strip('\n').strip(',').split(',')
    if 'user_id' in user_lst:
        print '标题行，跳过..\n'
        continue
    print '人格特征的行记录为 ', user_lst, '\n'
    Personality_lst_tmp.append(float(user_lst[3]))
    Personality_lst_tmp.append(float(user_lst[5]))
    Personality_lst_tmp.append(float(user_lst[6]))
    Personality_lst.append(Personality_lst_tmp)
Personality_array = np.array(Personality_lst)
# 全部用户的C-A-N的均值
Mean_value = Personality_array.mean(axis=0)

None_User = []
for user in f_1_lst[0:-1]:
    User_JS_tmp = []
    Personality_lst_tmp = []
    # psychometric file format: employee_name,user_id,O,C,E,A,N
    # Nicholas Fletcher Pruitt,NFP2441,34,39,38,36,21
    # 格式化人格特征数据中的行记录为字符串列表
    user_lst = user.strip('\n').strip(',').split(',')
    if 'user_id' in user_lst:
        print '标题行，跳过..\n'
        continue
    print '人格特征的行记录为 ', user_lst, '\n'
    # Personality_lst_tmp.append(user_lst[3])
    # Personality_lst_tmp.append(user_lst[5])
    # Personality_lst_tmp.append(user_lst[6])
    User_JS_tmp.append(user_lst[1])
    # 计算C特质的满意度侧写
    User_JS_tmp.append(float(user_lst[3]) * 0.22)
    # 计算A特质的满意度侧写
    User_JS_tmp.append(float(user_lst[5]) * 0.31)
    # 计算N特质的满意度侧写
    User_JS_tmp.append(float(user_lst[6]) * (-0.23))
    print User_JS_tmp, '\t', 'C-A-N原始特质分析完成...\t即将开始分析其人际网络影响...\n'
    # 需要先确定用户所处团队，然后计算团队中除了自己意外其他成员的特质分数之和
    # 文件格式：Department is 5 - Security,[0]
    # 7 - Medical,['Lev Myles Harrington', 'JLM3847', 'NBF3844', 'DBB3846', 'LMH3831', 'MSP3845', 6]
    # 如果直接split(','):
    # '7 - Medical', "['Lev Myles Harrington'", " 'JLM3847'", " 'NBF3844'", " 'DBB3846'", " 'LMH3831'", " 'MSP3845'", ' 6]'
    # 当使用split方法分割字符串时，需要考虑到[]以及多出的''
    # 7 - BuildingSecurity,AMJ2374,GKK2422,DKD2409,LJE2413,MDG2418,MJP2421,TTP2417,HIA2415,DHS2419,
    # SNV2423,ZTB2410,AMJ2374,WYC2416,DJP2420,WAJ2412,15,
    # 匹配负责人时需要转换成简易记号方式
    # 确定用户ID所在的team
    User_Nm_lst = Locate_User(user_lst[1], f_0_lst)
    if User_Nm_lst == 'No':
        print user_lst[1], 'has no team...\n'
        None_User.append(user_lst[1])
        continue

    team_user = []
    for user_t in User_Nm_lst:
        if '-' in user_t:
            continue
        if user_lst[1] in user_t:
            print '用户自身，跳过\n'
            continue
        if len(user_t) < 7: # 读到最后的用户数量
            break
        team_user.append(user_t)
    print user_lst[1], ' 的团队成员有: ', team_user, '\n'

    # 已经建立了用户对应的团队成员列表team_user，接下来要映射成团队成员的C-A-N分数
    Personality_Score = []
    for user_team in team_user:
        personality_tmp = []
        User_OCEAN_lst = Locate_User(user_team, f_1_lst)
        personality_tmp.append(float(User_OCEAN_lst[3]))
        personality_tmp.append(float(User_OCEAN_lst[5]))
        personality_tmp.append(float(User_OCEAN_lst[6]))
        Personality_Score.append(personality_tmp)
    Personality_Score_array = np.array(Personality_Score)
    # 默认array.mean()是得到一个标量值，只有当axis=0时才是按列计算，axie=1时时按行计算
    Personality_mean = Personality_Score_array.mean(axis=0)
    Personality_std = Personality_Score_array.std(axis=0)
    Personality_sum = Personality_Score_array.sum(axis=0)
    # print Personality_Score_array[0:10], '\n'
    Personality_median = np.median(Personality_Score_array, axis=0)
    # 尝试使用中位数而非均值替代原有数据
    # 尝试用团队中的LowC-LowC-HighN成员的数值来计算均值，作为计算CPB-I与CPB-O的依据
    # Personality_median = np.median(Personality_Score_array, axis=0)
    # A-CPB-I：-0.43， C-CPB-I：-0.16， N-CPB-I：0.24
    # A-CPB-O：-0.41， C-CPB-O：-0.44， N-CPB-O：0.47
    if np.size(Personality_mean) < 3:
        Error_lst.append(user_team)
        continue
    if np.size(Personality_std) < 3:
        Error_lst.append(user_team)
        continue
        # 开始补充记录每个Team中C-A低于均值，而N高于均值的个体数
    C_num = 0
    A_num = 0
    N_num = 0
    Low_C_lst = []
    Low_A_lst = []
    High_N_lst = []
    for user in team_user:
        User_OCEAN_lst = Locate_User(user, f_1_lst)
        print User_OCEAN_lst,'\n'
        print User_OCEAN_lst[3], Personality_mean[0], '\n'
        # 确保比较大小的两边变量类型一致，否则无法正确比较
        # Personality_mean储存的为团队均值
        if float(User_OCEAN_lst[3]) < Mean_value[0]:
            C_num += 1
            Low_C_lst.append(float(User_OCEAN_lst[3]))
        if float(User_OCEAN_lst[5]) < Mean_value[1]:
            A_num += 1
            Low_A_lst.append(float(User_OCEAN_lst[5]))
        if float(User_OCEAN_lst[6]) > Mean_value[2]:
            N_num += 1
            High_N_lst.append(float(User_OCEAN_lst[6]))
    Low_C_array = np.array(Low_C_lst)
    Low_A_array = np.array(Low_A_lst)
    High_N_array = np.array(High_N_lst)
    # print Low_C_array, '\n'
    # 均值的效果再次平均了，不应使用均值，而是可以使用其和
    # 当使用和的时候，因为LowA人数多的人反而
    Low_C_mean = Low_C_array.sum()
    Low_A_mean = Low_A_array.sum()
    High_N_mean = High_N_array.sum()
    # CPB-I = A均值-->CPB-I + A均值-->JS-->CPB-I
    # CPB-O = C均值-->CPB-O + A均值-->JS-->CPB-O
    # 其中关键的相关性有：
    # Personality中顺序为C-A-N
    # A-CPB-I:-0.43, A-JS:0.31, JS-CPB-I:-0.41, JS-CPB-O:-0.43, C-CPB-O:-0.44
    # 使用团队中的和作为计算CPB_I与CPB_O的数据
    # CPB_I = (Personality_mean[1] * (-0.43) + Personality_mean[1] * 0.31 * (-0.41))
    # CPB_O = (Personality_mean[1] * 0.31 * (-0.43) + Personality_mean[0] * (-0.44))
    # CPB_I = (Personality_sum[1] * (-0.43) + Personality_sum[1] * 0.31 * (-0.41))
    # CPB_O = (Personality_sum[1] * 0.31 * (-0.43) + Personality_sum[0] * (-0.44))
    CPB_I = (Personality_median[1] * (-0.43) + Personality_median[1] * 0.31 * (-0.41))
    CPB_O = (Personality_median[1] * 0.31 * (-0.43) + Personality_median[0] * (-0.44))
    # CPB_I = (Low_A_mean * (-0.43) + Low_A_mean * 0.31 * (-0.41))
    # CPB_O = (Low_A_mean * 0.31 * (-0.43) + Low_C_mean * (-0.44))
    User_JS_tmp.append(CPB_I)
    User_JS_tmp.append(CPB_O)

    User_JS_tmp.append(C_num)
    User_JS_tmp.append(A_num)
    User_JS_tmp.append(N_num)
    # print User_JS_tmp,'\n'

    User_JS_Feat.append(User_JS_tmp)

# print 'User_JS_Feat is ', User_JS_Feat, '\n'
for feat in User_JS_Feat:
    for score in feat:
        f_2.write(str(score))
        f_2.write(',')
    f_2.write('\n')
f_2.close()

print 'All User-JS-Feature done...\n'
print 'None users is ', None_User[0:10], '\n'
sys.exit()
