"""
Модуль management команды для импорта данных.

Импортирует из CSV файлов в базу данных SQLite.
"""
import csv
import sqlite3
from django.core.management.base import BaseCommand
from django.conf import settings


path = str(settings.BASE_DIR) + '/data/'
files = ('category.csv', 'genre.csv', 'titles.csv',
         'genre_title.csv', 'review.csv', 'comments.csv', 'users.csv')
tables = ('reviews_category', 'reviews_genre', 'reviews_title',
          'reviews_title_genre', 'reviews_review', 'reviews_comment',
          'reviews_user')


def import_csv_to_sqlite(csv_file, table_name):
    """Импортирует данные из CSV файла в базу данных SQLite."""
    conn = sqlite3.connect(str(settings.BASE_DIR) + '/db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(
        f'SELECT name FROM sqlite_master'
        f'WHERE type="table" AND name="{table_name}";'
    )
    if not cursor.fetchone():
        print(f'Table {table_name} does not exist. Skipping {csv_file}.')
        conn.close()
        return
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        columns = ', '.join(header)
        for row in csv_reader:
            size = ', '.join(['?'] * len(row))
            cursor.execute(
                f"INSERT INTO {table_name} ({columns}) VALUES ({size})", row
            )
    conn.commit()
    conn.close()


class Command(BaseCommand):
    """Команда для импорта данных из CSV файлов в базу данных SQLite."""

    def handle(self, *args, **kwargs) -> None:
        """Обрабатывает импорт данных из CSV-файлов в базу данных SQLite."""
        for file, table in zip(files, tables):
            try:
                print('start download', file)
                import_csv_to_sqlite(path + file, table)
                print('finish download', file)
            except Exception as e:
                print(e)
