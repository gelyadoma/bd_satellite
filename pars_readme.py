from osgeo import gdal
import os
# from osgeo import ogr
from pathlib import Path, PurePath
import re
from pg_connect import pg_connect_insert


ATTRIBUTE_KEY = {
    'productOrderId': 'name_product',
    'satId': 'satellite_name',
    'bandId': 'band_info',
    'productLevel': 'processing_level',
    'bitsPerPixel': 'format',
    'generationTime': 'date',
    'cloudCover': 'cloud_cover',
    'meanCollectedGSD': 'pixel_resolution'
}

dict_content = {}
imd_path = []  # список файлов метаданных
tif_path = []  # список тифов

path_folder = os.walk('D:/Dev/bd_satellite/products/')
path_list = []


def path_walk(path_folder):
    # for path_folder, dirs, filenames in path_folder:
    #     pattern = re.compile(r'^[0-9]+.\d{2}.[A-Z]+\d{3}.\D{3}') 
    #     matches = [subdir for subdir in dirs if pattern.match(subdir)]
    #     for path in matches:
    #         print(path)
    # return 
    rootdir = r'D:\Dev\bd_satellite\products'
    for path in Path(rootdir).iterdir():
        # print(path)
        path_list.append(os.path.join(path))
    for p in path_list:
        # print(p) # корневые папки продуктов
        for path in os.listdir(p):  # для каждой подпапки в папке продукта
            pattern = re.compile(r'^[0-9]+.\d{2}.[A-Z]+\d{3}.\D{3}')
            if pattern.match(path):  # сравнить с шаблоном названия папки с ихображением
                path_img = os.path.join(p, path)  # сгенерить путь папка продукта + папка с изображением
                # print(path_img)
                wv_pars(path_img)
        # print(tif_pars(tif_path))
            # pg_connect_insert(dict_content)
    return


def wv_pars(path_img):
    files = os.listdir(path_img)
    # print(files)
    for f in files:
        file = os.path.join(f)
        # print(file)
        match_imd = re.search(r'^.+IMD', file)
        match_tif = re.search(r'.+TIF$', file)
        if match_imd:
            file_path = os.path.join(path_img, file)
            # imd_path.append(file_path)
            print(imd_pars(file_path))
            # print(file_path)
        elif match_tif:
            tif_path.append(file)
    print(imd_path)
    return 
    # print(imd_path)
    # return dict_content
    # print(tif_path)
    
    # print(shp_path)
# meanCollectedGSD


def imd_pars(file_path):
    # # print(imd_path)
    # for p in imd_path:
    #     # print(p)
        with open(file_path) as f:
            content = list(filter(None, f.read().strip().split(';\n')))
            # print(content)
            for el in content:
                params = el.strip('\t').split()
            # print(params)
                if len(params) > 3:
                    if params[3] in ATTRIBUTE_KEY.keys():
                        value_param = params[5]
                        key_dict = ATTRIBUTE_KEY[params[3]]
                        dict_content[key_dict] = value_param.strip('"')
                else:
                    if params[0] in ATTRIBUTE_KEY.keys():
                        value_param = params[2]
                        key_dict = ATTRIBUTE_KEY[params[0]]
                        dict_content[key_dict] = value_param.strip('"')
        return dict_content


def tif_pars(tif_path):
    for p in tif_path:
        gtif = gdal.Open(p)
        band_numbers = gtif.RasterCount  # band numbers
        dict_content['band_numbers'] = band_numbers
    return dict_content



# rootdir = '../bd_satellite/products/'
# path_list = []

# for path in Path(rootdir).iterdir():
#     if path.is_dir():
#         path_list.append(os.path.join(path))
#         for p in path_list:
#             wv_pars(p)
# print(path_list)
# # def shp_pars(shp_path):
# #     layerList = []
# #     for p in shp_path:
# #         gshp = ogr.Open(p)
# #         layer = gshp.GetName()
# #         print(layer)
# #         layerList.append(layer)
# #     dict_content['mask'] = layerList
# #     return dict_content

# def insert_pgdb():
path_walk(path_folder)
# wv_pars(path_list)
# imd_pars(imd_path)
# print(tif_pars(tif_path))

# print(shp_pars(shp_path))
