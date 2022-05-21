from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI()

# path operation decorator
@app.get("/blog")
def index(limit : int = 10 , published : bool = True, sort: Optional[str] = None):   # query parameter 
    # only get 10 published blogs
    if published:
        return {"data":f" {limit} published blogs from blog list"}
    else:
        print("else statement")
        return {"data": f"{limit} blogs from blog list"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}")  # path parameter
def show(id: int):
    # fetch blog with id = id
    return {"data": id}
 

@app.get("/blog/{id}/comments")
def comments(id):
    # fetch comments 
    return {"data": {"hello", "wrong idea"}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] 


@app.post("/blog")
def create_blog(blog: Blog):
    return {"data": f"Blog is created with title as {blog.title}"}


# if __name__ == "__main__":
#     uvicorn.run(app,port=9000)