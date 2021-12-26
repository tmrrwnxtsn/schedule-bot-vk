from datetime import datetime, timedelta
from re import sub

from pandas import read_excel, Series

import config
from utils import get_week_and_weekday_nums


def get_schedule(group_name: str, days_delta: int) -> str:
    now_time_with_delta = datetime.today() + timedelta(days=days_delta)

    week_num, weekday_num = get_week_and_weekday_nums(now_time_with_delta)
    school_week_num = 2 if week_num % 2 == 0 else 1

    time_strf = now_time_with_delta.strftime("%d.%m.%Y")

    schedule_text = f'Расписание {group_name} на {time_strf} ({school_week_num} учебная неделя):\n\n'

    # если воскресенье
    if weekday_num == 6:
        schedule_text += 'Пар нет &#128526;'
        return schedule_text

    dfs = read_excel(config.SCHEDULE_PATH, sheet_name=f"расписание {school_week_num} неделя", engine="openpyxl")
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
