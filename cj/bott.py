import psycopg2
import copy
import os
import random
import re
import http.client
import json
import time
import luck_draw as ld
import picture_join as pj
from collections import defaultdict

dic_group={}
dic_private={}
dic_m={}
dic_m["菜单"]="庙檐开发，目前功能贫瘠，只有学习语言功能，第一次输入如‘字段1 & 字段2’的文字，凯露会响应并学会字段1;2.输入:十连;3.输入抽up"
group_pic_all_d ={}
group_pic_now_d={}
all_pic_d={}
fo='推荐'
basePath="C:\\Users\\Administrator\\Desktop\\cj\\图片素材\\搜索库\\"

database='bot'
user='postgres'
password='00000000'
host="127.0.0.1"
"""
#database:University
#user:postgres
#password:
host = host,
"""
from pixivpy3 import *

api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
# api.set_additional_headers({'Accept-Language':'en-US'})
api.set_accept_language('zh-cn')
api.login('Pixiv账号','Pixiv密码')

def renew_pic(all_pic_d,group_pic_now_d,group_pic_all_d,group_id,fo='推荐',basePath="C:\\Users\\Administrator\\Desktop\\cj\\图片素材\\搜索库\\"):
    l_tem=[int(i[:-4]) for i in all_pic_d[group_id][fo]]#当前路径的id
    de_fi_l(group_pic_now_d[group_id][fo],os.path.join(basePath,str(group_id),fo))#删除以及浏览过的图片文件,now的
    group_pic_now_d[group_id][fo]=[]#清空now的图片id
    all_pic_d[group_id]=renew_path(basePath+str(group_id))[1]#再次查看当前图片目录，删完后为缺失状态
    l_tem=[i[:-4] for i in all_pic_d[group_id][fo]]#缺失状态下当前id
    get_recom_pic(api, l_tem , group_pic_all_d[group_id][fo],dir_path=os.path.join(basePath, str(group_id),fo))#当前缺失图片id目录，所有已使用的图片id目录
    #抓取的
    all_pic_d[group_id]=renew_path(basePath+str(group_id))[1]#刷新所有路径
    return all_pic_d,group_pic_now_d

def build_fo(file_name,basePath="C:\\Users\\Administrator\\Desktop\\cj\\图片素材\\搜索库\\"):
    if not os.path.exists(os.path.join(basePath,file_name)):
        """判断文件夹是否存在，不存在则创建文件夹"""
        os.mkdir(os.path.join(basePath, file_name))
        print(file_name+"文件夹创造完成")
    else:
        print(file_name+"文件夹已存在")
#推荐
def get_recom_pic(api,l,l_all,dir_path):
    json_result = api.illust_recommended()
    #print(json_result)
    illusts = json_result.illusts
    for i in illusts:
        if(len(l)>=50):
                break
        if (i["id"] not in l_all):
            l.append(i["id"])
            print(">>> %s, origin url: %s" % (i.title, i.image_urls['large']))
            api.download(i.image_urls['large'], path=dir_path, name=str(i["id"])+".jpg")#replace=True
    while (len(l)<50):
        next_qs = api.parse_qs(json_result.next_url)
        json_result = api.illust_recommended(**next_qs)
        illusts = json_result.illusts
        for i in illusts:
            if (i["id"] not in l_all):
                l.append(i["id"])
                print(">>> %s, origin url: %s" % (i.title, i.image_urls['large']))
                api.download(i.image_urls['large'], path=dir_path, name=str(i["id"])+".jpg")#replace=True

conn_p=psycopg2.connect(host = host,database=database, user=user, password=password)  #connect to the database
cur = conn_p.cursor()
print("connect successfully")
dir_path="C:\\Users\\Administrator\\Desktop\\cj\\图片素材\\搜索库\\"

def renew_path(dir_path="C:\\Users\\Administrator\\Desktop\\cj\\图片素材\\搜索库\\"):
    folder_l=os.listdir(dir_path)
    all_p={}
    for folder in folder_l:
        file_l=[]
        one_folder_path=os.path.join(dir_path,folder)
        for file in os.listdir(one_folder_path):
            if ('jpg' in file) or ('png' in file):
                file_l.append(file)
        all_p[folder]=file_l
    return folder_l,all_p

def de_fi_l(l=[],basePath=''):
    for i in l:
        if os.path.exists(os.path.join(basePath,str(i)+'.jpg')):
            os.remove(os.path.join(basePath,str(i)+'.jpg'))
        else:
            print('不存在文件'+i+'.jpg')

cur.execute("select * from GROUPID")
group_li=cur.fetchall()

