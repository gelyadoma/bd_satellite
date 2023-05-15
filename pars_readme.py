from osgeo import gdal
import os
# from osgeo import ogr
from pathlib import Path
import re
from pg_connect import pg_connect_insert

# path_folder = os.walk('./bd_satellite/products/')

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

rootdir = r'D:\Dev\bd_satellite\products'
path_list = []
# imd_path = []  # список файлов метаданных
# tif_path = []


def path_walk(rootdir):
    # dict_content = {}
    for path in Path(rootdir).iterdir():
        print(path)
        path_list.append(os.path.join(path))
        for p in path_list:
            wv_pars(p)
            imd_pars(imd_path)
            tif_pars(tif_path)
            pg_connect_insert(dict_content)
    return


def wv_pars(p):
    for dirpath, dirname, filenames in os.walk(p):
        for filename in filenames:   # генерит пути с названием файлов
            files = os.path.join(dirpath, filename)
            match_imd = re.search(r'.IMD', files)
            match_tif = re.search(r'.TIF$', files)
            if os.path.isfile(files) and match_imd:
                imd_path.append(files)
            elif os.path.isfile(files) and match_tif:
                tif_path.append(files)
    return tif_path, imd_path
    # return dict_content
    # print(tif_path)
    # print(imd_path)
    # print(shp_path)
# meanCollectedGSD


def imd_pars(imd_path):
    for p in imd_path:
        with open(p) as f:
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
path_walk(rootdir)
# wv_pars(path_list)
# imd_pars(imd_path)
# print(tif_pars(tif_path))

# print(shp_pars(shp_path))
