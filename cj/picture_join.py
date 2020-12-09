from PIL import Image
import math

def pic_join_10(all_path=[],row_max=2,line_max=5,file_name='十连.png'):
    width_i = 148
    height_i = 148
    num=0
    toImage = Image.new('RGBA',(width_i*line_max,height_i*row_max))
    for j in range(0,row_max):
        for i in range(0,line_max): 
            pic_fole_head =  Image.open(all_path[num])
            width,height =  pic_fole_head.size
            tmppic = pic_fole_head.resize((width_i,height_i))
            loc = (int(i%line_max*width_i),int(j%row_max*height_i))
            #print("第" + str(num) + "存放位置" + str(loc))
            toImage.paste(tmppic,loc)
            num= num+1
            if num >= len(all_path):
                break
    #print(toImage.size)
    toImage.save(file_name)

def pic_join_up(all_path=[]):
    path_num=len(all_path)
    if path_num>3:
        line_max=3
    else:
        line_max=path_num
    row_max=math.ceil(path_num/line_max)
    pic_join_10(all_path,row_max=row_max,line_max=line_max,file_name='抽up.png')