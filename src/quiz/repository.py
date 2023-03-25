import json
from typing import Any
from uuid import UUID

from db import pool
from quiz import entity


async def create_user(
    telegram_id: int, telegram_username: str, telegram_name: str | None = None
):

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(
                """
                    INSERT INTO telegram_user(id, name, username) VALUES(%s, %s, %s)
                    ON CONFLICT DO NOTHING RETURNING *
                """,
                (telegram_id, telegram_name, telegram_username),
            )
            r: tuple[int, str, str, str] | None = await cur.fetchone()
            if not r:
                return None
            id, name, context, username = r
            user = entity.User(
                id=id, name=name, context=context, username=username
            )
            return user


async def set_context(userid: int, taskid: UUID | None):

    task = (
        json.dumps({"type": entity.ContextType.TASK, "id": str(taskid)})
        if taskid is not None
        else None
    )

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
            r: tuple[int, str, str, str] | None = await cur.fetchone()

            if not r:
                return None

            id, name, context, username = r
            user = entity.User(
                id=id, name=name, context=context, username=username
            )
            return user


async def add_solved_task(userid: int, taskid: UUID):

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO user_exercise(telegram_user_id, exercise_id) VALUES(%s, %s) """,
                (userid, taskid),
            )


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

            if r is None:
                return None

            return next(iter(r), None)


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
                entity.Exercise(
                    id=id, type=type, body=body, difficulty=difficulty
                )
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
            if not r:
                return None
            id, type, body, difficulty = r
            exercise = entity.Exercise(
                id=id, type=type, body=body, difficulty=difficulty
            )

            return exercise


async def get_random_exercise_for_user(user_id: str) -> entity.Exercise:

    async with pool.connection() as aconn:
        async with aconn.cursor() as cur:
            # await cur.execute(
            #     """
            #     SELECT e.id FROM exercise e
            #     ORDER BY random()
            #     EXCEPT SELECT ue.exercise_id FROM user_exercise ue
            #         WHERE ue.telegram_user_id = %s
                
            #     """,
            #     (user_id,),
            # )
            await cur.execute(
                """
                SELECT
                    *
                FROM
                    exercise e
                WHERE NOT EXISTS (
                    SELECT
                        *
                    FROM
                        user_exercise
                    WHERE
                        telegram_user_id = %s AND
                        exercise_id = e.id
                )
                ORDER BY
                    random()
                LIMIT 1
                """,
                (user_id,),
            )
            r: tuple[UUID, str, str, int] | None = (await cur.fetchall())[0]
            print(r)
            if not r:
                return None
            id, type, body, difficulty = r
            exercise = entity.Exercise(
                id=id, type=type, body=body, difficulty=difficulty
            )

            return exercise


async def get_leaderboard(limit: int = 10) -> list[tuple[int, int]]:
    async with pool.connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                SELECT
                    username,
                    name,
                    COUNT(telegram_user_id) as count
                FROM
                    user_exercise
                LEFT JOIN telegram_user as t ON user_exercise.telegram_user_id = t.id
                GROUP BY
                    telegram_user_id, t.username, t.name
                ORDER BY
                    count DESC
                LIMIT %s
                """,
                (limit,),
            )

            res = await cursor.fetchall()
            print(res)
            return res
