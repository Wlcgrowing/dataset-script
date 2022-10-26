#实现voc数据集格式(.xml)-->coco数据集格式(.json)

import os
import shutil
import numpy as np
import json
import xml.etree.ElementTree as ET
# 检测框的ID起始值
START_BOUNDING_BOX_ID = 1
# 类别列表无必要预先创建，程序中会根据所有图像中包含的ID来创建并更新
PRE_DEFINE_CATEGORIES = {}
# If necessary, pre-define category and its id
PRE_DEFINE_CATEGORIES = {"crazing": 1, "inclusion": 2, "patches": 3, "pitted_surface": 4,
                          "rolled-in_scale":5, "scratches": 6}

#遍历xml树根的节点信息
def get(root, name):
    vars = root.findall(name)
    return vars

def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def convert(xml_list, xml_dir, json_file):
    '''
    :param xml_list: 需要转换的XML文件列表
    :param xml_dir: XML的存储文件夹
    :param json_file: 导出json文件的路径
    :return: None
    '''
    list_fp = xml_list
    image_id=0
    # 标注json的基本结构
    json_dict = {"images":[],
                 "type": "instances",
                 "annotations": [],
                 "categories": []}
    categories = PRE_DEFINE_CATEGORIES
    bnd_id = START_BOUNDING_BOX_ID
    for line in list_fp:
        line = line.strip()
        print(" Processing {}".format(line))
        # 解析XML        
        #使用root.find / root.findall()方法在xml中定位所需的信息;
        #然后使用(.text)返回child/grandchild元素的值。
        xml_f = os.path.join(xml_dir, line)
        tree = ET.parse(xml_f)
        root = tree.getroot()
        filename = root.find('filename').text  # 取出图片名字
        image_id+=1
        size = get_and_check(root, 'size', 1)
        # 图片的基本信息
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename,
                 'height': height,
                 'width': width,
                 'id':image_id}
        json_dict['images'].append(image)
        # [循环嵌套]处理每个标注的检测框
        for obj in get(root, 'object'):
            # 取出检测框类别名称
            category = get_and_check(obj, 'name', 1).text
            # 更新类别ID字典
            if category not in categories:
                new_id = len(categories)
                categories[category] = new_id+1
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(get_and_check(bndbox, 'xmin', 1).text) - 1
            ymin = int(get_and_check(bndbox, 'ymin', 1).text) - 1
            xmax = int(get_and_check(bndbox, 'xmax', 1).text)
            ymax = int(get_and_check(bndbox, 'ymax', 1).text)
            assert(xmax > xmin)
            assert(ymax > ymin)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            annotation = dict()
            annotation['area'] = o_width*o_height
            annotation['iscrowd'] = 0
            annotation['image_id'] = image_id
            annotation['bbox'] = [xmin, ymin, o_width, o_height]
            annotation['category_id'] = category_id
            annotation['id'] = bnd_id
            annotation['ignore'] = 0
            # 设置分割数据，点的顺序为逆时针方向
            annotation['segmentation'] = [[xmin,ymin,xmin,ymax,xmax,ymax,xmax,ymin]]

            json_dict['annotations'].append(annotation)
            bnd_id = bnd_id + 1

    # 写入类别ID字典
    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    # 导出到json
    #mmcv.dump(json_dict, json_file)????
    #print(type(json_dict))

    json_data = json.dumps(json_dict)
    with  open(json_file, 'w') as w:
        w.write(json_data)


if __name__ == '__main__':
    root_path = './'
    #生成coco-2014格式
    if not os.path.exists(os.path.join(root_path,'coco/annotations')):
        os.makedirs(os.path.join(root_path,'coco/annotations'))
    if not os.path.exists(os.path.join(root_path, 'coco/train')):
        os.makedirs(os.path.join(root_path, 'coco/train'))
    if not os.path.exists(os.path.join(root_path, 'coco/val')):
        os.makedirs(os.path.join(root_path, 'coco/val'))
    
    #####｛可修改｝xml文件地址
    ##注意分开xml和图片
    xml_dir = os.path.join(root_path,'xml555') ##或：xml_dir = 'path'
    ##划分训练集和验证集
    xml_labels = os.listdir(xml_dir)
    np.random.shuffle(xml_labels)
    
    #9:1划分
    split_point = int(len(xml_labels)/10)

    # validation data
    xml_list = xml_labels[0:split_point]
    json_file = os.path.join(root_path,'coco/annotations/instances_val.json')
    convert(xml_list, xml_dir, json_file)
    for xml_file in xml_list:
        img_name = xml_file[:-4] + '.jpg'
        #####｛可修改｝voc图片路径
        shutil.copy(os.path.join(root_path, 'voc', img_name),
                    os.path.join(root_path, 'coco/val', img_name))    #复制文件（夹）
    # train data
    xml_list = xml_labels[split_point:]
    json_file = os.path.join(root_path,'coco/annotations/instances_train.json')
    convert(xml_list, xml_dir, json_file)
    for xml_file in xml_list:
        img_name = xml_file[:-4] + '.jpg'
        #####｛可修改｝voc图片路径
        shutil.copy(os.path.join(root_path, 'voc', img_name),
                    os.path.join(root_path, 'coco/train', img_name))
    