from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TriviaQuestion(Base):
    """SQLAlchemy ORM model for trivia questions"""

    __tablename__ = "trivia_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    show_number = Column(Integer, nullable=False)
    air_date = Column(Date, nullable=True)
    round = Column(String(50), nullable=True)
    category = Column(String(255), nullable=True)
    value = Column(Integer, nullable=True)
    question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
