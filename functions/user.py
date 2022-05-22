from blog import models
from sqlalchemy.orm import Session

from blog.hashing import Hash


def create_user(request,db:Session):
    new_user = models.User(name = request.name, email=request.email, password= Hash.bcrypt(password=request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


def show_user(db:Session):
    users = db.query(models.User).all()
    return users