from enum import Enum
from typing import Any
# from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class User(BaseModel):

    id: int
    name: str | None


class ExerciseType(str, Enum):
    QUIZ = "quiz"
    TEXT = "text"


class ContextType(str, Enum):

    TASK = "task"


class ExerciseBody(BaseModel):

    question: str
    answer: str
    options: Any | None


class ExerciseBase(BaseModel):
    type: ExerciseType
    body: ExerciseBody

    difficulty: int = Field(ge=0, le=5)


class Exercise(ExerciseBase):

    id: UUID4
