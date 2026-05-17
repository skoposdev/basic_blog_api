import datetime
import sqlite3

from database.connection import get_article_connection
from utils.exceptions import InsertArticleError, ArticleUpdatingError, DeleteArticleError, ReturnedArticlesError, \
    ReturnedArticlesByAuthorError, ReturnedArticlesByIdError
from utils.models import ArticleCreate, ArticleUpdate, ArticleResponse


def init_article_db() -> None:
    with get_article_connection() as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS blog (
                                                         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                         author TEXT NOT NULL,
                                                         title TEXT NOT NULL,
                                                         content TEXT NOT NULL,
                                                         timestamp INTEGER NOT NULL
                     )
                     """)

def insert_article(author: str, article: ArticleCreate) -> ArticleCreate:
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with get_article_connection() as conn:
            conn.execute("""
                         INSERT INTO blog (author, title, content, timestamp)
                         VALUES (?, ?, ?, ?)""",
                         (author, article.title, article.content, timestamp)
                         )
            return article
    except sqlite3.IntegrityError:
        raise InsertArticleError("Error while inserting article (DuplicateAuthorError)")

def modify_article(article_update: ArticleUpdate, id: int) -> None:
    fields = []
    values = []

    try:
        with get_article_connection() as conn:
            if article_update.content is not None:
                fields.append("content = ?")
                values.append(article_update.content)

            if article_update.title is not None:
                fields.append("title = ?")
                values.append(article_update.title)

            conn.execute(f"UPDATE blog SET {', '.join(fields)} WHERE id = ?",
                         (*values, id)
                         )
    except sqlite3.IntegrityError:
        raise ArticleUpdatingError("Error while updating article")

def delete_article_by_id(id: int) -> None:
    try:
        with get_article_connection() as conn:
            conn.execute("""
                         DELETE FROM blog WHERE id = ?
                         """,
                         (id,)
                         )
    except sqlite3.IntegrityError:
        raise DeleteArticleError("Error while deleting article")

def return_all_articles() -> list[ArticleResponse]:
    try:
        with get_article_connection() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM blog
                """
            ).fetchall()

            return row
    except sqlite3.IntegrityError:
        raise ReturnedArticlesError("Error while retrieving all articles")

def return_article_by_author(author: str) -> list[ArticleResponse]:
    try:
        with get_article_connection() as conn:
            row = conn.execute(
                """
                SELECT *
                from blog
                WHERE author = ?
                """,
                (author,)
            ).fetchone()

            return row
    except sqlite3.IntegrityError:
        raise ReturnedArticlesByAuthorError("Error while retrieving articles by author")

def return_article_by_id(id: int) -> ArticleResponse:
    try:
        with get_article_connection() as conn:
            row = conn.execute(
                """
                SELECT *
                from blog
                WHERE id = ?
                """,
                (id,)
            ).fetchone()

            return row
    except sqlite3.IntegrityError:
        raise ReturnedArticlesByIdError("Error while retrieving articles by id")

def check_if_author(id: int, request_author: str) -> bool:
    try:
        with get_article_connection() as conn:
            row = conn.execute("""
                               SELECT author FROM blog WHERE id = ?
                               """,
                               (id,)
                               ).fetchone()
            (db_author, ) = row
            if db_author == request_author:
                return True
            else:
                return False

    except sqlite3.IntegrityError:
        raise ReturnedArticlesByAuthorError("Error while retrieving articles by author")