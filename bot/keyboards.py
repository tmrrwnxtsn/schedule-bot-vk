from vkbottle.api.keyboard import Keyboard, Text


def default_keyboard():
    keyboard = Keyboard()
    keyboard.add_row()
    keyboard.add_button(Text("Моё расписание"), color="primary")
    keyboard.add_button(Text("Изменить группу"), color="primary")
    return keyboard.generate()


def first_lvl_schedule_keyboard():
    keyboard = Keyboard()
    keyboard.add_row()
    keyboard.add_button(Text("Пары"), color="primary")
    keyboard.add_button(Text("Экзамены"), color="primary")
    keyboard.add_row()
    keyboard.add_button(Text("Назад"), color="secondary")
    return keyboard.generate()


def second_lvl_schedule_keyboard():
    keyboard = Keyboard()
    keyboard.add_row()
    keyboard.add_button(Text("Сегодня"), color="primary")
    keyboard.add_button(Text("Завтра"), color="primary")
    keyboard.add_button(Text("День недели"), color="primary")
    keyboard.add_row()
    keyboard.add_button(Text("Назад"), color="secondary")
    return keyboard.generate()


def weekdays_keyboard():
    keyboard = Keyboard()
    keyboard.add_row()
    keyboard.add_button(Text("Пн"), color="primary")
    keyboard.add_button(Text("Вт"), color="primary")
    keyboard.add_button(Text("Ср"), color="primary")
    keyboard.add_row()
    keyboard.add_button(Text("Чт"), color="primary")
    keyboard.add_button(Text("Пт"), color="primary")
    keyboard.add_button(Text("Сб"), color="primary")
    keyboard.add_button(Text("Вс"), color="primary")
    keyboard.add_row()
    keyboard.add_button(Text("Назад"), color="secondary")
    return keyboard.generate()


def empty_keyboard():
    keyboard = Keyboard()
    return keyboard.generate()
