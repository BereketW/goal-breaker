from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import models, schemas

async def create_goal(db: AsyncSession, goal: schemas.GoalCreate, subtasks: list[schemas.SubTaskCreate]):
    db_goal = models.Goal(description=goal.description)
    db.add(db_goal)
    await db.commit()
    await db.refresh(db_goal)
    
    for task in subtasks:
        db_subtask = models.SubTask(
            goal_id=db_goal.id,
            description=task.description,
            complexity_score=task.complexity_score
        )
        db.add(db_subtask)
    
    await db.commit()
    result = await db.execute(
        select(models.Goal).options(selectinload(models.Goal.subtasks)).where(models.Goal.id == db_goal.id)
    )
    return result.scalar_one()

async def get_goal(db: AsyncSession, goal_id: int):
    result = await db.execute(
        select(models.Goal).options(selectinload(models.Goal.subtasks)).where(models.Goal.id == goal_id)
    )
    return result.scalar_one()

async def get_goals(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Goal).options(selectinload(models.Goal.subtasks)).offset(skip).limit(limit).order_by(models.Goal.created_at.desc())
    )
    return result.scalars().all()