for i in group_li:
    build_fo(str(i[0]))
    build_fo("推荐",basePath+str(i[0]))
    all_pic_d[i[0]]=renew_path(basePath+str(i[0]))[1]
    cur.execute("select * from LEXICON_GROUP where groupid=%s" %str(i[0]))
    word_li=cur.fetchall()
    dic_w={}
    if word_li !=[]:
        for k in word_li:
            dic_w[k[1]]=k[2]
        dic_group[i[0]]=copy.copy(dic_w)
    else:
        dic_group[i[0]]={}
    cur.execute("select * from PIC_GROUP where groupid=%s" %str(i[0]))
    folder_pic_li=cur.fetchall()
    group_folder=defaultdict(list)
    if folder_pic_li !=[]:
        for k in folder_pic_li:
            group_folder[k[1]].append(k[2])
    
    group_pic_all_d[i[0]]=copy.copy(group_folder)
    """
    cur.execute("select * from PIC_NOW_GROUP where groupid=%s" %str(i[0]))
    PIC_NOW_f_li=cur.fetchall()
    if PIC_NOW_f_li !=[]:
        folder_now_d[i[0]]=copy.copy(PIC_NOW_f_li[0][1])
    else:
        folder_now_d[i[0]]=random.choice(folder_l)
    """
    cur.execute("select * from PIC_GROUP_NOW where groupid=%s" %str(i[0]))
    folder_pic_li=cur.fetchall()
    group_folder=defaultdict(list)
    if folder_pic_li !=[]:
        for k in folder_pic_li:
            group_folder[k[1]].append(k[2])
    group_pic_now_d[i[0]]=copy.copy(group_folder)
    renew_pic(all_pic_d,group_pic_now_d,group_pic_all_d,i[0],fo='推荐',basePath=basePath)
    

cur.execute("select * from PRIVATEID")
private_li=cur.fetchall()

for i in private_li:
    cur.execute("select * from LEXICON_PRIVATE where privateid=%s" %str(i[0]))
    word_li=cur.fetchall()
    dic_w={}
    if word_li !=[]:
        for k in word_li:
            dic_w[k[1]]=k[2]
        dic_private[i[0]]=copy.copy(dic_w)
    else:
        dic_private[i[0]]={}

#数据导入

def learn_sen(msg:str):
    key=re.compile(r'\S+ & ').findall(msg)[0][:-3]
    sen=re.compile(r' & .*').findall(msg)[0][3:]
    return key,sen

