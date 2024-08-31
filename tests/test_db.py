from sqlalchemy import select

from madr.models import User


def test_create_user(session):
    new_user = User(username='madman', password='secret', email='foo@bar.com')
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    user = session.scalar(select(User).where(User.username == 'madman'))

    assert user.username == 'madman'
    assert new_user.username == 'madman'
