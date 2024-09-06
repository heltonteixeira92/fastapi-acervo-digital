from http import HTTPStatus

from tests.conftest import AuthorFactory


def test_create_author(client, token):
    json = {
        'name': 'William Shakespeare',
    }

    response = client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.json() == {
        'id': 1,
        'name': 'william shakespeare',
    }


def test_create_author_already_exists(client, token, author):
    json = {
        'name': author.name,
    }

    response = client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json=json,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Author is already included in MADR!'


def test_list_authors_filter_title_should_return_1_author(
    session, client, token
):
    expected_authors = 1
    session.bulk_save_objects(
        AuthorFactory.create_batch(1, name='William Shakespeare')
    )
    session.commit()

    response = client.get(
        '/authors/?name=William Shakespeare',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['authors']) == expected_authors


def test_delete_author(session, client, token):
    author = AuthorFactory(name='William Shakespeare')
    session.add(author)
    session.commit()
    session.refresh(author)

    response = client.delete(
        f'/authors/{author.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Author has been deleted successfully.'
    }


def test_delete_author_error(client, token):
    response = client.delete(
        f'/authors/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


def test_patch_author_error(client, token):
    json = {'name': 'Test author'}

    response = client.patch(
        '/authors/10', json=json, headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author not found in MADR.'}


def test_patch_author(session, client, author, token):
    author = AuthorFactory(name='Paulo Coelho')
    json = {
        'name': 'William Shakespeare',
    }

    session.add(author)
    session.commit()

    response = client.patch(
        f'/authors/{author.id}',
        json=json,
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'william shakespeare'
