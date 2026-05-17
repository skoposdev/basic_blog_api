from typing import Annotated

from fastapi import APIRouter, HTTPException, Form
from fastapi.params import Depends

import database.article_db
from database.user_db import get_user_by_id
from dependencies.dependencies import check_user_auth
from utils.models import ArticleCreate, ArticleUpdate

router = APIRouter()

@router.get("/articles")
async def get_articles():
    try:
        articles = database.article_db.return_all_articles()
        return articles
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/article/author/{article_author}")
async def get_article_by_author(article_author: str):
    try:
        article = database.article_db.return_article_by_author(article_author)
        return article
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/article/id/{article_id}")
async def get_article_by_id(article_id: int):
    try:
        article = database.article_db.return_article_by_id(article_id)
        return article
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/article")
async def create_article(article: Annotated[ArticleCreate, Form()], user = Depends(check_user_auth)):
    try:
        author = get_user_by_id(user.get("id"))
        row = database.article_db.insert_article(*author, article)
        return {"article": row}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/article/{article_id}")
async def update_article(article_id: int, article: Annotated[ArticleUpdate, Form()], user = Depends(check_user_auth)):
    try:
        author = get_user_by_id(user.get("id"))
        if database.article_db.check_if_author(article_id, *author):
            database.article_db.modify_article(article, article_id)
            return {"article": article}
        else:
            raise HTTPException(status_code=401, detail="You're not authorized to edit this article")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/article/{article_id}")
async def delete_article(article_id: int, user = Depends(check_user_auth)):
    try:
        author = get_user_by_id(user.get("id"))
        if database.article_db.check_if_author(article_id, *author):
            database.article_db.delete_article_by_id(article_id)
            return {"success": True}
        else:
            raise HTTPException(status_code=401, detail="You're not authorized to delete this article")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))