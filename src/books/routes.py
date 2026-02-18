from fastapi import APIRouter
from src.books.schemas import Book, BookUpdteModel
from src.books.book_data import books
from typing import List
from fastapi import HTTPException, status

router = APIRouter()

@router.get('/', response_model=List[Book]) 
async def get_all_books():
    return books

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book_data:Book) ->dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@router.get('/{book_id}')
async def get_book(book_id:int) ->dict:
    for index, book in enumerate(books):
        if book["id"] == book_id:
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")
    
@router.patch('/{book_id}')
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

@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int):
    for book in books:
        if book["id"]  == book_id:
            books.remove(book)
            return None
    raise HTTPException(status_code=404, detail="Book not found")