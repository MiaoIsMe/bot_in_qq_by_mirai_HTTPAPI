import psycopg2
import copy
import re

dic_group={}
dic_w={}
dic_private={}
dic_m={}
dic_m["菜单"]="庙檐开发，目前功能贫瘠，只有学习语言功能，第一次输入如‘字段1 & 字段2’的文字，凯露会响应并学会字段1;2.输入:十连;3.输入抽up"

database='bot'
user='postgres'
password='miaoyan528'
host="127.0.0.1"
"""
#database:University
#user:postgres
#password:
host = host,
"""

conn_p=psycopg2.connect(host = host,database=database, user=user, password=password)  #connect to the database
cur = conn_p.cursor()
print("connect successfully")

cur.execute("select * from GROUPID")
group_li=cur.fetchall()

for i in group_li:
    cur.execute("select * from LEXICON_GROUP where groupid=%s" %str(i[0]))
    word_li=cur.fetchall()
    dic_w={}
    if word_li !=[]:
        for k in word_li:
            dic_w[k[1]]=k[2]
        dic_group[i[0]]=copy.copy(dic_w)
    else:
        dic_group[i[0]]={}

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


import http.client
import json
import time
import luck_draw as ld
import picture_join as pj
from collections import defaultdict

__version__=1.2

#从简单入手，慢慢实践
#目前问题，不明原因无法发送图片，只能发送几kb的图，大于此即会无法加载
#这只是第一步，一个简单deemo，只发文字，处理快速，后面要改成多线程
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
                            print(ev.user_id,' ',ev.message)
                            int(ev.user_id)
                            if ev.user_id not in dic_private:
                                cur.execute("insert into PRIVATEID(id) values (%r)" % (str(ev.user_id)))
                                conn_p.commit()
                                dic_private[ev.user_id]={}
                            if ev.user_id in dic_private:
                                msg = ev.message
                                print(msg)
                                l_bo=re.compile(r'\S+ & .*').findall(msg)
                                if l_bo != []:
                                    key,sen=learn_sen(msg)
                                    if key in dic_private[ev.user_id]:
                                        dic_private[ev.user_id][key]=sen
                                        print(dic_private[ev.user_id])
                                        b.send_private_msg(user_id=ev.user_id, message="凯露重学了"+key)
                                        cur.execute("update LEXICON_PRIVATE set sen='%s' where privateid=%s and keyw='%s'" % (sen,str(ev.user_id),key))
                                        conn_p.commit()
                                    else:
                                        dic_private[ev.user_id][key]=sen
                                        print(dic_private[ev.user_id])
                                        b.send_private_msg(user_id=ev.user_id, message="凯露学会了"+key)
                                        cur.execute("insert into LEXICON_PRIVATE(privateid,keyw,sen) values (%s,'%s','%s')" % (str(ev.user_id),key,sen))
                                        conn_p.commit()
                                elif msg in dic_private[ev.user_id]:
                                    b.send_private_msg(user_id=ev.user_id, message=dic_private[ev.user_id][msg])
                                elif(ev.message=="十连"):
                                    message=chou()
                                    url='file:///C:\\Users\\Win\\Desktop\\十连.png'
                                    self.send_private_msg(ev.user_id,'image',message=message,url=url)
                                elif(ev.message=="抽up"):
                                    self.send_private_msg(ev.user_id,'text',chou_up())
                                elif(ev.message=="_help"):
                                    self.send_private_msg(ev.user_id,'text',dic_m["菜单"])
                            
                        elif(ev.type=='group'):
                            print(ev.group_id,' ',ev.message)
                            int(ev.group_id)
                            if ev.group_id not in dic_group:
                                cur.execute("insert into GROUPID(id) values (%r)" %(str(ev.group_id)))
                                conn_p.commit()
                                dic_group[ev.group_id]={}
                            if ev.group_id in dic_group:
                                msg = ev.message
                                print(msg)
                                l_bo=re.compile(r'\S+ & .*').findall(msg)
                                if l_bo != []:
                                    key,sen=learn_sen(msg)
                                    if key in dic_group[ev.group_id]:
                                        dic_group[ev.group_id][key]=sen
                                        print(dic_group[ev.group_id])
                                        b.send_group_msg(group_id=ev.group_id, message="凯露重学了"+key)
                                        cur.execute("update LEXICON_GROUP set sen='%s' where groupid=%s and keyw='%s'" % (sen,str(ev.group_id),key))
                                        conn_p.commit()
                                    else:
                                        dic_group[ev.group_id][key]=sen
                                        print(dic_group[ev.group_id])
                                        b.send_group_msg(group_id=ev.group_id, message="凯露学会了"+key)
                                        cur.execute("insert into LEXICON_GROUP(groupid,keyw,sen) values (%s,'%s','%s')" %(str(ev.group_id),key,sen))
                                        conn_p.commit()
                                elif msg in dic_group[ev.group_id]:
                                    b.send_group_msg(group_id=ev.group_id, message=dic_group[ev.group_id][msg])
                            if(ev.message=="十连"):
                                message=chou()
                                url='file:///C:\\Users\\Win\\Desktop\\十连.png'
                                self.send_group_msg(ev.group_id,'image',message=message,url=url)
                            elif(ev.message=="抽up"):
                                self.send_group_msg(ev.group_id,'text',chou_up())
                            elif(ev.message=="_help"):
                                self.send_group_msg(ev.group_id,'text',dic_m["菜单"])
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
            self.permission=i['sender']['permission']
        self.message_type=i['messageChain'][1]['type']
        if(self.message_type=='Face'):
            self.message=i['messageChain'][1]['faceId']
        elif(self.message_type=='Plain'):
            self.message=i['messageChain'][1]['text']

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

    
class json_deal():
    def build_text_json(sessionKey,target,message):
        sessionKey=sessionKey
        target=target
        dic={
            "sessionKey":sessionKey,
            "target":target,
            "messageChain": [
                {"type": "Plain", "text":message }
            ]
        }
        js = json.dumps(dic)
        return js
    def build_image_json(sessionKey,target,url,message):
        dic={
            "sessionKey":sessionKey,
            "target":target,
            "messageChain": [
                { "type": "Image", "url": url },
                { "type": "Plain", "text": message }
            ]
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
        l_p.append("C:\\Users\\Win\\Desktop\\cj\\图片素材\\%s_加框\\%s_加框.jpg" %(l_star[i],l_n[i]))
    pj.pic_join_10(all_path=l_p)
    s=""
    for i in dic:
        s+=str(i)+"出现次数："+str(dic[i])+"次."
    return s

def chou_up():
    role,dic,l,count=ld.choose_up()
    out="本次抽up,抽中本期up角色%s,共抽%s次," %(role,count)
    if l!=[]:
        s=""
        for i in l:
            s+=str(i)+"、"
        out+="其他三星角色还包括{%s}," %s[:-1]
    s=""
    for i in dic:
        s+=str(i)+"出现次数："+str(dic[i])+"次."
    out+="其中%s" %s
    return out

if __name__ == '__main__':
    b=bot("127.0.0.1",8080)
    b.run()