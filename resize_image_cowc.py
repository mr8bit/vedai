import os
from PIL import Image
import numpy as np
Image.MAX_IMAGE_PIXELS = 1000000000
## This for resize iamge of COWC dataset
import cv2
import xml.etree.ElementTree as ET
import pandas
df = pandas.read_csv('train_labels.{0}'.format('csv'), names = ['filename','width','height','class','xmin','ymin','xmax','ymax'], skiprows=1)
num_file = 2932
def create_xml(path, list, x_coor, y_coor, num):
    full_path_to_image = os.path.abspath('cowc_image/image{0}.jpg'.format(path))
    annotation = ET.Element("annotation", verified="yes")
    folder = ET.SubElement(annotation, "folder").text = 'images'
    filename = ET.SubElement(annotation, "filename").text = '{0}.{1}'.format(path,'jpg')
    path = ET.SubElement(annotation, "path").text = '{0}'.format(full_path_to_image)
    source = ET.SubElement(annotation, "source")
    database = ET.SubElement(source, "database").text = 'Unknown'
    size = ET.SubElement(annotation, 'size')
    width = ET.SubElement(size, 'width').text = '1024'
    height = ET.SubElement(size, 'height').text = '1024'
    depth = ET.SubElement(size, 'depth').text = '3'
    segmented = ET.SubElement(annotation, 'segmented').text = '0'
    for index, row in list:
        object = ET.SubElement(annotation, 'object')
        name = ET.SubElement(object, 'name').text = row['class']
        pose = ET.SubElement(object, 'pose').text = 'Unspecified'
        truncated = ET.SubElement(object, 'truncated').text = '0'
        difficult = ET.SubElement(object, 'difficult').text = '0'
        bndbox = ET.SubElement(object, 'bndbox')
        x_min =row['xmin']-x_coor
        y_min =row['ymin']-y_coor
        x_max =row['xmax']-x_coor
        y_max =row['ymax']-y_coor
        if row['xmin']-x_coor < 0:
            x_min = 0
        if row['ymin']-y_coor < 0:
            y_min = 0
        if row['xmax']-x_coor > 1024:
            x_max = 1024
        if row['ymax']-y_coor > 1024:
            y_max = 1024
        xmin = ET.SubElement(bndbox, 'xmin').text = '{0}'.format(x_min)
        ymin = ET.SubElement(bndbox, 'ymin').text = '{0}'.format(y_min)
        xmax = ET.SubElement(bndbox, 'xmax').text = '{0}'.format(x_max)
        ymax = ET.SubElement(bndbox, 'ymax').text = '{0}'.format(y_max)
    tree = ET.ElementTree(annotation)
    tree.write("cowc_image/{0}.xml".format(num_file))

def resize(image_path):
    img = cv2.imread('cowc/{0}'.format(image_path))
    path =image_path.split('.')[0]
    height, width, channels = img.shape
    size_w = 1024
    size_h = 1024
    global df
    y_coor = 0
    mshtab = height/size_h
    print("Масштаб: {0}".format(mshtab))
    print("Ширина изображения: {0}".format(width))
    print("Ширина кадра: {0}".format(size_w))
    global num_file
    for y in range(int(mshtab)):
        x_coor = 0
        for x in range(int(mshtab)):
            if x == int(mshtab)-1:
                x_coor = width - size_w
                crop_img = img[y_coor:y_coor+size_h, x_coor:width]
                cv2.imwrite('cowc_image/{0}.jpg'.format(num_file), crop_img)
                rows = df[(df['filename']==image_path) & (df['xmax'] > x_coor) & (df['xmax'] < x_coor+width) & (df['ymax'] > y_coor) & (df['ymax'] < y_coor+size_h)]
                create_xml('image', rows.iterrows(), x_coor, y_coor,num_file)
                num_file+=1
            elif y == int(mshtab)-1:
                y_coor = height - size_h
                crop_img = img[y_coor:height, x_coor:x_coor+size_w]
                cv2.imwrite('cowc_image/{0}.jpg'.format(num_file), crop_img)
                rows = df[(df['filename']==image_path) & (df['xmax'] > x_coor) & (df['xmax'] < x_coor+size_w) & (df['ymax'] > y_coor) & (df['ymax'] < height)]
                create_xml('image', rows.iterrows(), x_coor, y_coor,num_file)
                num_file+=1
                x_coor +=1024
            else:
                crop_img = img[y_coor:y_coor+size_h, x_coor:x_coor+size_w]
                cv2.imwrite('cowc_image/{0}.jpg'.format(num_file), crop_img)
                rows = df[(df['filename']==image_path) & (df['xmax'] > x_coor) & (df['xmax'] < x_coor+size_w) & (df['ymax'] > y_coor) & (df['ymax'] < y_coor+size_h)]
                create_xml('image', rows.iterrows(), x_coor, y_coor,num_file)
                num_file+=1
                x_coor +=1024
        y_coor +=1024

if __name__ == '__main__':
    list = os.listdir('cowc/')
    for file in list:
        print("Work on: {0}".format(file))
        resize(file)
