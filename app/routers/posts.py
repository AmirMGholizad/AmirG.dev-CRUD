from typing import List
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, oauth2
from ..database import get_db
from ..schemas import CreatePost, Response, UpdatePost, Post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
def test_posts(db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user),
               limit: int=10, skip: int=0, search: Optional[str]=None):
    
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(
    post: CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user.email)
    return new_post


@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),):
    my_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not my_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )
    return my_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this post",
        )
    else:
        db.delete(deleted_post)
        db.commit()
        return deleted_post


@router.put("/{id}", response_model=Response)
def update_post(id: int, updated_post: UpdatePost, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this post",
        )
    else:
        post_query.update(updated_post.model_dump(), synchronize_session=False)
        db.commit()
        return post
