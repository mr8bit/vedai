import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET



def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        print("Work on: {0}".format(xml_file))
        anything_on_filder = False
        for member in root.findall('object'):
            if member[0].text == "car":
                anything_on_filder = True
                x_min = int(member[4][0].text)
                y_min = int(member[4][1].text)
                x_max = int(member[4][2].text)
                y_max = int(member[4][3].text)
                if x_min < 0:
                    print("ERORR x_min < 0 in file: {0}".format(xml_file))
                    x_min = 0
                if int(member[4][1].text) < 0:
                    print("ERORR y_min < 0 in file: {0}".format(xml_file))
                    y_min = 0
                if int(member[4][0].text) > 256:
                    print("ERORR x_min > 256 in file: {0}".format(xml_file))
                    x_min = 256
                if int(member[4][1].text) > 256:
                    print("ERORR y_min > 256 in file: {0}".format(xml_file))
                    y_min = 256
                if int(member[4][2].text) > 256:
                    print("ERORR x_max > 256 in file: {0}".format(xml_file))
                    x_max = 256
                if int(member[4][3].text) > 256:
                    print("ERORR y_max > 256 in file: {0}".format(xml_file))
                    y_max = 256
                value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     x_min, y_min,
                     x_max, y_max)
                xml_list.append(value)
        if anything_on_filder==False:
            jpg = xml_file.split('.')[0]
            os.remove(xml_file)
            os.remove("{0}.jpg".format(jpg))
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df



def main():
    for directory in ['train', 'test']:
        image_path = os.path.join(os.getcwd(), 'images/{0}'.format(directory))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv('data/{0}_labels.csv'.format(directory), index=None)
        print('{0} Successfully converted xml to csv.'.format(directory))
main()
