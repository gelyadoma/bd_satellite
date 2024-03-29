import psycopg2
from psycopg2 import Error
# from pars_readme import dict_content
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

sql_create_table = "CREATE TABLE IMAGE (ID SERIAL PRIMARY KEY,\
    NAME_PRODUCT TEXT,\
    SATELLITE_NAME TEXT,\
    PIXEL_RESOLUTION FLOAT,\
    BAND_INFO TEXT,\
    BAND_NUMBERS SMALLINT,\
    PROCESSING_LEVEL TEXT,\
    FORMAT SMALLINT,\
    DATE TIMESTAMPTZ,\
    CLOUD_COVER FLOAT,\
    GEOM GEOMETRY(POLYGON, 4326));"  # запрос на создание бд через криейт

sql_insert_data = "INSERT INTO image (name_product, satellite_name,\
    pixel_resolution,\
    band_info,\
    processing_level,\
    band_numbers,\
    format,\
    date, cloud_cover,\
    quicklook, geom)\
        VALUES (%(name_product)s, %(satellite_name)s, %(pixel_resolution)s,\
        %(band_info)s,\
        %(processing_level)s,\
        %(band_numbers)s,%(format)s,\
        %(date)s, %(cloud_cover)s,\
        %(quicklook)s, %(shp_prod)s);"


def pg_connect_insert(dict_content):
    try:
        connection = psycopg2.connect(
            port='5433',
            dbname='test_db',
            user='postgres',
            password='postgres'
        )
        # connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print('Вы подключились к базе')
        cursor = connection.cursor()
        # print('Информация о сервере PostgreSQL')
        # print(connection.get_dsn_parameters(), '\n')
        cursor.execute(sql_insert_data, dict_content)
        connection.commit()  # обязательно при выполнении запросов в бд
        # record = cursor.fetchone()
        print('Запись добавлена')
    except (Exception, Error) as error:
        print('Какая то фигня с подключением блин,', error)
        # connectioin.rollback() - если после запросов что-то не то - можно откатиться до предыдущего состояния базы
        # psycopg2.DatabaseError -  чтобы поймать все ошибки от одного оператора
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('Соединение закрыто')

# with - для создания транзакции внутри определенного блока в коде
# позволяет не писать явно коммит и ролбэк

# ИНСЕРТ ДИНАМИЧЕСКИ


# pg_connect_insert()