__version__=1.5
class bot():
    def __init__(self,address,port=8080,authKey=1234567890):
        self.conn = http.client.HTTPConnection(address,port)
        self.authKey=authKey
        self.sessionKey=self.bind()
    def bind(self):
        auth = json.dumps({"authKey":self.authKey})
        #print(str)
        #headers = {}
        conn=self.conn
        conn.request('POST', '/auth', auth)
        response = conn.getresponse()
        #print(response.status, response.reason)
        session = response.read().decode('utf-8')
        print(session)
        sessionKey=json.loads(session)['session']
        bind=json.dumps({"sessionKey":sessionKey,"qq": 3498250046 })
        conn.request('POST', '/verify', bind)
        response = conn.getresponse()
        #print(response.status, response.reason)
        data = response.read().decode('utf-8')
        print(data)
        return sessionKey
    def send_private_msg(self,user_id='',ty='text',message='',url=''):
        conn=self.conn
        def send_primary_text(user_id,text):
            sessionKey=self.sessionKey
            js = json_deal.build_text_json(sessionKey,user_id,text)
            print(js)
            conn.request('POST', '/sendFriendMessage', js)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            print(data)
        def send_primary_image(user_id,url,message):
            sessionKey=self.sessionKey
            js = json_deal.build_image_json(sessionKey,user_id,url,message)
            conn.request('POST', '/sendFriendMessage', js)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            #print(data)
        if (ty=='text'):
            send_primary_text(user_id,message)
        elif(ty=='image'):
            send_primary_image(user_id,url,message)

    def send_group_msg(self,group_id='',ty='text',message='',url=''):
        conn=self.conn
        def send_group_text(group_id,text):
            sessionKey=self.sessionKey
            js = json_deal.build_text_json(sessionKey,group_id,text)
            #print(js)
            conn.request('POST', '/sendGroupMessage', js)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            print(data)
        def send_group_image(group_id,url,message):
            sessionKey=self.sessionKey
            js = json_deal.build_image_json(sessionKey,group_id,url,message)
            conn.request('POST', '/sendGroupMessage', js)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            print(data)
        if (ty=='text'):
            send_group_text(group_id,message)
        elif(ty=='image'):
            send_group_image(group_id,url,message)
    def send_group_m_i_m(self,group_id,url,message1,message2):
        sessionKey=self.sessionKey
        messageChain=[
            json.loads(json_deal.build_dic_for_json(ty='text',text=message1)),
            json.loads(json_deal.build_dic_for_json(ty='image',url=url)),
            json.loads(json_deal.build_dic_for_json(ty='text',text=message2))
        ]
        js = json_deal.build_mix_json(sessionKey,group_id,messageChain=messageChain)
        self.conn.request('POST', '/sendGroupMessage', js)
        response = self.conn.getresponse()
        data = response.read().decode('utf-8')
        print(data)

    def run(self):
        conn=self.conn
        sessionKey=self.sessionKey
        while 1:
            time.sleep(1)
            try:
                conn.request('GET', '/fetchLatestMessage?sessionKey='+sessionKey+'&count=10')
                response = conn.getresponse()
                #print(response.status, response.reason)
                data = response.read().decode('utf-8')
                #print(data)
                j = json.loads(data)
                if j["data"]!=[]:
                    for i in j["data"]:
                        print(i)
                        ev=event(i)
                        print(ev.type,' ',end='')
                        if (ev.type=='primary'):
                            pass
                        elif(ev.type=='group'):
                            print(ev.group_id,' ',ev.message)
                            int(ev.group_id)
                            if ev.group_id not in dic_group:
                                cur.execute("insert into GROUPID(id) values (%r)" %(str(ev.group_id)))
                                conn_p.commit()
                                dic_group[ev.group_id]={}
                                build_fo(str(ev.group_id))
                                build_fo("推荐",basePath+str(ev.group_id))
                                self.send_group_msg(group_id=ev.group_id, message="获取图片资源")
                                get_recom_pic(api,[])
                            if(ev.message=="十连"):
                                threading.Thread(target=threading_chou,args=(self,ev)).start()
                            elif(ev.message=="抽up"):
                                threading.Thread(target=threading_chou_up,args=(self,ev)).start()
                            elif(ev.message=="_help"):
                                self.send_group_msg(ev.group_id,'text',dic_m["菜单"])
                            elif(ev.message=="凯露来一张"):
                                #如果一直查找的话，不会出现full的情况
                                if ev.group_id in dic_group:
                                    global all_pic_d,group_pic_now_d
                                    all_pic_d[ev.group_id]=renew_path(basePath+str(ev.group_id))[1]
                                    l_p=[i for i in all_pic_d[ev.group_id][fo] if i not in group_pic_all_d[ev.group_id][fo]]
                                    one_pic=random.choice(l_p)
                                    one_p_path=basePath+str(ev.group_id)+"\\"+fo+"\\"+one_pic
                                    group_pic_now_d[ev.group_id][fo].append(one_pic)
                                    group_pic_all_d[ev.group_id][fo].append(one_pic)
                                    self.send_group_msg(ev.group_id,'image',url="file:///"+one_p_path)
                                    print(dic_group[ev.group_id],' ',fo,' ',one_pic)
                                    cur.execute("insert into PIC_GROUP(groupid,forder_n,pic_l) values (%s,'%s','%s')" %(str(ev.group_id),fo,one_pic))
                                    conn_p.commit()
                                    cur.execute("insert into PIC_GROUP_NOW(groupid,forder_n,pic_l) values (%s,'%s','%s')" %(str(ev.group_id),fo,one_pic))
                                    conn_p.commit()
                                    if len(group_pic_now_d[ev.group_id][fo])/len(all_pic_d[ev.group_id][fo]) >0.1:
                                        api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
                                        api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
                                        # api.set_additional_headers({'Accept-Language':'en-US'})
                                        api.set_accept_language('zh-cn')
                                        api.login('PIX账号','PIX密码')
                                        all_pic_d,group_pic_now_d=renew_pic(all_pic_d,group_pic_now_d,group_pic_all_d,ev.group_id)
                                        cur.execute("TRUNCATE PIC_GROUP_NOW RESTART IDENTITY;" %())
                                        conn_p.commit()
                            elif(ev.message=="凯露显示画夹使用进度"):
                                s=fo+":\n已使用"+str(len(group_pic_all_d[ev.group_id][fo]))+"张,总计:"+str(len(all_pic_d[ev.group_id][fo]))+"张"
                                self.send_group_msg(ev.group_id,'text',s)
                            elif ev.group_id in dic_group:
                                msg = ev.message
                                print(msg)
                                l_bo=re.compile(r'\S+ & .*').findall(msg)
                                if l_bo != []:
                                    key,sen=learn_sen(msg)
                                    if key in dic_group[ev.group_id]:
                                        dic_group[ev.group_id][key]=sen
                                        print(dic_group[ev.group_id])
                                        self.send_group_msg(group_id=ev.group_id, message="凯露重学了"+key)
                                        cur.execute("update LEXICON_GROUP set sen='%s' where groupid=%s and keyw='%s'" % (sen,str(ev.group_id),key))
                                        conn_p.commit()
                                    else:
                                        dic_group[ev.group_id][key]=sen
                                        print(dic_group[ev.group_id])
                                        self.send_group_msg(group_id=ev.group_id, message="凯露学会了"+key)
                                        cur.execute("insert into LEXICON_GROUP(groupid,keyw,sen) values (%s,'%s','%s')" %(str(ev.group_id),key,sen))
                                        conn_p.commit()
                                elif msg in dic_group[ev.group_id]:
                                    self.send_group_msg(group_id=ev.group_id, message=dic_group[ev.group_id][msg])
            except Exception as e:
                print(e)


