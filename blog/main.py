from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List


from .database import engine, SessionLocal
from . import schemas, models
from .hashing import Hash


app = FastAPI()


models.Base.metadata.create_all(engine)



# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
    # return {"title": request.title, "body": request.body}


# deleting the data based on id
@app.delete("/blog/delete/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found.")
    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"


# updating the data in the database
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog ,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f"Blog with id {id} not found.")
    blog.update({"title":request.title, "body": request.body})
    # db.query(models.Blog).filter(models.Blog.id == id)\
    #     .update({"title":request.title, "body": request.body})
    db.commit()
    return "updated"


@app.get("/blog" , response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=200 , response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if  not blog:
        raise HTTPException(status_code=404, detail=f"Blog with the id {id} is not available.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available."}
    return blog


# Adding new user
@app.post("/user")
def create_user(request: schemas.User , db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email=request.email, password= Hash.bcrypt(password=request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


# Displaying users
@app.get("/user/all", response_model=List[schemas.ShowUser])
def show_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users