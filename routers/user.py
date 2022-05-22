from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from blog import schemas, models, database
from functions import user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


# Adding new user
@router.post("/")
def create_user(request: schemas.User , db: Session = Depends(database.get_db)):
    return user.create_user(request,db)


# Displaying users
@router.get("/all", response_model=List[schemas.ShowUser])
def show_users(db: Session = Depends(database.get_db)):
    return user.show_user(db)


# getting user id
@router.get("/{id}",response_model=schemas.ShowUser)
def get_user(id: int, db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} is not available.")
    return user