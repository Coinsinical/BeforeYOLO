# 该脚本用于将数据集按照比例进行分配（依照YOLOV5官方样例）
# 该脚本文件需要修改第11-12行，设置train、val、test的切分的比率
import os
import sys
import random
import shutil
import argparse

# 配置数据集分配比例
train_percent = 0.9
val_percent = 0.1
test_percent = 0
# seed = 42 # 随机数种子，固定值可保证每次结果相同

# 设置xml文件目录与图片目录（相对路径或绝对路径均可）
dataset_path = './stone' # 包含标签与图片文件的数据目录
imgs_dirname = 'JPEGImages' # 图片文件夹名
xml_dirname =  'Annotations' # 标签文件夹名


dataset_abspath = os.path.abspath(dataset_path)
imgs_path = os.path.join(dataset_abspath,imgs_dirname)
xml_file_path = os.path.join(dataset_abspath,xml_dirname)

# 获取所有img文件名
filenames = os.listdir(imgs_path)
xmlnames = os.listdir(xml_file_path)

if len(filenames) != len(xmlnames):
    lossimg_list = []
    lostlabel_list = []
    for file in filenames:
        name = os.path.splitext(file)[0]
        if f'{name}.xml' not in xmlnames:
            loss_list.append(name)
    print(loss_list)
else:   
    # 打乱文件名列表
    # random.seed(seed)
    random.shuffle(filenames)

    # 计算数量
    num = len(filenames)
    train_num = int(num * train_percent)
    val_num = int(num * val_percent)
    test_num = int(num * test_percent)

    diff = num - train_num - val_num - test_num
    if diff < 0 :
        train_num = train_num + diff 


    # 创建输出文件夹
    for name in ('images','labels',xml_dirname):
        for kind in ('train','val','test'):
            os.makedirs(os.path.join(dataset_abspath,name,kind),exist_ok=True)

    sets = ['train','val','test']
    for index,kind_set in enumerate((filenames[:train_num],filenames[train_num:train_num + val_num],filenames[train_num + val_num:])):
        # filename为图片文件名
        for file in kind_set:
            name = os.path.splitext(file)[0]
            img_path = os.path.join(imgs_path,file)
            xml_path = os.path.join(xml_file_path,f'{name}.xml')
            txt_path = os.path.join(dataset_abspath,'labels',f'{name}.txt') # 获取相应的txt文件路径
            shutil.copy(img_path,os.path.join(dataset_abspath,'images',sets[index]))
            shutil.move(txt_path,os.path.join(dataset_abspath,'labels',sets[index]))
            shutil.move(xml_path,os.path.join(xml_file_path,sets[index]))