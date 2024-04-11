from datetime import datetime
from typing import Optional


from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class Response(PostBase):
    pass


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None




class Post(PostBase):
    id: int
    last_update: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


# class PostOut(BaseModel):
#     Post: Post
#     votes: int

#     class Config:
#         orm_mode = True