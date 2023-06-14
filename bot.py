# Импорование необходимых модулей
import time # Импортирование модуля для работы со временем
import datetime # Импортирование модуля для работы с датой и временем
import logging # Импортирование модуля для логгирования (записи событий) приложения
import pytz # импортирование модуля для работы с часовыми поясами
import os # Импортирование модуля для работы с операционной системой
import sys # Импортирование модуля для работы со стандартными потоками ввода/вывода

from aiogram import Bot, Dispatcher, executor, types # Импортирование необходимых объектов из модуля aiogram
from lessons import timetable # Импортирование объекта timetable (расписания) из lessons.py

TOKEN = "***********" # Ваш личный токен бота

logging.basicConfig(level=logging.INFO) # Настройка логгера приложения на уровень INFO (вывод информационных сообщений и выше)

bot = Bot(token=TOKEN) # Инициализация объекта бота с токеном, переданным в переменной TOKEN (значение не указано в данном участке кода)
dp = Dispatcher(bot=bot) # Инициализация диспетчера для обработки входящих сообщений от бота. Передается объект бота в качестве параметра

@dp.message_handler(commands=["start"]) # Декоратор, указывающий на то, что обработчик сообщений будет отвечать только на команду /start
async def start_handler(message: types.Message): # Обработчик команды /start, который отправляет приветственное сообщение
    user_id = message.from_user.id # Получение id пользователя, отправившего сообщение
    user_name = message.from_user.first_name # Получение имени пользователя, отправившего сообщение
    user_full_name = message.from_user.full_name # Получение полного имени пользователя, отправившего сообщение
    logging.info(f'{user_id} {user_full_name} {time.asctime()}') # Запись информации о пользователе в логи приложения в формате: id пользователя, полное имя пользователя и время отправки сообщения
    await message.reply(f"Привет, {user_full_name}!") # Ответ на сообщение пользователю, который отправил команду /start с приветственным сообщением и использованием его полного имени

@dp.message_handler(commands=["lesson"]) # Декоратор, указывающий на то, что обработчик сообщений будет отвечать только на команду /lesson
async def lesson_handler(message: types.Message): # Обработчик команды /lesson, который находит ближайшее занятие
    user_id = message.from_user.id # Получение id пользователя, отправившего сообщение
    user_full_name = message.from_user.full_name # Получение полного имени пользователя, отправившего сообщение
    logging.info(f'{user_id} {user_full_name} {time.asctime()}') # Запись информации о пользователе в логи приложения в формате: id пользователя, полное имя пользователя и время отправки сообщения
    
    tz = pytz.timezone('Europe/Moscow') # Получаем информацию о часовом поясе "Europe/Moscow"
    now = datetime.datetime.now(tz) # Получаем текущее время now и присваиваем ему значение текущего дня и времени в указанном часовом поясе

    next_lesson = None # В переменную next_lesson записываем None
    for lesson in timetable: # Перебор всех занятий из расписания в цикле for
        if now.date() == lesson['date'] and now.time() < lesson['time']: # Если текущая дата совпадает с датой занятия и время занятия еще не наступило
            next_lesson = lesson # То эта информация записывается в переменную next_lesson
            break # Цикл прерывается с помощью оператора break
        else: # Иначе
            if now.date() < lesson['date']: # Если текущая дата меньше даты занятия
                next_lesson = lesson # То также происходит запись информации в переменную next_lesson
                break # Цикл снова прерывается

    if next_lesson: # Если переменная next_lesson не равна None
        next_lesson_time = next_lesson['time'].strftime('%H:%M') # В переменную next_lesson_time записывается время занятия в формате ЧАСЫ:МИНУТЫ
        next_lesson_date = next_lesson['date'].strftime('%d-%m-%Y') # В переменную next_lesson_date записывается дата занятия в формате ДЕНЬ-МЕСЯЦ-ГОД
        response_text = f"Ближайшее занятие:\n Дата: {next_lesson_date}\n Время: {next_lesson_time} МСК\n Урок: {next_lesson['lesson']}\n Преподаватель: {next_lesson['teacher']}." # Переменной присваевается данные ближайшего занятие с датой, временем, уроком и преподавателем
    else: # В противном случае, если значение next_lesson равно None
        response_text = "Ближайшее занятие не найдено" # То в переменную записывается, что ближайшее занятие не найдено

    await message.answer(response_text)  # В конце функции выдаем сообщение с текстом ответа отправляется пользователю, который вызвал команду
    
