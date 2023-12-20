import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import random
import os

block_list = ["安徽省", "云南省", "西藏自治区", "北京市", "台湾省"]

geo_file_path = './full/district/'
head_adcode = 100000

def get_file_name(index):
    return geo_file_path + str(index) + "_full.json"

# 加载中国和省份边界的GeoJSON文件
china_boundary_gpd = gpd.read_file(get_file_name(head_adcode), encoding='UTF-8')
china_boundary = china_boundary_gpd.geometry.unary_union

def get_point_province(point, parent_gpd, tag_list):
    for deltail_data in parent_gpd.itertuples():
        if deltail_data.geometry.contains(point):
            tag_list.append(deltail_data.name)
            if os.path.exists(get_file_name(deltail_data.adcode)):
                son_gpd = gpd.read_file(get_file_name(deltail_data.adcode), encoding='UTF-8')
                get_point_province(point, son_gpd, tag_list)
            
            return tag_list

def is_in_area(tags, area_name):
    for tag in tags:
        if tag == area_name:
            return True
     
    return False

def is_in_country(point):
    return china_boundary_gpd.geometry.unary_union.contains(point)

def generate_random_point_within_country():
    minx, miny, maxx, maxy = china_boundary.bounds
    while True:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if is_in_country(pnt):
            return pnt
        
def is_in_block_list(point, block_list):
    tags = get_point_province(point, china_boundary_gpd, [])

    for block in block_list:
        if is_in_area(tags, block):
            return False
    return True

if __name__ == "__main__":
    while True:
        random_point = generate_random_point_within_country()
        if is_in_block_list(random_point, block_list):
            break

    print(random_point)
    mpl.rcParams['figure.figsize']=(14,10)
    plt.style.use('ggplot')
    china_boundary_gpd.plot()
    print(get_point_province(random_point, china_boundary_gpd, []))
    plt.plot(random_point.x, random_point.y, 'ro')
    plt.show()