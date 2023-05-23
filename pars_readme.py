from osgeo import gdal, ogr
import os
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
        print(f'Open folder: {p}')
        for path in os.listdir(p):  # для каждого элемента в папке продукта
            pattern = re.compile(r'^[0-9]+.\d{2}.[A-Z]+\d{3}.\D{3}$')
            if pattern.match(path):  # сравнить с шаблоном названия папки с изображением
                path_img = os.path.join(p, path)
                # print(path_img)  # сгенерить путь папка продукта + папка с изображением
                pg_connect_insert(wv_pars(path_img, p))
    return


def wv_pars(path_img, p):
    files = os.listdir(path_img)
    for f in files:
        # print(f)
        file = os.path.join(f)
        # print(file)
        match_imd = re.search(r'^.+IMD', file)
        match_til = re.search(r'^.+TIL$', file)
        if match_imd:
            file_path = os.path.join(path_img, file)
            imd_pars(file_path)
        elif match_til:
            # file_path = os.path.join(path_img, file)
            # print(file_path)
            til_pars(p, path_img, file)
    print('Success')
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


def til_pars(p, path_img, file):
    file_path = os.path.join(path_img, file)
    gtil = gdal.Open(file_path)
    ql_path = f'{p}\\{file[:-4]}_quickLook.tif'
    gtil = gdal.Warp(ql_path, gtil, creationOptions=['widthPct = 10, heightPct = 10'])
    if not gtil:
        return 'fail'
    print('QuickLook created')
    dict_content['quicklook'] = ql_path
    band_numbers = gtil.RasterCount  # band numbers
    dict_content['band_numbers'] = band_numbers
    gtil = None
    for path_shp in os.listdir(p):
        pattern = re.compile('GIS_FILES')
        # найти папку с шейпами
        if pattern.match(path_shp):
            print('Match folder with shpfile')
            shp_dir = os.path.join(p, path_shp)
            # print(shp_dir) # D:\Dev\bd_satellite\products1\052746661010_01\GIS_FILES
            for shp_file in os.listdir(shp_dir):
                # найти шейп
                # print(shp_file) # D:\Dev\bd_satellite\products1\052746661010_01\GIS_FILES\052746661010_01.dbf
                pattern = f'{file[:-4]}_PIXEL_SHAPE.shp'
                shp_pattern = re.compile(pattern)
                if shp_pattern.match(str(shp_file)):
                    print(f'Match:{shp_file}')
                    shp_path = os.path.join(shp_dir, shp_file)
                    shpToWkt(shp_path)

    return gtil, dict_content


def shpToWkt(shp_path):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shp_path, 0)
    layer = dataSource.GetLayer()
    for feature in layer:
        geom = feature.GetGeometryRef()
        geomwkt = geom.ExportToWkt()
        # print(geomwkt)
        dict_content['shp_prod'] = geomwkt
        print('WKT created')
    return dict_content


path_walk()