@dp.message_handler(commands=["week"]) # Декоратор, указывающий на то, что обработчик сообщений будет отвечать только на команду /week
async def week_handler(message: types.Message): # Обработчик команды /week, который отправляет расписание на текущую неделю
    user_id = message.from_user.id # Получение id пользователя, отправившего сообщение
    user_full_name = message.from_user.full_name # Получение полного имени пользователя, отправившего сообщение
    logging.info(f'{user_id} {user_full_name} {time.asctime()}') # Запись информации о пользователе в логи приложения в формате: id пользователя, полное имя пользователя и время отправки сообщения
    
    tz = pytz.timezone('Europe/Moscow') # Получаем информацию о часовом поясе "Europe/Moscow"
    now = datetime.datetime.now(tz) # Получаем текущее время now и присваиваем ему значение текущего дня и времени в указанном часовом поясе
    week_start = now - datetime.timedelta(days=now.weekday()) # Определяем дату начала текущей недели
    week_end = week_start + datetime.timedelta(days=6) # Определяем дату окончания текущей недели

    week_lessons = [lesson for lesson in timetable # Фильтруем занятия из списка "timetable"
                    if week_start.date() <= lesson['date'] <= week_end.date()] # Выбирая только те, которые проходят в текущую неделю
    if not week_lessons: # Если занятий не найдено
        response_text = 'На этой неделе занятий нет' # Записываем в переменную, что занятий нет на этой неделе
    else: # Иначе
        response_text = f'Расписание на текущую неделю с {week_start.date().strftime("%d-%m-%Y")} по {week_end.date().strftime("%d-%m-%Y")}:\n\n' # Записываем расписание на текущую неделю с начальной даты недели по конечную
        for lesson in week_lessons: # Перебираем все занятия на этой неделе
            lesson_date = lesson['date'].strftime('%d-%m-%Y') # В переменную lesson_date записывается дата занятия в формате ДЕНЬ-МЕСЯЦ-ГОД
            lesson_time = lesson['time'].strftime('%H:%M') # В переменную lesson_time записывается время занятия в формате ЧАСЫ:МИНУТЫ
            response_text += f'{lesson_date} {lesson_time} МСК - {lesson["lesson"]}\n' # Формируется список занятий в формате дата, время и урок
    await message.answer(response_text) # В конце функции выдаем сообщение с текстом ответа отправляется пользователю, который вызвал команду
    
allowed_users = [000000000, 000000000] # ID пользователей, которым разрешен доступ к команде /reboot

@dp.message_handler(commands=["reboot"]) # Декоратор, указывающий на то, что обработчик сообщений будет отвечать только на команду /reboot
async def reboot_handler(message: types.Message): # Обработчик команды /reboot, который перезапускает бота
    user_id = message.from_user.id # Получение id пользователя, отправившего сообщение
    if user_id not in allowed_users: # Если пользователю не разрешен доступ к команде
        await message.answer('Вы не имеете права на выполнение этой команды') # Отправляем сообщение "Вы не имеете права на выполнение этой команды"
        return # Заканчиваем работу функции return
    user_full_name = message.from_user.full_name # Получение полного имени пользователя, отправившего сообщение
    logging.info(f'{user_id} {user_full_name} {time.asctime()}') # Запись информации о пользователе в логи приложения в формате: id пользователя, полное имя пользователя и время отправки сообщения
    await message.answer('Бот перезапускается...') # Отправляем сообщение "Бот перезапускается..."
    os.execve(sys.executable, [sys.executable] + sys.argv, os.environ) # Функция использует os.execve() для перезапуска скрипта. Его параметры передаются в виде списка sys.argv, который включает имя скрипта и его аргументы

@dp.message_handler() # Декоратор, указывающий на то, что обработчик сообщений будет отвечать только на все сообщения кроме команд
async def handler(message: types.Message): # Обработчик всех остальных сообщений, которые не являются командами
    await message.reply(f"Извините, «злой» студент, который написал меня... запретил с Вами разговаривать! Я могу только отвечать на заданные команды, которые находятся в Меню") # Отвечаем пользователю

if __name__ == "__main__": # Если код запускается как главный файл (main)
    executor.start_polling(dp) # То происходит запуск бота в режиме ожидания сообщений от пользователя
