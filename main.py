from fastapi import FastAPI


app = FastAPI()

# path operation decorator
@app.get("/blog")
def index(limit : int = 10 , published : bool = True):   # query parameter 
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