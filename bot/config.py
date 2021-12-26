from pandas import read_excel

from utils import is_group

# путь к файлу с расписанием
SCHEDULE_PATH = "assets/schedule/FMIAT_schedule.xlsx"

# регулярное выражение для поиска учебных групп
GROUP_PATTERN = "^[а-яё]+-[а-яё]+-\d+\/\d+$"

# названия учебных групп
dfs = read_excel(SCHEDULE_PATH, sheet_name="расписание 1 неделя", engine="openpyxl")
headings = dfs.columns.ravel()
GROUPS = list(filter(lambda heading: is_group(heading), headings))
