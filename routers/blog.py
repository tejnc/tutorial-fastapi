from fastapi import APIRouter , Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session

from blog import schemas, models, database  # import blog module
from functions import blog
from functions.oauth2 import get_current_user


router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

# get all the blogs
@router.get("/" , response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(get_current_user)):
    return blog.get_all(db)


# create a blog post
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(request, db)


# deleting the data based on id
@router.delete("/delete/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db:Session = Depends(database.get_db)):
    return blog.delete(db ,id)


# updating the data in the database
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog ,db: Session = Depends(database.get_db)):
   return blog.update(db,request,id)


# get the blog with the specific id
@router.get("/{id}", status_code=200 , response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(database.get_db)):
    return blog.show(db,id)