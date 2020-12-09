#bot
from aiocqhttp import CQHttp,Event
import re
import psycopg2
import getpass
import copy
import luck_draw as ld

bot = CQHttp(access_token='3498250046', enable_http_post=False)
dic_group={}
dic_w={}
dic_private={}
dic_m={}
dic_m["菜单"]="庙檐开发，目前功能贫瘠，只有学习语言功能，第一次输入如‘字段1 & 字段2’的文字，凯露会响应并学会字段1;2.输入:十连;3.输入抽up"

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

conn=psycopg2.connect(host = host,database=database, user=user, password=password)  #connect to the database
cur = conn.cursor()
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

@bot.on_message('private')
async def _(event: Event):
    try:
        if event.user_id not in dic_private:
            cur.execute("insert into PRIVATEID(id) values (%r)" % (str(event.user_id)))
            conn.commit()
            dic_private[event.user_id]={}
        if event.user_id in dic_private:
            msg = event.message
            print(msg)
            l_bo=re.compile(r'\S+ &amp; \S+').findall(msg)
            if l_bo != []:
                key,sen=learn_sen(event)
                if key in dic_private[event.user_id]:
                    dic_private[event.user_id][key]=sen
                    print(dic_private[event.user_id])
                    await bot.send_private_msg(user_id=event.user_id, message="凯露重学了"+key)
                    cur.execute("update LEXICON_PRIVATE set sen='%s' where privateid=%s and keyw='%s'" % (sen,str(event.user_id),key))
                    conn.commit()
                else:
                    dic_private[event.user_id][key]=sen
                    print(dic_private[event.user_id])
                    await bot.send_private_msg(user_id=event.user_id, message="凯露学会了"+key)
                    cur.execute("insert into LEXICON_PRIVATE(privateid,keyw,sen) values (%s,'%s','%s')" % (str(event.user_id),key,sen))
                    conn.commit()
            elif msg in dic_private[event.user_id]:
                await bot.send_private_msg(user_id=event.user_id, message=dic_private[event.user_id][msg])
            elif msg=="十连":
                await bot.send_private_msg(user_id=event.user_id, message="%s" %chou())
            elif msg=="抽up":
                await bot.send_private_msg(user_id=event.user_id, message="%s" %chou_up())
            elif msg=="_菜单":
                print("发送菜单")
                await bot.send_private_msg(user_id=event.user_id, message=dic_m["菜单"])
    except Exception as e:
        print (e)
    
def chou():
    dic={}
    l=ld.choose_stare(10)
    l2=[i.star for i in l]
    dic=ld.list_count(l2,dic)
    st,s=ld.out(dic,l)
    out="本次十连结果:"+st+"[CQ:enter]"+"统计结果"+s
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

def learn_sen(event:Event):
    msg=event.message
    print(re.compile(r' &amp; \S+').findall(msg))
    key=re.compile(r'\S+ &amp; ').findall(msg)[0][:-7]
    sen=re.compile(r' &amp; \S+').findall(msg)[0][7:]
    return key,sen

@bot.on_message('group')
async def _(event: Event):
    try:
        if event.group_id not in dic_group:  # 群号
            cur.execute("insert into GROUPID(id) values (%r)" %(str(event.group_id)))
            conn.commit()
            dic_group[event.group_id]={}
        if event.group_id in dic_group:
            msg = event.message
            print(msg)
            l_bo=re.compile(r'\S+ &amp; \S+').findall(msg)
            if l_bo != []:
                key,sen=learn_sen(event)
                if key in dic_group[event.group_id]:
                    dic_group[event.group_id][key]=sen
                    print(dic_group[event.group_id])
                    await bot.send_group_msg(group_id=event.group_id, message="凯露重学了"+key)
                    cur.execute("update LEXICON_GROUP set sen='%s' where groupid=%s and keyw='%s'" % (sen,str(event.group_id),key))
                    conn.commit()
                else:
                    dic_group[event.group_id][key]=sen
                    print(dic_group[event.group_id])
                    await bot.send_group_msg(group_id=event.group_id, message="凯露学会了"+key)
                    cur.execute("insert into LEXICON_GROUP(groupid,keyw,sen) values (%s,'%s','%s')" %(str(event.group_id),key,sen))
                    conn.commit()
            elif msg in dic_group[event.group_id]:
                await bot.send_group_msg(group_id=event.group_id, message=dic_group[event.group_id][msg])
            elif msg=="十连":
                await bot.send_group_msg(group_id=event.group_id, message="%s" %chou())
            elif msg=="抽up":
                await bot.send_group_msg(group_id=event.group_id, message="%s" %chou_up())
            elif msg=="_菜单":
                print("发送菜单")
                await bot.send_group_msg(group_id=event.group_id, message=dic_m["菜单"])
    except Exception as e:
        print (e)

if __name__ == '__main__':
    bot.run(host = '127.0.0.1', port = 5)

"""
async def handle_msg(context):
    await bot.send(context, '现在为您复读：')
    return {'reply': context['message']}

@bot.on_message('group')
async def _(event: Event):
    available = [1061750983]  # 群号
    if event.group_id in available:
        msg = event.message
        # 常用的比如 event.message, event.user_id, event.group_id
        msg = msg.replace("你", "我")
        msg = msg.replace("吗", "")
        msg = msg.replace("？", "！")
        await bot.send_group_msg(group_id=event.group_id, message=msg)
    # return {'reply': event.message}
"""

#cursor.execute("insert into people values (%s, %s)", (who, age))
"""
cur.execute("insert into LEXICON(groupid,keyw,sen) values (%s,%s,%s)",(str(849710371),"'测试使用'","'正常运行'"))
cur.commit()


cur.execute("insert into Time(day) values (%r)" %(str(date)))    #execute() for entering one line command of SQL

for i in data:
    cur.execute("insert into rank(day,名次,作品名称,url,up_id,up_名称,综合热度) values (%r,%r,%r,%r,%r,%r,%r)" %(str(date),i["名次"],i["作品名称"],i["url"],i["up_id"],i["up_名称"],i["综合热度"]))
print("Data enter")
conn.commit()
"""
