from osgeo import gdal
import os
# from osgeo import ogr
# from pathlib import Path
import re
# import pg_connect


path_folder = os.walk('./pars/')

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
path = []


def path_walk(path_folder):
    for path_folder, dirs, files in path_folder:
        # отбирает только те папки которые состоят из чисел
        # не обязательно если в директории кроме папок продуктов ничего нет
        pattern = re.compile(r'^[0-9]+.\d{2}$') 
        for subdir in dirs:
            if pattern.match(subdir):
                path = os.path.join(path_folder, subdir)
                print(path)
    return path
 

def wv_pars(path):
    for p in path:
        for dirpath, dirname, filenames in p:
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


path_walk(path_folder)
wv_pars(path)
imd_pars(imd_path)
tif_pars(tif_path)

