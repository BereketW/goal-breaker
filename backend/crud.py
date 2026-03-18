from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import models, schemas

async def create_item(db: AsyncSession, item: schemas.ItemCreate, related_items_data: list[schemas.RelatedItemCreate]) -> models.Item:
    db_item = models.Item(description=item.description)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    
    for related_item_data in related_items_data:
        db_related_item = models.RelatedItem(
            item_id=db_item.id,
            description=related_item_data.description,
            attribute_score=related_item_data.attribute_score
        )
        db.add(db_related_item)
    
    await db.commit()
    result = await db.execute(
        select(models.Item).options(selectinload(models.Item.related_items)).where(models.Item.id == db_item.id)
    )
    return result.scalar_one()

async def get_item(db: AsyncSession, item_id: int) -> models.Item:
    result = await db.execute(
        select(models.Item).options(selectinload(models.Item.related_items)).where(models.Item.id == item_id)
    )
    return result.scalar_one()

async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Item]:
    result = await db.execute(
        select(models.Item).options(selectinload(models.Item.related_items)).offset(skip).limit(limit).order_by(models.Item.created_at.desc())
    )
    return result.scalars().all()