from fastapi import FastAPI, Header, status, HTTPException
from typing import Optional, List
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
# ==========================

class Book(BaseModel):
        id: int
        title: str
        author: str
        publisher: str
        published_date:str
        page_count:int
        language: str

class BookUpdteModel(BaseModel):
        title: str
        author: str
        publisher: str
        page_count:int
        language: str

books = [
    {
        "id":1,
        "title":"Book 1",
        "author":"Author 1",
        "publisher":"Publisher 1",
        "published_date":"2023-01-01",
        "page_count":200,
        "language":"English"
    },
    {
        "id":2,
        "title":"Book 2",
        "author":"Author 2",
        "publisher":"Publisher 2",
        "published_date":"2023-01-02",
        "page_count":300,
        "language":"English"
    },
    {
        "id":3,
        "title":"Book 3",
        "author":"Author 3",
        "publisher":"Publisher 3",
        "published_date":"2023-01-03",
        "page_count":400,
        "language":"English"
    }
    ]

@app.get('/books', response_model=List[Book]) 
# Input should be a valid dictionary
async def get_all_books():
    return books
@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book_data:Book) ->dict:
    new_book = book_data.model_dump() # Convert the Pydantic model to a dictionary
    books.append(new_book)
    return new_book
@app.get('/books/{book_id}')
async def get_book(book_id:int) ->dict:
    for index, book in enumerate(books):
        if book["id"] == book_id:
            return books[index]
        raise HTTPException(status_code=404, detail="Book not found")
@app.patch('/books/{book_id}')
async def update_book(book_id:int, book_update_data:BookUpdteModel) ->dict:
    for book in books:
        if book["id"]  == book_id:
            book["title"] = book_update_data.title
            book["author"] = book_update_data.author
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language
            return book
        raise HTTPException(status_code=404, detail="Book not found")

@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int): # This api doesn't return any thing
    for book in books:
        if book["id"]  == book_id:
            books.remove(book)
            return None
    raise HTTPException(status_code=404, detail="Book not found")