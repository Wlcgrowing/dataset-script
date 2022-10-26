# dataset-script
规范化管理数据集

## rename.py
用于对数据集中图片以及文件的重命名

## resize.py
批量修改图片的分辨率

## format.py
用于替换json中不合法的imagePath

## checkClasses.py
用于检测当前一共标注了多少class 并对检测结果进行输出

## labelme2coco.py
用于生成coco形式的标准数据集

## voc2coco.py      xml-->json
实现了从voc的.xml标注格式转换到coco的.json格式,同时进行训练／验证的分割 

## voc_split_trainVal.py
该脚本用于生成voc/目录下的ImageSets/..目录,分割了训练和验证集

## voc2yoloV5.py　和 voc2yoloV3.py      xml-->txt
两个脚本实现的功能几乎相同,灵活取用
> - V5脚本实现将voc格式的数据转化为yoloV5需要的.txt标注文件,运行该脚本，会在voc/目录下生成
worktxt/目录(yolo需要的格式).
> - V3这个脚本除了生成.txt的标注(同上)，还会生成一个trianval.txt的索引,以前的yolov3系列用的多一点

## coco_split_trainVal.py
该脚本实现coco格式的数据分割出训练集和验证集,同时里面还实现了一个去除背景图的方法(没有标注框的图)，可以结合上面的
voc_to_coco_v2.py使用.

## make_voc.py
make_voc.py就提供了一个制作voc格式数据的通用套路（核心代码）

## json2txt.py      json-->txt
该脚本实现从coco的.json格式转换到yolo的.txt格式

## txt2json.py      txt-->json
该脚本实现从yolo的.txt格式转换到coco的.json格式
# 具体操作可以参考视频


