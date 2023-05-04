import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


try:
    connection = psycopg2.connect(
        user='',
        password='',
        host='',
        port=''
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = 'create database test_bd' # запрос на создание бд через криейт
    cursor.execute(sql_create_database)
except (Exception, Error) as error:
    print('Какая то фигня с постгресом блин,', error)
    # connectioin.rollback() - если после запросов что-то не то - можно откатиться до предыдущего состояния базы
    # psycopg2.DatabaseError -  чтобы поймать все ошибки от одного оператора
finally:
    if connection:
        cursor.close()
        connection.close()
        print('Соединение закрыто')

# with - для создания транзакции внутри определенного блока в коде
# позволяет не писать явно коммит и ролбэк 