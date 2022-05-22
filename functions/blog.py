from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from blog import models


def get_all(db:Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(db: Session, id):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"


def update(db: Session, request, id):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f"Blog with id {id} not found.")
    blog.update({"title":request.title, "body": request.body})
    # db.query(models.Blog).filter(models.Blog.id == id)\
    #     .update({"title":request.title, "body": request.body})
    db.commit()
    return "updated"


def show(db: Session, id):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if  not blog:
        raise HTTPException(status_code=404, detail=f"Blog with the id {id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available."}
    return blog