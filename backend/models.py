from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    subtasks = relationship("SubTask", back_populates="goal", cascade="all, delete-orphan")

class SubTask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    description = Column(String)
    complexity_score = Column(Integer)
    
    goal = relationship("Goal", back_populates="subtasks")
