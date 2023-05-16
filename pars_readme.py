from osgeo import gdal
import os
from osgeo import ogr
from pathlib import Path
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
path_list = []


def path_walk():
    rootdir = r'D:\Dev\bd_satellite\products'
    for path in Path(rootdir).iterdir():
        path_list.append(os.path.join(path))
    for p in path_list:
        for path in os.listdir(p):  # для каждой подпапки в папке продукта
            pattern = re.compile(r'^[0-9]+.\d{2}.[A-Z]+\d{3}.\D{3}')
            if pattern.match(path):  # сравнить с шаблоном названия папки с изображением
                path_img = os.path.join(p, path)  # сгенерить путь папка продукта + папка с изображением
                # pg_connect_insert(wv_pars(path_img))
                print(wv_pars(path_img))
    return


def wv_pars(path_img):
    files = os.listdir(path_img)
    for f in files:
        file = os.path.join(f)
        match_imd = re.search(r'^.+IMD', file)
        match_tif = re.search(r'^.+TIL$', file)
        if match_imd:
            file_path = os.path.join(path_img, file)
            imd_pars(file_path)
        elif match_tif:
            file_path = os.path.join(path_img, file)
            tif_pars(file_path)
    return dict_content


def imd_pars(file_path):
    with open(file_path) as f:
        content = list(filter(None, f.read().strip().split(';\n')))
        for el in content:
            params = el.strip('\t').split()
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
    gtif = gdal.Open(tif_path)
    # print(gtif)
    band_numbers = gtif.RasterCount  # band numbers
    dict_content['band_numbers'] = band_numbers
    # print(dict_content)
    return dict_content


path_walk()
