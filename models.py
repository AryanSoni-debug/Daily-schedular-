from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    reminder_time = Column(DateTime, nullable=False)
