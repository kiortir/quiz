import os

import dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from quiz import repository
from db import pool
from settings import settings


bot = AsyncTeleBot(settings.API_TOKEN)


@bot.message_handler(commands=["create"])
async def add_exercise(message: Message):
    ...


@bot.message_handler(commands=["leaderboard"])
async def get_leaderboard(message: Message):
    leaderboard = await repository.get_leaderboard()

    leaderboard_text = ""
    for index, position in enumerate(leaderboard):
        username, full_name, task_count = position
        leaderboard_text += f'<b>{index + 1}.</b> <a href="https://t.me/{username}">{full_name}</a> - <b>{task_count}</b>\n'

    await bot.send_message(
        message.chat.id, leaderboard_text, parse_mode="HTML"
    )


@bot.message_handler(commands=["task"])
async def get_random_exercise(message: Message):
    user_id = message.from_user.id
    await repository.create_user(
        user_id, message.chat.username, message.from_user.full_name
    )

    exercise = await repository.get_random_exercise_for_user(user_id)
    await repository.set_context(user_id, exercise.id)

    await bot.send_message(message.chat.id, exercise.body.question)


@bot.message_handler(func=lambda message: True)
async def get_exercise_by_id(message: Message):

    context = await repository.get_context(message.from_user.id)
    if context is None:
        await bot.send_message(message.chat.id, "Сначала запросите задачу")
        return

    context_dict = context
    print(context, context_dict)

    taskid = context_dict.get("id")
    task = await repository.get_exercise(taskid)
    answer = task.body.answer
    if answer == message.text:
        await repository.add_solved_task(message.from_user.id, taskid)
        await bot.send_message(message.chat.id, "Все верно")
        await repository.set_context(message.from_user.id, None)
    else:
        await bot.send_message(message.chat.id, "Нет. Пробуй еще")


async def init():
    await bot.remove_webhook()
    async with pool:
        await bot.polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(init())
