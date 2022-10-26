import json
import os
import xml.etree.ElementTree as ET
import cv2
 
 
# 标准化输出x, y, w, h格式
# 将x1, y1, x2, y2转换成yolov5所需要的x, y, w, h格式
def xyxy2xywh(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[2]) / 2 * dw
    y = (box[1] + box[3]) / 2 * dh
    w = (box[2] - box[0]) * dw
    h = (box[3] - box[1]) * dh
    return (x, y, w, h) 
 
 
def json2txt(path):
    #print(len(os.listdir(path)))
    pic_path = 'E:/Desktop/pv/pic'  # 原始图片路径
    txt_out_path = './backgr' # 转换后txt保存路径
    # 遍历每一个json文件
    for file in os.listdir(path):
        print(file)
        if "json" in str(file):
            with open(os.path.join(path, file), 'r') as f:
                data = json.load(f)
                #print(data)
                points = data['shapes'][0]['points']
                pic = file.split('.')[0]+'.png'
                pic_name = os.path.join(pic_path, pic)
                txt_name = file.split(".")[0] + ".txt"
                imread = cv2.imread(pic_name)
                h = imread.shape[0]
                w = imread.shape[1]
                print(imread.shape)
                xmin = points[0][0]
                ymin = points[0][1]
                xmax = points[2][0]
                ymax = points[2][1]
                box = [float(xmin), float(ymin), float(xmax),
                       float(ymax)]
                #print(box)
                # # 将x1, y1, x2, y2转换成yolov5所需要的x, y, w, h格式
                bbox = xyxy2xywh((w, h), box)
                print(bbox)
 
                # # 写入目标文件中，格式为 id x y w h
                with open(os.path.join(txt_out_path, txt_name), 'w') as out_file:
                    out_file.write(str(1) + " " + " ".join(str(x) for x in bbox) + '\n')
                out_file.close()
                #exit()
 
 
if __name__ == '__main__':
    # json格式数据路径
    jsonpath = './json'
    json2txt(jsonpath)