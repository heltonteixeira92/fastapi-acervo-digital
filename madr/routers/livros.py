from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Author, Book, User
from madr.schemas import BookList, BookPublic, BookSchema
from madr.security import get_current_user

router = APIRouter(prefix='/books', tags=['books'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
def create_book(book: BookSchema, session: Session):
    db_book = session.scalar(select(Book).where(Book.title == book.title))
    author = session.scalar(select(Author).where(Author.id == book.author_id))

    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author does not exist'
        )

    if not db_book:
        book = Book(title=book.title, year=book.year, author_id=author.id)
        session.add(book)
        session.commit()
        session.refresh(book)

        return book

    raise HTTPException(
        status_code=HTTPStatus.CONFLICT,
        detail='Book is already included in MADR!',
    )


@router.get('/', response_model=BookList)
def list_books(  # noqa
    session: Session,
    title: str or None = None,
    year: int or None = None,
    offset: int or None = None,
    limit: int or None = None,
):
    query = select(Book)

    if title:
        query = query.filter(Book.title.contains(title))

    if year:
        query = query.filter(Book.year == year)

    books = session.scalars(query.offset(offset).limit(limit)).all()

    return {'books': books}


@router.delete('/{book_id}')
def delete_book(book_id: int, session: Session):
    book = session.scalar(select(Book).where(Book.id == book_id))

    if not book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found.'
        )

    session.delete(book)
    session.commit()

    return {'message': 'Book has been deleted successfully.'}


@router.patch('/{book_id}', response_model=BookPublic)
def patch_book(book_id: int, session: Session, book: BookSchema):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found.'
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book
