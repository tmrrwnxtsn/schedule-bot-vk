import asyncio
import time
from os import getenv
from random import randint

from vkbottle import Bot
from vkbottle.bot import Blueprint, Message
from vkbottle.types.methods.groups import GroupsGetMembers
from vkbottle.types.methods.messages import MessagesSend

import config
from database import StudentDatabase
from keyboards import *
from schedule import get_lessons, get_exams
from utils import get_days_delta_by_weekday, is_group

bp = Blueprint(name="Обработчик сообщений")
db = StudentDatabase(getenv("DATABASE_URL"))

bot_api = Bot(getenv("TOKEN")).api

get_members = GroupsGetMembers(bot_api.request)
messages_send = MessagesSend(bot_api.request)

loop = asyncio.get_event_loop()
gid = loop.run_until_complete(bot_api.group_id)
get_members_response = loop.run_until_complete(get_members(group_id=str(gid), filter="managers"))

announcer_ids = []
for announcer in get_members_response.items:
    announcer_ids.append(dict(announcer)["id"])


@bp.on.message(text=["Начать", "Start", "Привет", "Здравствуй", ".", "/start"], lower=True)
async def handle_start_msg(ans: Message):
    if db.check_student(ans.from_id):
        await ans("Привет! На связи Фмиашка! &#128156; Напиши:\n\n"
                  "&#10145; «Моё расписание», чтобы перейти к расписанию выбранной учебной группы\n\n"
                  "&#10145; «Изменить группу», чтобы поменять группу, расписание которой ты будешь получать\n\n",
                  keyboard=default_keyboard())
    else:
        await ans("Привет! На связи Фмиашка! &#128156;\n\n"
                  "Ты что, опять забыл своё расписание? &#9785;\nЭх, всё на мне, всё на мне..\n\n"
                  "Пиши название своей группы, и я тебе помогу!\nНапример ПМ-О-20/1 или АТПП-О-20/1 &#128400;",
                  keyboard=empty_keyboard())


@bp.on.message(text=["Назад", "Главное меню", "Помощь", "Хелп", "Помоги"], lower=True)
async def handle_back_msg(ans: Message):
    if db.check_student(ans.from_id):
        await ans("Напиши:\n\n"
                  "&#10145; «Моё расписание», чтобы перейти к расписанию выбранной учебной группы\n\n"
                  "&#10145; «Изменить группу», чтобы поменять группу, расписание которой ты будешь получать\n\n",
                  keyboard=default_keyboard())
    else:
        await ans("Напиши название учебной группы, чтобы узнать её расписание &#9999; "
                  "Например, ПМ-О-21/1 или АТПП-О-20/1.", keyboard=empty_keyboard())


@bp.on.message(text=["Моё расписание"], lower=True)
async def handle_my_schedule_msg(ans: Message):
    if db.check_student(ans.from_id):
        await ans("Напиши:\n\n"
                  "&#10145; «Пары», чтобы получить расписание занятий\n\n"
                  "&#10145; «Экзамены», чтобы узнать расписание экзаменов\n\n"
                  "&#10145; «Назад», чтобы вернуться в главное меню", keyboard=first_lvl_schedule_keyboard())
    else:
        await ans("Группа не выбрана! Напиши название учебной группы, чтобы узнать её расписание &#9999; "
                  "Например, ПМ-О-21/1 или АТПП-О-20/1.", keyboard=empty_keyboard())


@bp.on.message(text=["Пары"], lower=True)
async def handle_my_lessons_schedule_msg(ans: Message):
    if db.check_student(ans.from_id):
        await ans("Напиши:\n\n"
                  "&#10145; «Сегодня», чтобы получить расписание занятий на сегодняшний день\n\n"
                  "&#10145; «Завтра», чтобы узнать расписание занятий на завтрашний день\n\n"
                  "&#10145; «День недели», чтобы получить расписание занятий на выбранный день ТЕКУЩЕЙ недели\n\n"
                  "&#10145; «Назад», чтобы вернуться в главное меню", keyboard=second_lvl_schedule_keyboard())
    else:
        await ans("Группа не выбрана! Напиши название учебной группы, чтобы узнать её расписание &#9999; "
                  "Например, ПМ-О-21/1 или АТПП-О-20/1.", keyboard=empty_keyboard())


