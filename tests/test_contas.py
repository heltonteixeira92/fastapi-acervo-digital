from http import HTTPStatus

from madr.schemas import UserPublic


def test_create_account(client):
    data = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }

    response = client.post('/users/', json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_email_already_exists(client, user):
    data = {
        'username': 'Frederico',
        'email': user.email,
        'password': user.password,
    }

    response = client.post('/users/', json=data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'conta já consta no MADR'}


def test_create_user_username_already_exists(client, user):
    data = {
        'username': user.username,
        'email': 'foo@bar.com',
        'password': user.password,
    }

    response = client.post('/users/', json=data)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'conta já consta no MADR'}


# def test_read_users(client):
#     response = client.get('/users/')
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'users': []}


def test_read_user(client, user):
    response = client.get(f'/users/{user.id}/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_user_does_not_exists(client):
    response = client.get('/users/10/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user not found'}


def test_read_users_with_user(client, user):
    # Generate a dictionary representation of the model
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}

    assert response


def test_update_user(client, user, token):
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'mynewpassword',
    }

    response = client.put(f'/users/{user.id}', json=data, headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_user_not_enough_permission(client, other_user, token):
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'mynewpassword',
    }

    response = client.put(
        f'/users/{other_user.id}', json=data, headers=headers
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_user_does_not_exists(client):
    data = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'mynewpassword',
    }

    response = client.put('/users/1', json=data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}
