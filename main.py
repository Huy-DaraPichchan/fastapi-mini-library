from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from models import Book
from schema import BookResponse, BookCreate, BookUpdate

app = FastAPI()


@app.get("/books", response_model=list[BookResponse])
def get_books(
        search: str | None = None,
        year: int | None = None,
        available: bool | None = None,
        db: Session = Depends(get_db)
    ):
    
    query = db.query(Book)
    
    if search is not None:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%")
            )
        )
        
    if year is not None:
        query = query.filter(Book.year >= year)
    
    if available is not None:
        query = query.filter(Book.available == available)
        
    
    
    return query.all()

@app.get("/books/{bid}", response_model=BookResponse)
def get_book_detail(bid: int, db: Session = Depends(get_db)):
    
    book = db.query(Book).filter(Book.id == bid).first()
    
    if not book:
        raise HTTPException(
                status_code=404,
                detail="Book not found!"
            )
    return book
    

@app.post("/books/new")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.model_dump())
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    return {"message": "Book created!", "book": new_book}

@app.delete("/books/{bid}")
def delete_book(bid: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == bid).first()
    if not book:
        raise HTTPException(
                status_code=404,
                detail="Book not found!"
            )
    db.delete(book)
    db.commit()
    
    return {"message": "Book removed!"}
    
    
    
@app.put("/books/{bid}", response_model=BookResponse)
def update_book(bid: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == bid).first()
    
    if not db_book:
        raise HTTPException(
                status_code=404,
                detail="Book not found!"
            )
    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year
    db_book.available = book.available
    db_book.rating = book.rating
    
    db.commit()
    db.refresh(db_book)
    
    return db_book
    
    