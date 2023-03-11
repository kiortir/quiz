import os

import dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from quiz import repository
from db import pool


env = dotenv.load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")

print(API_TOKEN)
if not API_TOKEN:
    raise ValueError("Токен обязателен!")

bot = AsyncTeleBot(API_TOKEN)


@bot.message_handler(commands=["create"])
async def add_exercise(message: Message):
    ...
    # exercise = entity.ExerciseBase(
    #     type=entity.ExerciseType.TEXT, difficulty=3, body={"content": "test_task"}
    # )

    # eid = await repository.create_exercise(exercise)
    # await bot.send_message(message.chat.id, eid)


@bot.message_handler(commands=["task"])
async def get_random_exercise(message: Message):
    print("step 0")   
    await repository.create_user(message.from_user.id, message.from_user.full_name)
    print("step 1")
    exercise = await repository.get_random_exercise()
    print("step 2")
    await repository.set_context(message.from_user.id, exercise.id)
    print("step 3")
    await bot.send_message(message.chat.id, exercise.body.question)


@bot.message_handler(func=lambda message: True)
async def get_exercise_by_id(message: Message):

    context = await repository.get_context(message.from_user.id)
    # мне не очень нравится context == (None,), но я не знаю, как
    # можно сделать удобнее
    if not context or context == (None,):
        await bot.send_message(message.chat.id, "Сначала запросите задачу")
        return

    context_dict = context[0]
    print(context, context_dict)

    taskid = context_dict.get("id")
    task = await repository.get_exercise(taskid)
    answer = task.body.answer
    if answer == message.text:
        await bot.send_message(message.chat.id, "Все верно")
        await repository.destroy_context(message.from_user.id)
    else:
        await bot.send_message(message.chat.id, "Нет. Пробуй еще")


async def init():
    async with pool:
        await bot.polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(init())
