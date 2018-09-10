# coding:utf-8
class point(object):
    x=0.0
    y=0.0
pointF=[]
pointType=[]#��¼�����ڵ���
AverageD=[]# ��¼ÿ������ľ�ֵ
ZArray=[]


StdDiff=[]   # ��¼�����������ı�׼��ֵ
Std=[]       #��׼��������
Sum=[]       #�����ʱ
N=[]          #��¼ÿ����������

StdDistance=[] #��������֮�����
StdDisMax=[]
StdDisMaxCor=[]

MaxDiff=1        #��׼���ж����� 
MinDistance=4    #��ͬ����������С����
MaxNumStd=2      #���ľ���������Ŀ
TotalNum=10       #����

SAArray=[[]]
ZDistance=[]
ZDistanceR=[]
ZDistanceC=[]
StdTime=10
Nc=1
step=2             #��¼���輰��ǰ״̬
CountTime=0
#---------------------------------��ʼ��
for i in range(TotalNum):
    pointF+=[point()]
    pointType+=[0]
    StdDiff+=[point()]
    ZDistance+=[0]
    ZDistanceR+=[0]
    ZDistanceC+=[0]
for i in range(MaxNumStd):
    AverageD+=[0]
    Std+=[point()]
    Sum+=[point()]
    ZArray+=[point()]
    N+=[0]
for i in range(MaxNumStd):
    StdDistance+=[point()]
    StdDisMax+=[0]
    StdDisMaxCor+=[0]
for i in range(TotalNum):
    SAArray+=[[]]
    for j in range(TotalNum):
        SAArray[i]+=[point()]
 