class event():
    def __init__(self,i):
        self.id=i['messageChain'][0]['id']
        if(i['type']=='FriendMessage'):
            self.type='primary'
            self.user_id=i['sender']['id']
        elif(i['type']=='GroupMessage'):
            self.type='group'
            self.group_id=i['sender']['group']['id']
            #MemberMuteEvent不处理
            self.memberName=i['sender']['memberName']
            self.permission=i['sender']['permission']
        self.message_type=i['messageChain'][1]['type']
        if(self.message_type=='Face'):
            self.message=i['messageChain'][1]['faceId']
        elif(self.message_type=='Plain'):
            self.message=i['messageChain'][1]['text']

                
import threading
#threading.Thread(target=None,args=())

def threading_chou(b:bot,ev=event):
    #b.send_group_msg(ev.group_id,'text',message='凯露在运行')
    b.send_group_msg(ev.group_id,'text',message='图片生成将耗时3s左右,'+ev.memberName+'请耐心等待')
    message=chou()
    url='file:///C:\\Users\\Administrator\\Desktop\\cj\\十连.png'
    b.send_group_msg(ev.group_id,'image',message=message,url=url)

def threading_chou_up(b:bot,ev=event):
    #b.send_group_msg(ev.group_id,'text',message='凯露在运行')
    b.send_group_msg(ev.group_id,'text',message='图片生成将耗时0-2s,'+ev.memberName+'请耐心等待')
    message1,message2=chou_up()
    url='file:///C:\\Users\\Administrator\\Desktop\\cj\\抽up.png'
    b.send_group_m_i_m(ev.group_id,url=url,message1=message1,message2=message2)

class json_deal():
    def build_dic_for_json(ty='text',text='',url=''):
        out = defaultdict(str)
        if ty=='text':
            out["type"]="Plain"
            out["text"]=text
        elif ty=='image':
            out["type"]="Image"
            out["url"]=url
        js=json.dumps(out)
        return js
    def build_text_json(sessionKey,target,message=''):
        dic={
            "sessionKey":sessionKey,
            "target":target,
            "messageChain": [json.loads(json_deal.build_dic_for_json(ty='text',text=message))]
        }
        js = json.dumps(dic)
        return js
    def build_image_json(sessionKey,target,url='',message=''):
        dic={
            "sessionKey":sessionKey,
            "target":target,
            "messageChain": [
                json.loads(json_deal.build_dic_for_json(ty='image',url=url)),
                json.loads(json_deal.build_dic_for_json(ty='text',text=message))
            ]
        }
        js = json.dumps(dic)
        return js
    def build_mix_json(sessionKey,target,messageChain=[]):
        dic={
            "sessionKey":sessionKey,
            "target":target,
            "messageChain": messageChain
        }
        js = json.dumps(dic)
        return js            

def chou():
    dic={}
    l_n=ld.choose_stare(10)
    l_star=[i.star for i in l_n]
    dic=ld.list_count(l_star,dic)
    l_p=[]
    for i in range(10):
        l_p.append("C:\\Users\\Administrator\\Desktop\\cj\\图片素材\\%s_加框\\%s_加框.jpg" %(l_star[i],l_n[i]))
    pj.pic_join_10(all_path=l_p)
    s=""
    for i in dic:
        s+=str(i)+"出现次数："+str(dic[i])+"次."
    return s

def chou_up():
    role,dic,l,count=ld.choose_up()
    print(role)
    out1="本次抽up,抽中本期up角色%s,共抽%s次," %(role,count)
    print(l)
    print(dic['三星'])
    l_p=[]
    fo='三星'
    l_p.append("C:\\Users\\Administrator\\Desktop\\cj\\图片素材\\%s_加框\\%s_加框.jpg" %(fo,role))
    if l!=[]:
        out1+="三星角色总览:\n"
        for i in l:
            l_p.append("C:\\Users\\Administrator\\Desktop\\cj\\图片素材\\%s_加框\\%s_加框.jpg" %(fo,str(i)))
    pj.pic_join_up(all_path=l_p)
    s=""
    for i in dic:
        s+=str(i)+"出现次数："+str(dic[i])+"次."
    out2="其中%s" %s
    return out1,out2

if __name__ == '__main__':
    b=bot("127.0.0.1",8080)
    b.run()