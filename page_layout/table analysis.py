# coding: utf-8
import os
import os.path
import fnmatch
import subprocess
import re
from collections import OrderedDict
from docx import Document
from docx.shared import Pt
from docx.shared import Inches
import cv2
import numpy as np
"""
直接调用shell
"""
#中英文写入规则不一样
languange='chi_sim_lstm'
show_box='false'
picture_format='jpg'
compen=5 #crop余量，有时候会超过图片范围

def image_None_rectangle_crop(image,width,point_list):
    mask = np.zeros(image.shape, dtype=np.uint8)
    coners_list=[(point[0],width-point[1]) for point in point_list]
    roi_corners = np.array([coners_list],dtype=np.int32)
    # fill the ROI so it doesn't get wiped out when the mask is applied
    if len(image.shape)==2:
        channel_count = 1  # i.e. 3 or 4 depending on your image
    else:
        channel_count=image.shape[-1]
    ignore_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    return cv2.bitwise_and(image, mask)


def image_crop(img,width,compensation,point_1,point_3):
    x1 = width - point_1[1] - compensation
    x2 = width - point_3[1] + compensation
    y1 = point_1[0] - compensation
    y2 = point_3[0] + compensation
    return img[x1:x2, y1:y2]


def filter_box(box_dict,height,width,filter_param_height,filter_param_width):
    """
    :param box_dict: raw box
    :param width:  image_width
    :param height:   image_height
    :return:
    """
    med_dic=box_dict.copy()
    print("raw boxes number: {}".format(len(med_dic)))
    new_dict={}
    for i in range(len(med_dic)):
        if len(med_dic[i])==5:
            point_1 = med_dic[i][0]
            point_3 = med_dic[i][2]
            type=med_dic[i][4]
        else:
            #后面可做连通图截取过程
            max_width=0
            min_width=10000
            max_height=0
            min_height=10000
            for point in med_dic[i][:-1]:
                if point[1]>max_width:
                    max_width=point[1]
                if point[1]<min_width:
                    min_width=point[1]
                if point[0]>max_height:
                    max_height=point[0]
                if point[0]<min_height:
                    min_height=point[0]
            point_1=(min_height,max_width)
            point_3=(max_height,min_width)
            type = med_dic[i][-1]

        box_width = point_1[1] - point_3[1]
        box_height = point_3[0] - point_1[0]
        #box只保留大段文字，图片，表格
        #针对表格和图片 width 垂直长度  height水平长度
        #这里只对规则的文本进行处理，多边形区域直接滤去了
        if type==19 or box_width<filter_param_width*width or box_height<filter_param_height*height:
            print("del box {}".format(i))
            del box_dict[i]
        else:
            #针对图片进行判断
            if type==3 and box_width<filter_param_width*5*width:
                print("del box {}".format(i))
                del box_dict[i]
        if i in box_dict.keys():
            new_dict[i] = [point_1, point_3, type]
    #对字典进行重排
    d = OrderedDict(sorted(new_dict.items(), key=lambda t: t[0]))
    d_raw=OrderedDict(sorted(box_dict.items(), key=lambda t: t[0]))
    return_dict={}
    return_dict_raw={}
    for i,item in enumerate(d):
    #重新编号字典
        return_dict[i]=d[item]
        return_dict_raw[i]=d_raw[item]
    print("final boxes number: {}".format(len(box_dict)))
    return return_dict,return_dict_raw

def crop_image(org_path,docx_path,result_path="./box_result.txt"):
    #write object
    document = Document()
#picture preprocessing
    # crop = cv2.addWeighted(crop, 4, cv2.blur(crop, (30, 30)), -4, 128)
    # kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    # crop = cv2.filter2D(crop, -1, kernel)
    #显示crop
    # cv2.imshow("image", crop)
    # cv2.waitKey(0)
    # 提取信息
    out_path=org_path.replace('.{}'.format(picture_format),'')
    #os.environ['SCROLLVIEW_PATH'] = "/Users/xiongfei/tesseract/java"
        #对于表格先出去直线：主要要看脚本的参数形式
        #-negate replace every pixel with its complementary color
        #-morphology morphology analysis
        #-define
    subprocess.call(["convert",org_path,
                     "-type","Grayscale",
                     "-negate",
                     "-define", "morphology:compose=darken",
                     "-morphology","Thinning",'Rectangle:1x80+0+0<',
                     "-negate",
                     org_path])
    #纯文字识别 --psm 最好的效果，并且保持了文字的顺序
    os.environ['SCROLLVIEW_PATH'] = "/Users/xiongfei/tesseract/java"
    subprocess.call(["tesseract", org_path, out_path,
                        "-l",languange,
                     #分块识别6针对文字块，采用--psm 6最好
                        "--psm", "6",
                        "-c","Recognize_choice=True",
                        "-c", "textord_tabfind_show_blocks={}".format(show_box),
                        "-c", "plot_choice={}".format(show_box),
                        "-c", "plot_choice_double={}".format(show_box),
                        "-c", "plot_third={}".format(show_box)
                        ])
    print("detection table, writing...")
    table_path = org_path.replace('.{}'.format(picture_format), '.txt')
    with open(table_path,'r') as f:
        all=f.read().strip().split('\n')
    #filter none line
    while '' in all:
        all.remove('')
    lens=len(all)
    table = document.add_table(lens, 1)
    for i in range(lens):
        table.cell(i,0).text=all[i]
    print("complete writing table")
    table.style='Table Grid'
    document.save(docx_path)
def execute(root_path):
    #os.walk存在隐藏文件，需要忽略
    for dirpath, _, filenames in os.walk(root_path):
        med=filenames.copy()
        for filename in med:
            if filename.startswith('.') or filename.endswith('.txt'):
                filenames.remove(filename)
        print(filenames)
        filenames.sort(key=lambda x: int(re.findall('(\d*).{}'.format(picture_format),x)[0]))
        for filename in filenames:
            if os.path.exists("./box_result.txt"):
                os.remove("./box_result.txt")
            print(filename)
            if fnmatch.fnmatch(filename, "*.{}".format(picture_format)):
                org_path = os.path.join(dirpath, filename)
                print("table analysis {}".format(org_path))
                crop_image(org_path,filename.replace(picture_format,'docx'))
if __name__ == '__main__':
    #root_path = input("target folder path>")
    root_path="./convert_image/test"
    execute(root_path)