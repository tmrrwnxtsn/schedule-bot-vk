from utils import get_exams_groups, get_lessons_groups

# путь к файлу с расписанием занятий
LESSONS_PATH = "assets/schedule/FMIAT_lessons.xlsx"

# путь к файлу с расписанием экзаменов
EXAMS_PATH = "assets/schedule/FMIAT_exams.xlsx"

# регулярное выражение для поиска учебных групп
GROUP_PATTERN = "^[а-яё]+-[а-яё]+-\d+\/\d+$"

# названия учебных групп (для получения расписания занятий)
LESSONS_GROUPS = get_lessons_groups()

# названия учебных групп (для получения раписания экзаменов)
EXAMS_GROUPS = get_exams_groups()
