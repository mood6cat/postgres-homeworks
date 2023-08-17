"""Скрипт для заполнения данными таблиц в БД Postgres."""
# import psycopg2
#
# #conn to db Вместе с менеджером контекста
# conn = psycopg2.connect(
#     host='localhost',
#     database='north',
#     user='postgres',
#     password="84627913"
# )
# try:
#     with conn:
#         # create cursor для различных операций с БД
#         with conn.cursor() as cur:
#
#             # execute some query делем запрос
#             execute_some = cur.execute("")
# conn.close()

import psycopg2
import pandas
import os
from psycopg2 import extensions

def build_path(file: str) -> str:
    """
    Возвращает путь от корня проекта к указанному файлу в папке 'north_data'.

    file: название файла
    """

    path_to_file = os.path.join(os.path.dirname(__file__), 'north_data', file)
    return path_to_file


def add_data_to_table(table: str, data: pandas.DataFrame, cursor: psycopg2.extensions.cursor):
    """
    Добавляет переданные данные в указанную таблицу базы данных.

    table: название таблицы в базе данных
    data: данные для записи в таблицу
    cursor: объект для взаимодействия с базой данных
    """

    cursor.execute(f"TRUNCATE TABLE {table} CASCADE")

    columns = data.columns.tolist()
    string_placeholders = ", ".join(["%s"] * len(columns))
    command = f"INSERT INTO {table} VALUES ({string_placeholders})"

    for index, row in data.iterrows():
        values = [row[column] for column in columns]
        cursor.execute(command, tuple(values))


if __name__ == '__main__':
    customers = pandas.read_csv(build_path('customers_data.csv'))
    employees = pandas.read_csv(build_path('employees_data.csv'))
    orders = pandas.read_csv(build_path('orders_data.csv'))

    with psycopg2.connect(
            host='localhost',
            database='north',
            user='postgres',
            password='84627913'
    ) as conn:
        with conn.cursor() as cur:
            add_data_to_table("customers", customers, cur)
            add_data_to_table("employees", employees, cur)
            add_data_to_table("orders", orders, cur)

    conn.close()
