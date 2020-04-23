from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime
)
from sqlalchemy.orm import relationship

from frost.server.database import Base, User as U


class User(U):
    scores = relationship(
        'Score',
        back_populates='user'
    )


class Score(Base):
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True, nullable=False)

    score = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship(
        'User',
        back_populates='scores'
    )

    def __repr__(self) -> str:
        return f'<Score user_id={repr(self.user_id)} score={repr(self.score)}>'
