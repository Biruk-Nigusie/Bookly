from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

class BookCreateModel(BaseModel):
    title : str
    author : str

@app.get('/')
async def read_root():
    return {"message":"Hello World"}

# path parameter
@app.get('/greet1/{name}')
async def greet_name(name: str) -> dict:
    # str ->input type, dict ->return type
    return {"message": f"Hello {name}"}

# query parameter
@app.get('/greet2') 
async def greet_name(name: str) -> dict: #query parameters are specified on request handlers.
    return {"message": f"Hello {name}"}

#using both
@app.get('/greet3/{name}') 
async def greet_name(name: str, age:int) -> dict:# age is query parameter and name is path parameter
    return {"message": f"Hello {name}", "age":age}

# optional path parameter using python's inbuilt class "Optional" with default value(name = User, and age = 0)
@app.get('/greet4/') 
async def greet_name(name:Optional[str] = "User", age:int = 0) -> dict:
    return {"message": f"Hello {name}", "age":age}

@app.post('/create_book')
async def create_book(book_data:BookCreateModel):
    return {
        "title":book_data.title,
        "author":book_data.author
    }
# headers and status code
@app.get('/get_headers', status_code=200)
async def get_headers(
    accept:str = Header(None), # str type header with default None
    content_type:str = Header(None),
    user_agent:str = Header(None),
    host:str = Header(None),
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host
    return request_headers