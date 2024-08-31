from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Author, User
from madr.schemas import AuthorList, AuthorPublic, AuthorSchema
from madr.security import get_current_user

router = APIRouter(prefix='/authors', tags=['authors'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
def create_author(author: AuthorSchema, session: Session, user: CurrentUser):
    db_author = session.scalar(
        select(Author).where(Author.name == author.name)
    )

    if not db_author:
        author = Author(
            name=author.name,
        )
        session.add(author)
        session.commit()
        session.refresh(author)

        return author

    raise HTTPException(
        status_code=HTTPStatus.CONFLICT,
        detail='Author is already included in MADR!',
    )


@router.get('/', response_model=AuthorList)
def list_authors(  # noqa
    session: Session,
    name: str or None = None,
    offset: int or None = None,
    limit: int or None = None,
):
    query = select(Author)

    if name:
        query = query.filter(Author.name.contains(name))

    authors = session.scalars(query.offset(offset).limit(limit)).all()

    return {'authors': authors}


@router.delete('/{author_id}')
def delete_author(author_id: int, session: Session, user: CurrentUser):
    author = session.scalar(select(Author).where(Author.id == author_id))

    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in MADR.',
        )

    session.delete(author)
    session.commit()

    return {'message': 'Author has been deleted successfully.'}


@router.patch('/{author_id}', response_model=AuthorPublic)
def patch_author(author_id: int, session: Session, author: AuthorSchema):
    db_author = session.scalar(select(Author).where(Author.id == author_id))

    if not db_author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Author not found in MADR.',
        )

    for key, value in author.model_dump(exclude_unset=True).items():
        setattr(db_author, key, value)

    session.add(db_author)
    session.commit()
    session.refresh(db_author)

    return db_author
