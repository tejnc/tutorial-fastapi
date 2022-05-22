from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from blog import schemas, models, database
from blog.hashing import Hash

router = APIRouter(
    tags=["users"],
    prefix="/user"
)

# Adding new user
@router.post("/")
def create_user(request: schemas.User , db: Session = Depends(database.get_db)):
    new_user = models.User(name = request.name, email=request.email, password= Hash.bcrypt(password=request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


# Displaying users
@router.get("/all", response_model=List[schemas.ShowUser])
def show_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


# getting user id
@router.get("/{id}",response_model=schemas.ShowUser)
def get_user(id: int, db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} is not available.")
    return user