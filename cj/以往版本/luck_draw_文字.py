#luck draw
#coding=utf-8
import random

class People():
    def __init__(self,name,star):
        self.name=name
        self.star=star
    def __repr__(self):
        return self.name

one_l=["碧","胡桃","莉玛","伶","铃莓","美咲","日和莉","未奏希","依里","由加莉"]
two_l=["纺希","宫子","惠理子","栞","空花","绫音","铃奈","美冬","美里","美美","千歌","茜里","忍","深月","香织","雪","真阳","珠希","铃","茉莉"]
three_l=["初音","纯","姬塔","静流","镜华","璃乃","莫妮卡","妮侬","秋乃","望","咲恋","杏奈","亚里莎","伊莉亚","伊绪","真步","真琴","智"]
up_l=["克莉丝提娜"]
rate_1=50#三星概率
rate_2=50+180#二星概率
rate_up=7
#rate_3=79

one=[People(one_l[i],"一星") for i in range(len(one_l))]
two=[People(two_l[i],"二星") for i in range(len(two_l))]
three=[People(three_l[i],"三星") for i in range(len(three_l))]
up=[People(up_l[i],"up") for i in range(len(up_l))]

def choose_up(rate_up=rate_up,rate_1=rate_1,rate_2=rate_2,up=up,three=three):
    dic={"三星":0,"二星":0,"一星":0}
    l=[]
    l2=[]
    count=0
    while True:
        i=random.randint(0,1000)
        count+=1
        if count%10==0:
            count=count%10
            if l2==[]:
                if i<rate_up:
                    dic["三星"]+=1
                    role=random.choice(up)
                    return role,dic,l,dic["一星"]+dic["二星"]+dic["三星"]
                elif i<rate_1:
                    dic["三星"]+=1
                else:
                    dic["二星"]+=1
            else:
                l2=[]
        else:   
            if i<rate_up:
                dic["三星"]+=1
                role=random.choice(up)
                return role,dic,l,dic["一星"]+dic["二星"]+dic["三星"]
            elif i<rate_1:
                l.append(random.choice(three))
                l2.append("三星")
                dic["三星"]+=1
            elif i<rate_2:
                l2.append("二星")
                dic["二星"]+=1
            else:
                dic["一星"]+=1

def choose_stare(time=10,rate_1=rate_1,rate_2=rate_2):
    l=random.sample(range(0,1000),9)
    l2=[]
    for i in range(len(l)):
        if l[i]<rate_up:
            l[i]=random.choice(up)
            l2.append(i)
        elif l[i] < rate_1:
            l[i]=random.choice(three)
            l2.append(i)
        elif l[i]<rate_2:
            l[i]=random.choice(two)
            l2.append(i)
        else:
            l[i]=random.choice(one)
    if l2 ==[]:
        i=random.randint(0,1000)
        if i<rate_1:
            l.append(random.choice(three))
        else:
            l.append(random.choice(two))
    else:
        l.append(random.choice(one))
    return l

def list_count(l,dic={}):
    l2=set(l)
    for i in l2:
        dic[i]=l.count(i)
    return dic

def out(dic,l):
    st=""
    for i in l:
        if i.star=="一星":
            st+=str(i)+"、"
        elif i.star=="二星":
            st+="#"+str(i)+"#"+"、"
        elif i.star=="up":
            st+="-*-"+str(i)+"*-*-*"+"、"
        else:
            st+="**"+str(i)+"**"+"、"
    s=""
    for i in dic:
        s+=str(i)+"出现次数："+str(dic[i])+"次."
    
    return st,s

#l=choose_stare(10,rate_1,rate_2)    
#dic=list_count(l)
#print(l)