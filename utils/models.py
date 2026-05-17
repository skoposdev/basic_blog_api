from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    id:       int
    username: str
    email:    Optional[str] = None
    password: str

class UserRegister(BaseModel):
    username: str
    email:    str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id:       int
    username: str
    email:    str

class ArticleCreate(BaseModel):
    author:  str
    title:   str
    content: str

class ArticleResponse(BaseModel):
    id:        int
    author:    str
    title:     str
    content:   str
    timestamp: int

class ArticleUpdate(BaseModel):
    title: Optional[str]   = None
    content: Optional[str] = None