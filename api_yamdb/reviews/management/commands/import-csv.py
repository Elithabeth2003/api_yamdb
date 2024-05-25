"""
Модуль management команды для импорта данных.

Импортирует из CSV файлов в базу данных SQLite.
"""
import csv
import sqlite3
from random import randint

from django.conf import settings
from django.core.management.base import BaseCommand


path = str(settings.BASE_DIR) + '/data/'


def import_csv():
    conn = sqlite3.connect(str(settings.BASE_DIR) + '/db.sqlite3')
    cursor = conn.cursor()

    with open(
            f'{path}category.csv', 'r', newline='', encoding='utf-8'
    ) as csvfile:
        reader_category = csv.DictReader(csvfile, delimiter=',')
        to_db_category = [
            (row['id'], row['name'], row['slug'])
            for row in reader_category
        ]

    with open(
        f'{path}genre.csv', 'r', newline='', encoding='utf-8'
    ) as csvfile:
        reader_genre = csv.DictReader(csvfile, delimiter=',')
        to_db_genre = [
            (row['id'], row['name'], row['slug'])
            for row in reader_genre
        ]

    with open(
        f'{path}titles.csv', 'r', newline='', encoding='utf-8'
    ) as csvfile:
        reader_titles = csv.DictReader(csvfile, delimiter=',')
        to_db_titles = [
            (row['id'], row['name'], '', row['category'],
             row['year'])
            for row in reader_titles
        ]

    with open(
            f'{path}genre_title.csv', 'r', newline='', encoding='utf-8'
    ) as csvfile:
        reader_genre_title = csv.DictReader(csvfile, delimiter=',')
        to_db_genre_title = [
            (row['id'], row['title_id'], row['genre_id'])
            for row in reader_genre_title
        ]

    with open(
            f'{path}review.csv', 'r', newline='', encoding='utf-8'
    ) as csvfile:
        reader_review = csv.DictReader(csvfile, delimiter=',')
        to_db_review = [
            (row['id'], row['text'], row['score'], row['pub_date'],
             row['author'], row['title_id'])
            for row in reader_review
        ]

    with open(
            f'{path}comments.csv', 'r', newline='', encoding='utf-8'
    ) as csvfile:
        reader_comments = csv.DictReader(csvfile, delimiter=',')
        to_db_comments = [
            (row['id'], row['text'], row['pub_date'],
             row['author'], row['review_id'])
            for row in reader_comments
        ]

    with open(
            f'{path}users.csv', 'r', newline='', encoding='utf-8'
    ) as csvfile:
        reader_users = csv.DictReader(csvfile, delimiter=',')
        to_db_users = [
            (row['id'], '', '', '',
             row['username'], row['first_name'], row['last_name'],
             '', '', '', row['bio'],
             row['role'], str(randint(1000000, 10000000)), row['email'])
            for row in reader_users
        ]

    cursor.executemany(
        'INSERT INTO reviews_category '
        '(id, name, slug) VALUES (?, ?, ?)',
        to_db_category
    )
    conn.commit()
    cursor.executemany(
        'INSERT INTO reviews_genre (id, name, slug)'
        ' VALUES (?, ?, ?)',
        to_db_genre
    )
    conn.commit()
    cursor.executemany(
        'INSERT INTO reviews_title (id, name, description, category_id, year)'
        ' VALUES (?, ?, ?, ?, ?)',
        to_db_titles
    )
    conn.commit()
    cursor.executemany(
        'INSERT INTO reviews_title_genre (id, title_id, genre_id)'
        ' VALUES (?, ?, ?)',
        to_db_genre_title
    )
    conn.commit()
    cursor.executemany(
        'INSERT INTO reviews_review '
        '(id, text, score, pub_date, author_id, title_id)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        to_db_review
    )
    conn.commit()
    cursor.executemany(
        'INSERT INTO reviews_comment '
        '(id, text, pub_date, author_id, review_id)'
        ' VALUES (?, ?, ?, ?, ?)',
        to_db_comments
    )
    conn.commit()
    cursor.executemany(
        'INSERT INTO reviews_user (id, password, last_login, '
        'is_superuser, username, first_name, last_name,'
        'is_staff, is_active, date_joined, bio,'
        'role, confirmation_code, email)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        to_db_users
    )
    conn.commit()
    conn.close()


class Command(BaseCommand):
    """Команда для импорта данных из CSV файлов в базу данных SQLite."""

    def handle(self, *args, **kwargs) -> None:
        """Обрабатывает импорт данных из CSV-файлов в базу данных SQLite."""
        import_csv()
