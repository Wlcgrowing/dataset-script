from email.mime import image
import os
from PIL import Image
 
 
def ResizeImage(filein, fileout, width, height):
    """
    改变图片大小
    :param filein: 输入图片
    :param fileout: 输出图片
    :param width: 输出图片宽度
    :param height: 输出图片宽度
    :param type: 输出图片类型（png, gif, jpeg...）
    :return:
    """
    img = Image.open(filein)
    #width = int(img.size[0] * scale)
    #height = int(img.size[1] * scale)
    type = img.format
    out = img.resize((width, height), Image.ANTIALIAS)
    # 第二个参数：
    # Image.NEAREST ：低质量
    # Image.BILINEAR：双线性
    # Image.BICUBIC ：三次样条插值
    # Image.ANTIALIAS：高质量
    out.save(fileout, type)
 
 
if __name__ == "__main__":
    print("开始运行")
    image_path = './backgr'
    print(os.listdir(image_path))
    for file in os.listdir(image_path):
        filein = os.path.join(image_path,file)
        fileout = filein
        ResizeImage(filein, fileout,960,540)
    #filein = r'E:\Desktop\SmallObjectAugmentation-master\backgr\img1.jpg'
    #fileout = r'E:\Desktop\SmallObjectAugmentation-master\backgr\img2.jpg'
    