from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from blog import schemas,models
from blog.database import get_db
from blog.hashing import Hash
from blog.functions.jwttoken import create_access_token


router = APIRouter(
    tags=["Authentication"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Login
@router.post('/login')
def login( request: OAuth2PasswordRequestForm = Depends(),db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect password")

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

    # generate    
    # return user