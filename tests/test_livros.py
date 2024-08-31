from http import HTTPStatus

import pytest

from tests.conftest import BookFactory


def test_create_book(author, client, token):
    json = {
        'title': 'Test book',
        'year': 1995,
        'author_id': author.id,
    }

    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.json() == {
        'id': 1,
        'title': json['title'],
        'year': json['year'],
        'author_id': json['author_id'],
    }


# def test_create_book_already_exists(client, token, session, author):
#     book = session.bulk_save_objects(
#         BookFactory.create_batch(5, title='test', author_id=author.id)
#     )
#     session.commit()
#
#     json = {
#         'title': book.title,
#         'year': 1995,
#         'author_id': author.id,
#     }
#
#     response = client.post(
#         '/books/',
#         headers={'Authorization': f'Bearer {token}'},
#         json=json,
#     )
#
#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json()['detail'] == 'Book is already included in MADR!'


def test_create_book_invalid_author(client, token):
    json = {
        'title': 'Test book',
        'year': 1995,
        'author_id': 10,
    }

    response = client.post(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Author does not exist'


@pytest.mark.skip
def test_list_books_should_return_5_books(session, client, author, token):
    expected_books = 5
    session.bulk_save_objects(BookFactory.create_batch(5, author_id=author.id))
    session.commit()

    response = client.get(
        '/books/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['books']) == expected_books


def test_list_books_pagination_should_return_2_books(
    session, client, author, token
):
    expected_books = 2
    session.bulk_save_objects(BookFactory.create_batch(5, author_id=author.id))
    session.commit()

    response = client.get(
        '/books/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['books']) == expected_books


def test_list_books_filter_title_should_return_5_books(
    session, client, author, token
):
    expected_books = 5
    session.bulk_save_objects(
        BookFactory.create_batch(5, author_id=author.id, year=1869)
    )
    session.commit()

    response = client.get(
        '/books/?year=1869',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['books']) == expected_books


def test_list_books_filter_title_should_return_1_book(
    session, client, author, token
):
    expected_books = 1
    session.bulk_save_objects(
        BookFactory.create_batch(
            1, author_id=author.id, title='Python Book', year=1992
        )
    )
    session.commit()

    response = client.get(
        '/books/?title=Python Book',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['books']) == expected_books


def test_list_books_filter_combined_should_return_5_books(
    session, author, client, token
):
    expected_books = 1
    session.bulk_save_objects(
        BookFactory.create_batch(
            1,
            title='Test book combined',
            author_id=author.id,
            year=2024,
        )
    )

    session.bulk_save_objects(
        BookFactory.create_batch(
            3,
            author_id=author.id,
            year=1992,
        )
    )
    session.commit()

    response = client.get(
        '/books/?title=Test book combined&year=2024',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['books']) == expected_books


def test_delete_book(session, client, author, token):
    book = BookFactory(author_id=author.id)
    session.add(book)
    session.commit()
    session.refresh(book)

    response = client.delete(
        f'/books/{book.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Book has been deleted successfully.'
    }


def test_delete_book_error(client, token):
    response = client.delete(
        f'/books/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found.'}


def test_patch_book_error(client, token):
    json = {
        'title': 'Test book',
        'year': 1995,
        'author_id': 1,
    }

    response = client.patch(
        '/books/10', json=json, headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found.'}


def test_patch_book(session, client, author, token):
    book = BookFactory(author_id=author.id)
    json = {
        'title': 'teste!',
        'year': 1995,
        'author_id': author.id,
    }

    session.add(book)
    session.commit()

    response = client.patch(
        f'/books/{book.id}',
        json=json,
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'
