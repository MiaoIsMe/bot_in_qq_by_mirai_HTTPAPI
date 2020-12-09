import http.client
import json
import time
import luck_draw as ld

memu="庙檐开发，目前功能贫瘠，只有学习语言功能（还未移植，作者贼懒，还要人催），第一次输入如‘字段1 & 字段2’的文字，凯露会响应并学会字段1;2.输入:十连;3.输入抽up"
__version__=1.0

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
    def send_message(self,user_id='',ty='text',message='',url='',primary=True):
        conn=self.conn
        def send_primary_text(user_id,text):
            sessionKey=self.sessionKey
            js = json_deal.build_text_json(sessionKey,user_id,text)
            #print(js)
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
            print(data)
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
        if (primary):
            if (ty=='text'):
                send_primary_text(user_id,message)
            elif(ty=='image'):
                send_primary_image(user_id,url,message)
        else:
            if (ty=='text'):
                send_group_text(user_id,message)
            elif(ty=='image'):
                send_group_image(user_id,url,message)
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
                            if(ev.message=="十连"):
                                self.send_message(ev.user_id,'text',chou())
                            elif(ev.message=="抽up"):
                                self.send_message(ev.user_id,'text',chou_up())
                            elif(ev.message=="_help"):
                                self.send_message(ev.user_id,'text',memu)
                        elif(ev.type=='group'):
                            print(ev.group_id,' ',ev.message)
                            if(ev.message=="十连"):
                                self.send_message(ev.group_id,'text',chou(),primary=False)       
                            elif(ev.message=="抽up"):
                                self.send_message(ev.group_id,'text',chou_up(),primary=False)
                            elif(ev.message=="_help"):
                                self.send_message(ev.group_id,'text',memu,primary=False)
            except Exception as e:
                print(e)


class event():
    def __init__(self,i):
        self.id=i['messageChain'][0]['id']
        if(i['type']=='FriendMessage'):
            self.type='primary'
        elif(i['type']=='GroupMessage'):
            self.type='group'
            #MemberMuteEvent不处理
        self.message_type=i['messageChain'][1]['type']
        if(self.message_type=='Face'):
            self.message=i['messageChain'][1]['faceId']
        elif(self.message_type=='Plain'):
            self.message=i['messageChain'][1]['text']
        if(self.type=='primary'):
            self.user_id=i['sender']['id']
        elif(self.type=='group'):
            self.group_id=i['sender']['group']['id']

    
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
    l=ld.choose_stare(10)
    l2=[i.star for i in l]
    dic=ld.list_count(l2,dic)
    st,s=ld.out(dic,l)
    out="本次十连结果:"+st+"\n"+"统计结果"+s
    return out

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