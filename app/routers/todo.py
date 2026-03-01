from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud.todo import (
    get_todos,
    get_todo,
    create_todo,
    update_todo,
    delete_todo,
)
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[TodoResponse])
async def read_todos(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Пропустить N записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    completed: bool | None = Query(None, description="Фильтр по статусу"),
):
    """Получить список всех TODO задач."""
    return await get_todos(db, skip=skip, limit=limit, completed=completed)


@router.get("/{todo_id}", response_model=TodoResponse)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    """Получить TODO задачу по ID."""
    todo = await get_todo(db, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO с ID {todo_id} не найден",
        )
    return todo


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_new_todo(
    todo_in: TodoCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создать новую TODO задачу."""
    return await create_todo(db, todo_in)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_existing_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Обновить существующую TODO задачу."""
    todo = await update_todo(db, todo_id, todo_in)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO с ID {todo_id} не найден",
        )
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Удалить TODO задачу."""
    deleted = await delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO с ID {todo_id} не найден",
        )
