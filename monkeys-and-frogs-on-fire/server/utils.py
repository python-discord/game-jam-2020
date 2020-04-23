import secrets

from frost.server.database.db import Base, engine, managed_session
from werkzeug.security import generate_password_hash


def init_db() -> None:
    from frost.server.database import Message, Room, User
    from server.models import Score

    Base.metadata.create_all(bind=engine)

    # Creates the master user and the main room
    with managed_session() as session:
        session.add_all([
            User(
                username='master',
                password=generate_password_hash(secrets.token_urlsafe())
            ),
            Room(
                name='Main Room',
                invite_code='main',
                owner_id=1
            )
        ])
        u = session.query(User).first()
        u.joined_rooms.append(
            session.query(Room).first()
        )
