from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


async def get_todos(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    completed: bool | None = None,
) -> list[Todo]:
    """Получить список TODO с фильтрацией."""
    query = select(Todo).offset(skip).limit(limit)

    if completed is not None:
        query = query.where(Todo.completed == completed)

    query = query.order_by(Todo.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_todo(db: AsyncSession, todo_id: int) -> Todo | None:
    """Получить TODO по ID."""
    query = select(Todo).where(Todo.id == todo_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_todo(db: AsyncSession, todo_in: TodoCreate) -> Todo:
    """Создать новый TODO."""
    todo = Todo(**todo_in.model_dump())
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(
    db: AsyncSession, todo_id: int, todo_in: TodoUpdate
) -> Todo | None:
    """Обновить существующий TODO."""
    update_data = todo_in.model_dump(exclude_unset=True)
    if not update_data:
        return await get_todo(db, todo_id)

    query = (
        update(Todo).where(Todo.id == todo_id).values(**update_data).returning(Todo)
    )
    result = await db.execute(query)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_todo(db: AsyncSession, todo_id: int) -> bool:
    """Удалить TODO."""
    query = delete(Todo).where(Todo.id == todo_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0