@bp.on.message(text=["Экзамены"], lower=True)
async def handle_my_exams_schedule_msg(ans: Message):
    if db.check_student(ans.from_id):
        student_group = db.get_group(ans.from_id)
        schedule_text = get_exams(student_group)
        await ans(schedule_text, keyboard=first_lvl_schedule_keyboard())
    else:
        await ans("Группа не выбрана! Напиши название учебной группы, чтобы узнать её расписание &#9999; "
                  "Например, ПМ-О-21/1 или АТПП-О-20/1.", keyboard=empty_keyboard())


@bp.on.message(text=["Сегодня", "Завтра"], lower=True)
async def handle_day_schedule_msg(ans: Message):
    if db.check_student(ans.from_id):
        student_group = db.get_group(ans.from_id)
        if ans.text.lower() == "сегодня":
            schedule_text = get_lessons(student_group, 0)
        else:
            schedule_text = get_lessons(student_group, 1)
        await ans(schedule_text, keyboard=second_lvl_schedule_keyboard())
    else:
        await ans("Группа не выбрана! Напиши название учебной группы, чтобы узнать её расписание &#9999; "
                  "Например, ПМ-О-21/1 или АТПП-О-20/1.", keyboard=empty_keyboard())


@bp.on.message(text=["День недели"], lower=True)
async def handle_weekday_schedule_msg(ans: Message):
    if db.check_student(ans.from_id):
        await ans("Напиши сокращённое название дня недели: «Пн», «Вт», «Ср», «Чт», «Пт», «Сб», «Вс» &#9999;",
                  keyboard=weekdays_keyboard())
    else:
        await ans("Группа не выбрана! Напиши название учебной группы, чтобы узнать её расписание &#9999; "
                  "Например, ПМ-О-21/1 или АТПП-О-20/1.", keyboard=empty_keyboard())


@bp.on.message(text=["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"], lower=True)
async def handle_get_weekday_schedule_msg(ans: Message):
    if db.check_student(ans.from_id):
        student_group = db.get_group(ans.from_id)
        days_delta = get_days_delta_by_weekday(ans.text.lower())
        schedule_text = get_lessons(student_group, days_delta)
        await ans(schedule_text, keyboard=weekdays_keyboard())
    else:
        await ans("Группа не выбрана! Напиши название учебной группы, чтобы узнать её расписание &#9999; "
                  "Например, ПМ-О-21/1 или АТПП-О-20/1.", keyboard=empty_keyboard())


@bp.on.message(text=config.LESSONS_GROUPS)
async def handle_group_msg(ans: Message):
    db.information(ans.from_id, ans.text)
    await ans(f"Твоя группа обновлена на {ans.text} &#9989;")
    await handle_my_schedule_msg(ans)


@bp.on.message(text=["Изменить", "Изменить группу", "Поменять группу"], lower=True)
async def handle_change_group(ans: Message):
    await ans("Напиши название учебной группы, чтобы узнать её расписание &#9999; Например, ПМ-О-21/1 или АТПП-О-20/1.",
              keyboard=empty_keyboard())


@bp.on.message()
async def handle_unknown_msg(ans: Message):
    split_user_input = ans.text.split("\n", 1)
    if is_group(split_user_input[0]) and ans.from_id in announcer_ids:
        student_ids = db.get_student_ids_by_group(split_user_input[0])
        for student_id in student_ids:
            await messages_send(user_id=student_id[0], random_id=randint(-200000000, 2100000000),
                                message=split_user_input[1])
            time.sleep(1)  # DDOS attack off :D
        await ans(
            f"{len(student_ids)} студент(-ов) из {split_user_input[0]} получил(-и) сообщение «{split_user_input[1]}»")
    else:
        await ans("Ты что, спишь еще &#128516;?\n\n"
                  "Перепроверь группу: у нас с рождения ФМИАТ'а такой не было... &#9785;")
