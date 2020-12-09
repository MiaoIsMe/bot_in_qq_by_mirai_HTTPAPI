#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import os

def add_kuang(star,name,color):
    print("%s\\%s.png %s" %(star,name,color))
    #img=cv2.imread("%s\\%s.png" %(star,name))
    img=cv2.imdecode(np.fromfile("%s\\%s.png" %(star,name),dtype = np.uint8),-1)
    img1=cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_CONSTANT,value=color)
    cv2.imencode('.jpg', img1)[1].tofile('%s_加框\\%s_加框.jpg' %(star,name))
    #cv2.imwrite('%s_加框\\%s_加框.png' %(star,name),img1,[int(cv2.IMWRITE_JPEG_QUALITY),70])

WHITE=[255,255,255]
BLUE=[255,204,102]  #bgr
PINK=[0,215,255]
one=["碧","胡桃","莉玛","伶","铃莓","美咲","日和莉","未奏希","依里","由加莉"]
two=["纺希","宫子","惠理子","栞","空花","铃","铃奈","美冬","美里","美美","千歌","茜里","忍","深月","香织","雪","真阳","珠希","茉莉","绫音"]
three=["初音","纯","姬塔","静流","镜华","璃乃","莫妮卡","妮侬","秋乃","望","咲恋","杏奈","亚里莎","伊莉亚","伊绪","真步","真琴","智","流夏"]
def folder(star):
    if not os.path.exists("%s_加框" %star):
        os.mkdir("%s_加框" %star)

folder("一星")
folder("二星")
folder("三星")
for i in one:
    if not os.path.exists("一星_加框\\%s_加框.jpg" %i):
        add_kuang("一星",i,WHITE)

for i in two:
    if not os.path.exists("二星_加框\\%s_加框.jpg" %i):
        add_kuang("二星",i,BLUE)

for i in three:
    if not os.path.exists("三星_加框\\%s_加框.jpg" %i):
        add_kuang("三星",i,PINK)