[pointF[0].x,pointF[0].y]=[0.0,0.0]    
[pointF[1].x,pointF[1].y]=[3.0,8.0]
[pointF[2].x,pointF[2].y]=[2.0,2.0]
[pointF[3].x,pointF[3].y]=[1.0,1.0]
[pointF[4].x,pointF[4].y]=[5.0,3.0]
[pointF[5].x,pointF[5].y]=[4.0,8.0]
[pointF[6].x,pointF[6].y]=[6.0,3.0]
[pointF[7].x,pointF[7].y]=[5.0,4.0]
[pointF[8].x,pointF[8].y]=[6.0,4.0]    
[pointF[9].x,pointF[9].y]=[7.0,5.0]
[ZArray[0].x,ZArray[0].y]=[0,0]
#----------------------------------����������
def DistancePoint(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5
def DistancePointF(a,b):
    return ((a.x-b.x)**2+(a.y-b.y)**2)**0.5
def ComputeNumStd(TypeList):
    temp=pointType[7]
    for i in range(6):
        if temp<pointType[i]:
            temp=pointType[i]
    return temp+1
while(CountTime<=StdTime):
    if step==2:
        for i in range(Nc):
            N[i]=0
        print '���ǵ�%d�ι���'%CountTime
        CountTime=CountTime+1
        stdtemp=0
        for i in range(TotalNum):
            dis=65535
            for j in range(Nc):
                ftemp=DistancePointF(pointF[i],ZArray[j])
                if ftemp<dis:
                    stdtemp=j
                    dis=ftemp
            SAArray[stdtemp][N[stdtemp]].x=pointF[i].x
            SAArray[stdtemp][N[stdtemp]].y=pointF[i].y
            N[stdtemp]=N[stdtemp]+1
        for i in range(Nc):
            print "��%d������������:(%d,%d)ӵ��%d��Ԫ��   "%(i,ZArray[i].x,ZArray[i].y,N[i])
            print "������Ԫ���У�"
            for j in range(N[i]):
                print "(%d,%d)"%(SAArray[i][j].x,SAArray[i][j].y)
        step=3   #��ת��������
        #break
    if step==3:
        print"��%d�����ж��Ƿ����ȥ��һЩ"%step
        for i in range(Nc):
            if N[i]<1: #1Ҳ����Ϊ�����β�
                #ȡ����������Ӽ�
                for j in range(TotalNum):
                    if pointType[j]==i:
                        pointType[j]=-1
                tr=i
                while(tr<Nc-1):
                    for m in range(N[tr+1]):
                        SAArray[tr][m].x=SAArray[tr+1][m].x
                        SAArray[tr][m].y=SAArray[tr+1][m].y
                    tr=tr+1
                tr=i
                while(tr<Nc-1):
                    N[tr]=N[tr+1]
                    tr=tr+1
                Nc=Nc-1
        step=4
        for i in range(Nc):
            print "��%d������������:(%d,%d)   "%(i,ZArray[i].x,ZArray[i].y)
            print "������Ԫ���У�"
            for j in range(N[i]):
                print "(%d,%d)"%(SAArray[i][j].x,SAArray[i][j].y)
    #break
    if step==4:
        print"��%d��������������������"%step
        for i in range(Nc):
            temx=0
            temy=0
            for j in range(N[i]):
                temx+=SAArray[i][j].x
                temy+=SAArray[i][j].y
            ZArray[i].x=temx/N[i]
            ZArray[i].y=temy/N[i]
            print N[i]
            print "�������������%dΪ(%f��%f)"%(i,ZArray[i].x,ZArray[i].y)
        step=5
    if step==5:
        print"��%d�������������������������������ĵ�ƽ������"%step
        TempAverage=0
        for i in range(Nc):
            for j in range(N[i]):
                TempAverage+=DistancePointF(SAArray[i][j],ZArray[i])
            AverageD[i]=TempAverage/N[i]
            print "����%d��ƽ������Ϊ%3f"%(i,AverageD[i])
            TempAverage=0
        step=6
        #break
    if step==6:
        print"��%d��������ȫ��ģʽ������Ӧ�������ĵ���ƽ������"%step
        DAv=0
        for i in range(Nc):
            DAv+=N[i]*AverageD[i]
        DAv/=TotalNum
        print"��ƽ������Ϊ%f"%DAv
        #break
        step=7
    if step==7:
        print"��%d�����ж�ת��"%step
        if CountTime>StdTime:
            step=14
            print"���������Ѿ��ﵽ%d��ת�Ƶ���%d��"%(StdTime,step)
        elif Nc<=MaxNumStd:
            step=8
            print"ת�Ƶ���%d���������еľ������"%step            
        elif CountTime%2==0|Nc>2*MaxNumStd:
            step=11
            print"��������Ϊż��ת�Ƶ���%d��"%step
    if step==8:
        print"��%d������������������������׼��"%step
        for i in range(Nc):
            temx=0
            temy=0
            for j in range(N[i]):
                temx+=(SAArray[i][j].x-ZArray[i].x)**2
                temy+=(SAArray[i][j].y-ZArray[i].y)**2
            StdDistance[i].x=(temx/N[i])**0.5
            StdDistance[i].y=(temy/N[i])**0.5
            temx=0.0
            temy=0.0
            print "����%d�ı�׼��Ϊ��%f��%f��"%(i,StdDistance[i].x,StdDistance[i].y)
        step=9
    if step==9:
        print"��%d������ÿ����׼�������е�������"%step
        for i in range(Nc):
            if StdDistance[i].x>StdDistance[i].y:
                StdDisMax[i]=StdDistance[i].x
                StdDisMaxCor[i]=1
            else:
                StdDisMax[i]=StdDistance[i].y
                StdDisMaxCor[i]=0
            print"����%d�еı�׼����������%dΪ%f"%(i,StdDisMaxCor[i],StdDisMax[i]) 
        step=10
    if step==10:
        print"��%d���������жϺͼ���"%step
        temp1=point()
        temp2=point()
        Garma=0.5
        for i in range(Nc):
            if StdDisMax[i]>MaxDiff:
                if((AverageD[i]>DAv)&(N[i]>2*(Nc+1)))|Nc<=MaxNumStd/2:
                    if StdDisMaxCor[i]==0:
                        temp1.x=ZArray[i].x+StdDisMax[i]*Garma
                        temp1.y=ZArray[i].y
                        temp2.x=ZArray[i].x-StdDisMax[i]*Garma
                        temp2.y=ZArray[i].y
                    elif StdDisMaxCor[i]==1:
                        temp1.y=ZArray[i].y+StdDisMax[i]*Garma
                        temp1.x=ZArray[i].x
                        temp2.y=ZArray[i].y-StdDisMax[i]*Garma
                        temp2.x=ZArray[i].x
                    ZArray[i].x=temp1.x
                    ZArray[i].y=temp1.y
                    ZArray[Nc].x=temp2.x
                    ZArray[Nc].y=temp2.y
                    print"����%d������Ϊ����%d�;���%d"%(i,i,Nc)
                    print"���Ѻ�����ķֱ�Ϊ��%f,%f���ͣ�%f,%f��"%(temp1.x,temp1.y,temp2.x,temp2.y)
                    Nc=Nc+1
                    step=2
                    i=Nc
        step=11
    if step==11:
        print"��%d��������ȫ���������ĵľ���"%step
        rank=0
        for i in range(Nc-1):
            j=i+1
            while(j<Nc):
                ZDistance[rank]=DistancePointF(ZArray[i],ZArray[j])
                ZDistanceR[rank]=j
                ZDistanceC[rank]=i
                print"����%d�����%d֮��ľ���Ϊ%f"%(i,j,ZDistance[rank])
                rank+=1
                j=j+1
        step=12
        #break
    if step==12:
        print"��%d�����ҳ���������С��,ֻ����һ��ֻ�ϲ�һ�Ծ������ĵ����"%step
        ZDistanceT=ZDistance[0]
        ZDistanceCT=ZDistanceC[0]
        ZDistanceRT=ZDistanceR[0]
        for i in range(rank):
            if ZDistance[i]<ZDistanceT:
                ZDistanceT=ZDistance[i]
                ZDistanceCT=ZDistanceC[i]
                ZDistanceRT=ZDistanceR[i]
        print "��С�ľ������Ϊ����%d��%d֮��ľ���Ϊ%f"%(ZDistanceCT,ZDistanceRT,ZDistanceT)
        step=13
        #break
    if step==13:
        print"��%d�����ϲ�����"%step
        if(ZDistanceT<MinDistance):
            ZArrayT=point()
            print"���Խ��кϲ�����,�ϲ��������%d��%d�����¾���%d"%(ZDistanceCT,ZDistanceRT,ZDistanceCT)
            ZArrayT.x=(N[ZDistanceCT]*ZArray[ZDistanceCT].x+N[ZDistanceRT]*ZArray[ZDistanceRT].x)/(N[ZDistanceCT]+N[ZDistanceRT])
            ZArrayT.y=(N[ZDistanceCT]*ZArray[ZDistanceCT].y+N[ZDistanceRT]*ZArray[ZDistanceRT].y)/(N[ZDistanceCT]+N[ZDistanceRT])
            print "�������ģ�%f,%f���������ģ�%f��%f���ϲ��ó����µľ�������Ϊ��%f,%f��"%(ZArray[ZDistanceCT].x,ZArray[ZDistanceCT].y,ZArray[ZDistanceRT].x,ZArray[ZDistanceRT].y,ZArrayT.x,ZArrayT.y)
            ZArray[ZDistanceCT].x=ZArrayT.x
            ZArray[ZDistanceCT].y=ZArrayT.y
            i=ZDistanceCT
            while(i<Nc-1):
                ZArray[i].x=ZArray[i+1].x
                ZArray[i].y=ZArray[i+1].y
                i=i+1
            i=ZDistanceCT
            while(i<Nc-1):
                N[i]=N[i+1]
                i+=1
            Nc=Nc-1
        step=14
        #break
    if step==14:
        print"��%d�������һ����ʾ���"%step
        if CountTime>StdTime:
            print"ISODATA�㷨���һ����Ϊ%d��"%Nc
            for i in range(Nc):
                print "��%d������������:(%f,%f)ӵ��%d��Ԫ��   "%(i,ZArray[i].x,ZArray[i].y,N[i])
                print "������Ԫ���У�"
                for j in range(N[i]):
                    print "(%f,%f)"%(SAArray[i][j].x,SAArray[i][j].y)
            break
        else:
            step=2
