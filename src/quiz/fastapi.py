from fastapi import APIRouter, Form
from fastapi.responses import FileResponse

from quiz.entity import ExerciseBase, ExerciseType, ExerciseBody, Exercise
from quiz import repository
from settings import settings
from uuid import UUID


router = APIRouter()


@router.get("/")
def root():
    return FileResponse(settings.static_path / "task.html")


@router.get("/questions")
async def get_questions() -> list[Exercise]:
    questions = await repository.get_all_exercises()
    return questions


@router.post("/questions")
async def create_question(
    body: str = Form(), answer: str = Form(), complexity: int = Form()
) -> UUID:
    b = ExerciseBody(question=body, answer=answer)
    excercise = ExerciseBase(
        body=b, difficulty=complexity, type=ExerciseType.TEXT
    )
    id = await repository.create_exercise(exercise=excercise)
    return id


@router.patch("/questions")
async def update_question():
    """Обновить данные о задаче"""
    ...


@router.delete("/questions")
async def delete_question():
    """Удалить задачу"""
    ...
