from fastapi import FastAPI

from blog import models
from blog.database import engine
from blog.routers import authentication, blog, user


app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)


models.Base.metadata.create_all(engine)






