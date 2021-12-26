from datetime import datetime
from re import match, IGNORECASE

import config


def get_week_and_weekday_nums(time: datetime) -> [int, int]:
    date = time.isocalendar()
    week_num, weekday_num = date[1], date[2] - 1
    return week_num, weekday_num


weekday_to_num = {
    "пн": 0,
    "вт": 1,
    "ср": 2,
    "чт": 3,
    "пт": 4,
    "сб": 5
}


def get_days_delta_by_weekday(weekday: str) -> int:
    weekday_num = weekday_to_num[weekday]
    now_weekday_num = datetime.today().weekday()
    return weekday_num - now_weekday_num


def is_group(s: str):
    return match(config.GROUP_PATTERN, s, flags=IGNORECASE)
