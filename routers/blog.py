from fastapi import APIRouter , Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session

from blog import schemas, models, database  # import blog module


router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

# get all the blogs
@router.get("/" , response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# create a blog post
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# deleting the data based on id
@router.delete("/delete/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"


# updating the data in the database
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog ,db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f"Blog with id {id} not found.")
    blog.update({"title":request.title, "body": request.body})
    # db.query(models.Blog).filter(models.Blog.id == id)\
    #     .update({"title":request.title, "body": request.body})
    db.commit()
    return "updated"


# get the blog with the specific id
@router.get("/{id}", status_code=200 , response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if  not blog:
        raise HTTPException(status_code=404, detail=f"Blog with the id {id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available."}
    return blog