from osgeo import gdal
import os
from osgeo import ogr
import re


path_folder = os.walk('./pars/014194668010_01')

ATTRIBUTE_KEY = {
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


def wv_pars(path_folder):
    for dirpath, dirname, filenames in path_folder:
        for filename in filenames:   # генерит пути с названием файлов
            files = os.path.join(dirpath, filename)
            match_imd = re.search(r'.IMD', files)
            match_tif = re.search(r'.TIF$', files)
            if os.path.isfile(files) and match_imd:
                imd_path.append(files)
            elif os.path.isfile(files) and match_tif:
                tif_path.append(files)
    return tif_path, tif_path
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


def shp_pars(shp_path):
    layerList = []
    for p in shp_path:
        gshp = ogr.Open(p)
        layer = gshp.GetName()
        print(layer)
        layerList.append(layer)
    dict_content['mask'] = layerList
    return dict_content


wv_pars(path_folder)
imd_pars(imd_path)
print(tif_pars(tif_path))
# print(shp_pars(shp_path))
