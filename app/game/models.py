from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    home_id = Column(Integer, ForeignKey("users.id"), index=True)
    home_life = Column(Integer, default=20)
    away_id = Column(Integer, ForeignKey("users.id"), index=True)
    away_life = Column(Integer, default=20)
    title = Column(String)
    description = Column(String)
    active = Column(Boolean, default=True)

    home_user = relationship("User", foreign_keys=[home_id])
    away_user = relationship("User", foreign_keys=[away_id])
