from pydantic import BaseModel

# schemas can be considered pydantic model
class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(BaseModel):
    title: str
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True