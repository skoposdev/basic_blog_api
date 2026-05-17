# uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.articles.articles import router as articles_router
from routes.auth.auth import router as auth_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router, tags=["auth"])
app.include_router(articles_router, tags=["articles"])

app.get("/")
async def root():
    return {"message": "Hello World"}