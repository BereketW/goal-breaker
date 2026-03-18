from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from database import Base

class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    description: Mapped[str] = Column(String, index=True)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), server_default=func.now())
    
    subtasks: Mapped[list["SubTask"]] = relationship("SubTask", back_populates="goal", cascade="all, delete-orphan")

class SubTask(Base):
    __tablename__ = "subtasks"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    goal_id: Mapped[int] = Column(Integer, ForeignKey("goals.id"))
    description: Mapped[str] = Column(String)
    complexity_score: Mapped[int] = Column(Integer)
    
    goal: Mapped["Goal"] = relationship("Goal", back_populates="subtasks")
