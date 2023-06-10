# 该脚本文件需要修改第10行（classes）即可
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from tqdm import tqdm
import os

# 这里使用要改成自己的类别
classes = ['shi']

xml_path = 'stone/Annotations'

xml_path = os.path.abspath(xml_path) # 转换为绝对路径

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    x = round(x, 6)
    w = round(w, 6)
    y = round(y, 6)
    h = round(h, 6)
    return x, y, w, h


def convert_annotation(img_name):
    global xml_path
    labels_path = os.path.join(os.path.dirname(xml_path),'labels') # 在XML文件夹创建labels目录
    os.makedirs(labels_path,exist_ok=True)
    # try:
    in_file = open(f'{xml_path}/{img_name}.xml', encoding='utf-8')
    out_file = open(f'{labels_path}/{img_name}.txt', 'w', encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " +
                       " ".join([str(a) for a in bb]) + '\n')


for file in os.listdir(xml_path):
    name = os.path.splitext(file)[0]
    convert_annotation(name)


