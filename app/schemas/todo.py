from datetime import datetime
from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    """Базовая схема для TODO."""

    title: str = Field(..., min_length=1, max_length=255, description="Название задачи")
    description: str | None = Field(
        None, max_length=1000, description="Описание задачи"
    )


class TodoCreate(TodoBase):
    """Схема для создания TODO."""

    pass


class TodoUpdate(BaseModel):
    """Схема для обновления TODO."""

    title: str | None = Field(
        None, min_length=1, max_length=255, description="Название задачи"
    )
    description: str | None = Field(
        None, max_length=1000, description="Описание задачи"
    )
    completed: bool | None = Field(None, description="Статус выполнения")


class TodoResponse(TodoBase):
    """Схема ответа TODO."""

    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
