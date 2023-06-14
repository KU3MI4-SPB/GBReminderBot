import datetime
import pytz

tz = pytz.timezone('Europe/Moscow')
now = datetime.datetime.now(tz)

timetable = [
    {
        'date': datetime.date(2023, 6, 13),
        'time': datetime.time(19, 0),
        'lesson': 'Создание структуры базы данных (лекция)',
        'teacher': 'Ильнар Шафигуллин',
    },
    {
        'date': datetime.date(2023, 6, 13),
        'time': datetime.time(20, 0),
        'lesson': 'Базы данных (дополнительная лекция)',
        'teacher': 'Ильнар Шафигуллин',
    },
    {
        'date': datetime.date(2023, 6, 15),
        'time': datetime.time(13, 0),
        'lesson': 'Создание структуры базы данных (семинар)',
        'teacher': 'Тимур Исламгулов',
    },
    {
        'date': datetime.date(2023, 6, 18),
        'time': datetime.time(12, 0),
        'lesson': 'Итоги блока. Выбор специализации (лекция)',
        'teacher': 'GeekBrains',
    }
]