import json
from typing import Any
from uuid import UUID

from db import pool
from quiz import entity


async def create_user(telegramid: int, telegram_name: str | None = None):
    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(
                """
                    INSERT INTO telegram_user(id, name) VALUES(%s, %s)
                    ON CONFLICT DO NOTHING  RETURNING *
                """,
                (telegramid, telegram_name),
            )
            r: tuple[int, str, str] | None = await cur.fetchone()

            if not r:
                return None
            id, name, context = r
            user = entity.User(id=id, name=name, context=context)
            return user


async def set_context(userid: int, taskid: UUID):

    task = json.dumps({"type": entity.ContextType.TASK, "id": str(taskid)})

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(
                """
                UPDATE telegram_user
                    SET context = %s
                    WHERE id = %s
                    RETURNING *
                """,
                (task, userid),
            )
            r: tuple[int, str, str] | None = await cur.fetchone()

            if not r:
                return None

            id, name, context = r
            user = entity.User(id=id, name=name, context=context)
            return user


async def destroy_context(userid: int):

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(
                """
                UPDATE telegram_user
                    SET context = null
                    WHERE id = %s
                    RETURNING *
                """,
                (userid,),
            )
            r: tuple[int, str, str] | None = await cur.fetchone()

            if not r:
                return None

            id, name, context = r
            user = entity.User(id=id, name=name, context=context)
            return user


async def get_context(userid: int):

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(
                """
                SELECT context FROM telegram_user
                    WHERE id = %s
                """,
                (userid,),
            )
            r: tuple[str] | None = await cur.fetchone()

            return r


async def create_exercise(exercise: entity.ExerciseBase) -> UUID:

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            print((exercise.type, exercise.body.json(), exercise.difficulty))
            await cur.execute(
                """
                INSERT INTO exercise(type, body, difficulty) VALUES(%s, %s, %s)
                RETURNING id
                """,
                (exercise.type, exercise.body.json(), exercise.difficulty),
            )
            r: tuple[UUID, Any] | None = await cur.fetchone()
            if not r:
                raise Exception
            exerciseid, *_ = r
            return exerciseid


async def get_all_exercises() -> entity.Exercise:

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(
                """
                SELECT * FROM exercise
                """
            )
            r: list[tuple[UUID, str, str, int]] = await cur.fetchall()
            print(r)
            if not r:
                return None
            exercises = [
                entity.Exercise(id=id, type=type, body=body, difficulty=difficulty)
                for id, type, body, difficulty in r
            ]
            return exercises


async def get_exercise(id: UUID | str) -> entity.Exercise:

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(
                """
                SELECT * FROM exercise
                    WHERE id = %s
                """,
                (str(id),),
            )
            r: tuple[UUID, str, str, int] | None = await cur.fetchone()
            print(r)
            if not r:
                return None
            id, type, body, difficulty = r
            exercise = entity.Exercise(
                id=id, type=type, body=body, difficulty=difficulty
            )
            return exercise


async def get_random_exercise() -> entity.Exercise:

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(
                """
                SELECT * FROM exercise
                    ORDER BY random()
                    LIMIT 1
                """
            )
            r: tuple[UUID, str, str, int] | None = await cur.fetchone()
            print(r)
            if not r:
                return None
            id, type, body, difficulty = r
            print(id)
            exercise = entity.Exercise(
                id=id, type=type, body=body, difficulty=difficulty
            )
            return exercise
