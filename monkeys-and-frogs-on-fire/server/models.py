from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DateTime
)
from sqlalchemy.orm import relationship

from frost.server.database import Base


class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, nullable=False)

    score = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User')

    def __repr__(self) -> str:
        return f'<Score id={repr(self.id)} user_id={repr(self.user_id)} score={repr(self.score)}>'
