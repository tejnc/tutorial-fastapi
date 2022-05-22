from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from blog import schemas,models
from blog.database import get_db
from blog.hashing import Hash


router = APIRouter(
    tags=["Authentication"]
)


# Login
@router.post('/login')
def login( request: schemas.Login ,db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect password")

    # generate    
    return user