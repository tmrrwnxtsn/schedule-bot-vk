from datetime import timedelta, datetime
from re import sub

import pandas
from pandas import Series, read_excel

import config
from utils import get_group_exams_sheet, get_week_and_weekday_nums


def get_lessons(group_name: str, days_delta: int) -> str:
    now_time_with_delta = datetime.today() + timedelta(days=days_delta)

    week_num, weekday_num = get_week_and_weekday_nums(now_time_with_delta)
    school_week_num = 2 if week_num % 2 == 0 else 1

    time_strf = now_time_with_delta.strftime("%d.%m.%Y")

    schedule_text = f'Расписание занятий {group_name} на {time_strf} ({school_week_num} учебная неделя):\n\n'

    # если воскресенье
    if weekday_num == 6:
        schedule_text += 'Пар нет &#128526;'
        return schedule_text

    dfs = read_excel(config.LESSONS_PATH, sheet_name=f"расписание {school_week_num} неделя", engine="openpyxl")
    dfs.index = Series(dfs.index).fillna(method='ffill')

    pd_data = dfs[group_name][8 * weekday_num:8 * (weekday_num + 1)]
    pd_data = pd_data[pd_data.notnull()]

    group_dict = pd_data.to_dict()
    if group_dict:
        for lesson_number, lesson_name in group_dict.items():
            schedule_text += f"{lesson_number % 8 + 1} пара: {sub(' +', ' ', lesson_name.strip())}\n\n"
    else:
        schedule_text += 'Пар нет &#128526;'

    return schedule_text


def get_exams(group_name: str):
    sheet_name = get_group_exams_sheet(group_name)

    dfs = read_excel(config.EXAMS_PATH, sheet_name=sheet_name, skiprows=6, engine="openpyxl")

    pd_data_exams = dfs[group_name]
    pd_data_dates = dfs["Дата"]

    dates = pd_data_dates.to_list()
    exams = pd_data_exams.to_list()

    schedule_text = f'Расписание экзаменов {group_name}:\n\n'

    has_exams = False
    for i in range(len(dates)):
        if isinstance(exams[i], str):
            has_exams = True
            if not pandas.isna(dates[i]):
                date_strf = dates[i].strftime("%d.%m.%Y")
                exam_strf = sub(" {2,}", " ", exams[i].replace("\n", ", ").strip())
                schedule_text += f'{date_strf} — {exam_strf}\n\n'
            elif "каникулы" in exams[i]:
                exam_strf = sub(" {2,}", " ",
                                exams[i].replace("\n", ", ").replace("каникулы", "&#10071; Каникулы").strip())
                schedule_text += f'{exam_strf}'

    if not has_exams:
        schedule_text += "Экзаменов нет &#128526;"

    return schedule_text
