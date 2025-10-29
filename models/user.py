from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Disambiguate relationships to Task
    tasks = relationship("Task", foreign_keys="Task.user_id", back_populates="owner")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
