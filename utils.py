from datetime import datetime
from re import match, IGNORECASE

from pandas import read_excel

import config

WEEKDAY_TO_NUM = {
    "пн": 0,
    "вт": 1,
    "ср": 2,
    "чт": 3,
    "пт": 4,
    "сб": 5,
    "вс": 6
}


def get_week_and_weekday_nums(time: datetime) -> [int, int]:
    date = time.isocalendar()
    week_num, weekday_num = date[1], date[2] - 1
    return week_num, weekday_num


def get_days_delta_by_weekday(weekday: str) -> int:
    weekday_num = WEEKDAY_TO_NUM[weekday]
    now_weekday_num = datetime.today().weekday()
    return weekday_num - now_weekday_num


def is_group(s: str):
    return match(config.GROUP_PATTERN, s, flags=IGNORECASE)


def get_exams_groups() -> dict:
    result = {}
    dfs = read_excel(config.EXAMS_PATH, sheet_name=None, skiprows=6, engine="openpyxl")
    for k, v in dfs.items():
        k_headings = v.columns.ravel()
        result[k] = list(filter(lambda heading: is_group(heading), k_headings))
    return result


def get_lessons_groups() -> list:
    dfs = read_excel(config.LESSONS_PATH, sheet_name="расписание 1 неделя", engine="openpyxl")
    headings = dfs.columns.ravel()
    return list(filter(lambda heading: is_group(heading), headings))


def get_group_exams_sheet(group_name: str) -> str:
    for k, v in config.EXAMS_GROUPS.items():
        if group_name in v:
            return k
    return ""
