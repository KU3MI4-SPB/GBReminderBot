import time
import datetime
import logging
import asyncio
import pytz
import os
import sys

from aiogram import Bot, Dispatcher, executor, types
from lessons import timetable

TOKEN = "***********" # Ваш личный токен бота

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.reply(f"Привет, {user_full_name}!")

@dp.message_handler(commands=["lesson"])
async def lesson_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)

    next_lesson = None
    for lesson in timetable:
        if now.date() == lesson['date'] and now.time() < lesson['time']:
            next_lesson = lesson
            break
        else:
            if now.date() < lesson['date']:
                next_lesson = lesson
                break

    if next_lesson:
        next_lesson_time = next_lesson['time'].strftime('%H:%M')
        next_lesson_date = next_lesson['date'].strftime('%d-%m-%Y')
        response_text = f"Ближайшее занятие:\n Дата: {next_lesson_date}\n Время: {next_lesson_time} МСК\n Урок: {next_lesson['lesson']}\n Преподаватель: {next_lesson['teacher']}."
    else:
        response_text = "Ближайшее занятие не найдено"

    await message.answer(response_text)
    
@dp.message_handler(commands=["week"])
async def week_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    week_start = now - datetime.timedelta(days=now.weekday()) 
    week_end = week_start + datetime.timedelta(days=6)

    week_lessons = [lesson for lesson in timetable
                    if week_start.date() <= lesson['date'] <= week_end.date()]
    if not week_lessons:
        response_text = 'На этой неделе занятий нет'
    else:
        response_text = f'Расписание на текущую неделю с {week_start.date().strftime("%d-%m-%Y")} по {week_end.date().strftime("%d-%m-%Y")}:\n\n'
        for lesson in week_lessons:
            lesson_date = lesson['date'].strftime('%d-%m-%Y')
            lesson_time = lesson['time'].strftime('%H:%M')
            response_text += f'{lesson_date} {lesson_time} МСК - {lesson["lesson"]}\n'
    await message.answer(response_text)
    
allowed_users = [000000000, 000000000] # ID пользователей, которым разрешен доступ к команде

@dp.message_handler(commands=["reboot"])
async def reboot_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in allowed_users:
        await message.answer('Вы не имеете права на выполнение этой команды')
        return
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.answer('Бот перезапускается...')
    os.execve(sys.executable, [sys.executable] + sys.argv, os.environ)

@dp.message_handler()
async def handler(message: types.Message):
    await message.reply(f"Извините, «злой» студент, который написал меня... запретил с Вами разговаривать! Я могу только отвечать на заданные команды, которые находятся в Меню")

if __name__ == "__main__":
    executor.start_polling(dp)
